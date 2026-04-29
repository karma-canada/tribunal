#!/usr/bin/env python3
"""
Recovery-pass parser. Reads scores.jsonl from a run and attempts to extract
scores from records that originally hit parse_error, using more permissive
heuristics than run.py's strict parser.

Writes scores.recovered.jsonl with all original records plus a
'recovery_status' field on each: 'untouched' (success/refusal preserved),
'recovered' (parse_error → score extracted), 'unrecovered' (parse_error
remains uninterpretable).

Usage:
    python3 recover.py runs/<run_id>
"""

import argparse
import json
import re
import sys
from pathlib import Path


def try_recover_score(content: str):
    """Best-effort score extraction from malformed model output.

    Strategies:
    1. Repair common bracket-confusion bugs (`]` instead of `}` closing object)
    2. Strip markdown fences with relaxed matching
    3. Truncate to first balanced JSON object even if surrounding noise
    4. Regex-extract bare 'score' field as last resort
    """
    if not content:
        return None, "no_content"

    text = content.strip()

    # Strip markdown fences (relaxed — trailing ``` may be missing)
    fence = re.match(r"^```(?:json)?\s*\n?(.*?)(?:\n```|$)", text, re.DOTALL)
    if fence:
        text = fence.group(1).strip()

    # Strategy 1: try strict parse
    try:
        obj = json.loads(text)
        s = int(obj.get("score"))
        if 1 <= s <= 10:
            return obj, "recovered_strict"
    except (json.JSONDecodeError, ValueError, TypeError, AttributeError):
        pass

    # Strategy 2: bracket repair — fix `]` closing what should be `}`
    # Common Claude bug: array of objects ends with `..."]` instead of `..."}`
    repaired = re.sub(r'(\}\s*)*"\s*\]\s*\n\s*,', '"}\n  ],', text)
    repaired = re.sub(r'\}\s*\]\s*,\s*\n', '}],\n', repaired)
    try:
        obj = json.loads(repaired)
        s = int(obj.get("score"))
        if 1 <= s <= 10:
            return obj, "recovered_bracket_repair"
    except (json.JSONDecodeError, ValueError, TypeError, AttributeError):
        pass

    # Strategy 3: extract the first balanced JSON object via brace counting
    start = text.find("{")
    if start != -1:
        depth = 0
        in_str = False
        esc = False
        for i in range(start, len(text)):
            c = text[i]
            if esc:
                esc = False
                continue
            if c == "\\":
                esc = True
                continue
            if c == '"':
                in_str = not in_str
                continue
            if in_str:
                continue
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    candidate = text[start:i + 1]
                    try:
                        obj = json.loads(candidate)
                        s = int(obj.get("score"))
                        if 1 <= s <= 10:
                            return obj, "recovered_extracted"
                    except (json.JSONDecodeError, ValueError, TypeError, AttributeError):
                        pass
                    break

    # Strategy 4: regex-extract the score field directly
    score_match = re.search(r'"score"\s*:\s*(\d+)', text)
    confidence_match = re.search(r'"confidence"\s*:\s*"(low|medium|high)"', text)
    if score_match:
        score = int(score_match.group(1))
        if 1 <= score <= 10:
            return {
                "score": score,
                "confidence": confidence_match.group(1) if confidence_match else None,
                "_recovery_note": "score extracted via regex; full structure not parseable",
            }, "recovered_regex"

    # Refusal extraction
    if re.search(r'"refusal"\s*:\s*true', text):
        return {"refusal": True, "reason": "(unrecoverable from malformed output)"}, "recovered_refusal"

    return None, "unrecovered"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("run_dir", type=Path)
    args = parser.parse_args()

    in_path = args.run_dir / "scores.jsonl"
    out_path = args.run_dir / "scores.recovered.jsonl"

    if not in_path.exists():
        print(f"ERROR: {in_path} not found", file=sys.stderr)
        sys.exit(2)

    n_total = 0
    n_recovered = 0
    n_unrecovered = 0
    recovery_modes = {}

    with in_path.open() as fin, out_path.open("w") as fout:
        for line in fin:
            r = json.loads(line)
            n_total += 1
            if r["status"] == "parse_error":
                content = r.get("raw_content", "") or ""
                obj, mode = try_recover_score(content)
                recovery_modes[mode] = recovery_modes.get(mode, 0) + 1
                if obj is not None and "score" in obj:
                    r["parsed"] = obj
                    r["status"] = "recovered"
                    r["recovery_mode"] = mode
                    n_recovered += 1
                else:
                    r["recovery_mode"] = mode
                    n_unrecovered += 1
            else:
                r["recovery_mode"] = "untouched"
            fout.write(json.dumps(r) + "\n")

    print(f"Total records: {n_total}")
    print(f"Recovered: {n_recovered}")
    print(f"Unrecovered: {n_unrecovered}")
    print(f"Modes: {recovery_modes}")
    print(f"Wrote: {out_path}")


if __name__ == "__main__":
    main()
