"""
List every test-mode note this writer has submitted and the evaluator scores for each.

uv run src/check_scores.py
uv run src/check_scores.py --json > scores.json

Pages through GET /2/notes/search/notes_written (test_mode=true) until there are no more
results, prints one block per note, then a count of score buckets per evaluator.
"""

import argparse
import json
import shutil
import subprocess
import sys
from collections import Counter, defaultdict
from typing import Dict, List

from cnapi.xurl_util import run_xurl
import dotenv


def get_all_test_notes_written() -> List[Dict]:
    notes: List[Dict] = []
    pagination_token = None
    while True:
        path = (
            "/2/notes/search/notes_written"
            "?test_mode=true"
            "&max_results=100"
            "&note.fields=id,info,status,test_result"
        )
        if pagination_token:
            path += f"&pagination_token={pagination_token}"
        resp = run_xurl(["xurl", path])
        notes.extend(resp.get("data", []))
        pagination_token = (resp.get("meta") or {}).get("next_token")
        if not pagination_token:
            return notes


def _evaluation_outcomes(note: Dict) -> List[Dict]:
    return (note.get("test_result") or {}).get("evaluation_outcome") or []


def print_report(notes: List[Dict]) -> None:
    print(f"{len(notes)} test-mode notes written\n")
    buckets: Dict[str, Counter] = defaultdict(Counter)
    for note in notes:
        info = note.get("info") or {}
        print(f"Note {note.get('id')}  post {info.get('post_id')}  status {note.get('status')}")
        print(f"  {info.get('text', '')}")
        outcomes = _evaluation_outcomes(note)
        if not outcomes:
            print("  (no evaluator results yet)")
        for outcome in outcomes:
            print(f"  {outcome['evaluator_type']}: {outcome['evaluator_score_bucket']}")
            buckets[outcome["evaluator_type"]][outcome["evaluator_score_bucket"]] += 1
        print()

    if buckets:
        print("Summary")
        for evaluator, counts in sorted(buckets.items()):
            print(f"  {evaluator}: " + ", ".join(f"{b}={n}" for b, n in counts.most_common()))
    pending = sum(1 for note in notes if not _evaluation_outcomes(note))
    if pending:
        print(f"  {pending} notes have no evaluator results yet")


if __name__ == "__main__":
    dotenv.load_dotenv()
    parser = argparse.ArgumentParser(description="Show evaluator scores for test-mode notes.")
    parser.add_argument("--json", action="store_true", help="Print the raw notes as JSON")
    args = parser.parse_args()
    if shutil.which("xurl") is None:
        sys.exit("xurl is not installed. See step 5 of the README: https://github.com/xdevplatform/xurl")
    try:
        notes = get_all_test_notes_written()
    except subprocess.CalledProcessError as e:
        sys.exit(
            "Could not fetch your notes. The X API said:\n"
            + ((e.stdout or "") + (e.stderr or "")).strip()
            + "\n\nCheck that xurl is logged in (`xurl auth status`) and that your account is "
            "enrolled as an AI Note Writer."
        )
    if args.json:
        print(json.dumps(notes, indent=2))
    else:
        print_report(notes)
