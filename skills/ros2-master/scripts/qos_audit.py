#!/usr/bin/env python3
"""Static QoS contract auditor for ROS 2 Python nodes.

Walks a source tree, finds every create_publisher / create_subscription call
via `ast`, resolves each call's QoS to (reliability, durability, history,
depth), and flags topics where an in-repo publisher and subscriber would
silently fail to connect (the classic "I publish but nothing arrives" QoS
mismatch).

    python3 qos_audit.py <src_root>        # human-readable table
    python3 qos_audit.py <src_root> --json  # same data as JSON

Exit code is 1 if any INCOMPATIBLE pair is found, else 0.

ponytail: Python only (no C++ create_publisher<T>()); QoS variables resolve
only within the SAME module (no cross-file QoSProfile constants), and the
scan is whole-module, not control-flow-aware — a name assigned the SAME
QoSProfile value everywhere resolves fine regardless of order, but a name
reassigned to DIFFERENT QoSProfile values in different places is ambiguous
and reported as UNKNOWN(<name>) rather than guessed. .venv/build/install/
__pycache__/.git directories are skipped. Add cross-module resolution if a
shared qos_profiles.py module shows up.
"""
from __future__ import annotations

import ast
import json
import sys
from pathlib import Path

PRESETS = {
    "qos_profile_sensor_data": ("BEST_EFFORT", "VOLATILE", "KEEP_LAST", "5"),
    "qos_profile_system_default": ("SYSTEM_DEFAULT",) * 4,
    "qos_profile_services_default": ("RELIABLE", "VOLATILE", "KEEP_LAST", "10"),
    "qos_profile_parameters": ("RELIABLE", "VOLATILE", "KEEP_LAST", "1000"),
}
CALL_NAMES = {"create_publisher", "create_subscription"}


def last_name(node: ast.AST | None) -> str | None:
    """Final segment of a Name or Attribute chain, e.g. a.b.C -> 'C'."""
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    return None


def var_key(node: ast.AST) -> str | None:
    """Key used to look up a module-level QoSProfile variable: 'x' or 'self.x'."""
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) and node.value.id == "self":
        return f"self.{node.attr}"
    return None


def parse_qosprofile_call(call: ast.Call) -> tuple[str, str, str, str]:
    rel, dur, hist, depth = "RELIABLE", "VOLATILE", "KEEP_LAST", "?"
    for kw in call.keywords:
        if kw.arg == "reliability":
            rel = last_name(kw.value) or ast.unparse(kw.value)
        elif kw.arg == "durability":
            dur = last_name(kw.value) or ast.unparse(kw.value)
        elif kw.arg == "history":
            hist = last_name(kw.value) or ast.unparse(kw.value)
        elif kw.arg == "depth":
            if isinstance(kw.value, ast.Constant) and isinstance(kw.value.value, int):
                depth = str(kw.value.value)
            else:
                depth = ast.unparse(kw.value)
    return rel, dur, hist, depth


def collect_qos_vars(tree: ast.AST) -> dict[str, tuple[str, str, str, str]]:
    """Every `<name-or-self.attr> = QoSProfile(...)` in the module, any scope.

    A name assigned DIFFERENT QoSProfile values in more than one place (e.g.
    the same local `q` reused across two sibling methods) is ambiguous under
    our order-blind whole-module scan — dropped so callers fall through to
    UNKNOWN(<name>) instead of silently picking whichever Assign ast.walk
    happened to visit last.
    """
    seen: dict[str, list[tuple[str, str, str, str]]] = {}
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign) or len(node.targets) != 1:
            continue
        key = var_key(node.targets[0])
        if key is None or not isinstance(node.value, ast.Call):
            continue
        if last_name(node.value.func) == "QoSProfile":
            seen.setdefault(key, []).append(parse_qosprofile_call(node.value))
    return {k: v[0] for k, v in seen.items() if len(set(v)) == 1}


def resolve_qos(node: ast.AST | None, qos_vars: dict) -> tuple[str, str, str, str]:
    if node is None:
        return ("UNKNOWN(missing)",) * 4
    if isinstance(node, ast.Constant) and isinstance(node.value, int) and not isinstance(node.value, bool):
        return ("RELIABLE", "VOLATILE", "KEEP_LAST", str(node.value))
    if isinstance(node, ast.Call) and last_name(node.func) == "QoSProfile":
        return parse_qosprofile_call(node)
    key = var_key(node)
    if key is not None and key in qos_vars:
        return qos_vars[key]
    preset = last_name(node)
    if preset in PRESETS:
        return PRESETS[preset]
    expr = ast.unparse(node)
    return (f"UNKNOWN({expr})",) * 4


def resolve_topic(node: ast.AST) -> str:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.JoinedStr):
        out = []
        for v in node.values:
            if isinstance(v, ast.Constant):
                out.append(str(v.value))
            elif isinstance(v, ast.FormattedValue):
                out.append("{" + ast.unparse(v.value) + "}")
        return "".join(out)
    return f"UNKNOWN({ast.unparse(node)})"


def kw(call: ast.Call, name: str) -> ast.AST | None:
    for k in call.keywords:
        if k.arg == name:
            return k.value
    return None


def extract_entries(path: Path, rel: Path, tree: ast.AST) -> list[dict]:
    qos_vars = collect_qos_vars(tree)
    entries = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        fname = last_name(node.func)
        if fname not in CALL_NAMES:
            continue
        args = node.args
        msg_node = args[0] if len(args) > 0 else kw(node, "msg_type")
        topic_node = args[1] if len(args) > 1 else kw(node, "topic")
        if fname == "create_publisher":
            qos_node = args[2] if len(args) > 2 else (kw(node, "qos_profile") or kw(node, "qos"))
        else:
            qos_node = args[3] if len(args) > 3 else (kw(node, "qos_profile") or kw(node, "qos"))
        if msg_node is None or topic_node is None:
            continue
        rel_, dur, hist, depth = resolve_qos(qos_node, qos_vars)
        entries.append({
            "file": str(rel), "line": node.lineno,
            "kind": "PUB" if fname == "create_publisher" else "SUB",
            "msg_type": last_name(msg_node) or ast.unparse(msg_node),
            "topic": resolve_topic(topic_node),
            "reliability": rel_, "durability": dur, "history": hist, "depth": depth,
        })
    return entries


SKIP_DIRS = {".venv", "venv", "build", "install", "__pycache__", ".git"}


def audit(src_root: Path) -> dict:
    entries = []
    for path in sorted(src_root.rglob("*.py")):
        if SKIP_DIRS & set(path.relative_to(src_root).parts[:-1]):
            continue
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except (SyntaxError, UnicodeDecodeError) as e:
            print(f"skip {path}: {e}", file=sys.stderr)
            continue
        entries.extend(extract_entries(path, path.relative_to(src_root), tree))

    by_topic: dict[str, list[dict]] = {}
    for e in entries:
        by_topic.setdefault(e["topic"], []).append(e)

    incompatible, one_sided, unresolved = [], [], []
    for topic, group in by_topic.items():
        unknown_topic = topic.startswith("UNKNOWN(")
        pubs = [e for e in group if e["kind"] == "PUB"]
        subs = [e for e in group if e["kind"] == "SUB"]
        if not unknown_topic and pubs and subs:
            for p in pubs:
                for s in subs:
                    reason = None
                    if s["reliability"] == "RELIABLE" and p["reliability"] == "BEST_EFFORT":
                        reason = "sub=RELIABLE, pub=BEST_EFFORT"
                    elif s["durability"] == "TRANSIENT_LOCAL" and p["durability"] == "VOLATILE":
                        reason = "sub=TRANSIENT_LOCAL, pub=VOLATILE"
                    if reason:
                        incompatible.append({"topic": topic, "reason": reason,
                                              "pub": p, "sub": s})
        elif not unknown_topic and (pubs or subs) and not (pubs and subs):
            one_sided.append({"topic": topic, "kind": "PUB" if pubs else "SUB",
                               "entries": pubs or subs})
        if unknown_topic:
            unresolved.extend(group)
    for e in entries:
        if e["reliability"].startswith("UNKNOWN(") and e not in unresolved:
            unresolved.append(e)

    return {"entries": entries, "incompatible": incompatible,
            "one_sided": one_sided, "unresolved": unresolved}


def row(e: dict) -> str:
    return f"{e['file']}:{e['line']} | {e['kind']} | {e['msg_type']} | {e['reliability']} | {e['durability']} | {e['history']}/{e['depth']}"


def print_text(result: dict) -> None:
    by_topic: dict[str, list[dict]] = {}
    for e in result["entries"]:
        by_topic.setdefault(e["topic"], []).append(e)
    for topic in sorted(by_topic):
        print(f"\n{topic}")
        for e in sorted(by_topic[topic], key=lambda x: (x["file"], x["line"])):
            print(f"  {row(e)}")

    print("\nINCOMPATIBLE")
    if not result["incompatible"]:
        print("  (none)")
    for inc in result["incompatible"]:
        print(f"  {inc['topic']}  [{inc['reason']}]")
        print(f"    PUB {row(inc['pub'])}")
        print(f"    SUB {row(inc['sub'])}")

    print("\nONE-SIDED (other side not in this repo — cannot verify statically)")
    if not result["one_sided"]:
        print("  (none)")
    for os_ in result["one_sided"]:
        print(f"  {os_['topic']}  (only {os_['kind']} found)")
        for e in os_["entries"]:
            print(f"    {row(e)}")

    print("\nUNRESOLVED")
    if not result["unresolved"]:
        print("  (none)")
    for e in result["unresolved"]:
        print(f"  {row(e)}")


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__)
        return 1
    src_root = Path(args[0]).resolve()
    if not src_root.is_dir():
        print(f"error: {src_root} is not a directory", file=sys.stderr)
        return 2
    result = audit(src_root)
    if "--json" in sys.argv:
        print(json.dumps(result, indent=2))
    else:
        print_text(result)
    return 1 if result["incompatible"] else 0


if __name__ == "__main__":
    sys.exit(main())
