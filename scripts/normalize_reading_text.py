"""Normalize spacing, paragraph splits, and list formatting across all readings.

Fixes:
1. Mid-sentence paragraph splits where sentences were divided across adjacent blocks.
2. Glued list items, steps, and subheadings within paragraph text (e.g. \n or mid-paragraph markers).
3. Spacing anomalies (multiple spaces, irregular bullet spacing, trailing hyphens).
"""
from __future__ import annotations

import glob
import json
import re
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
READINGS_DIR = ROOT / "public/content/readings"
REFERENCE_FILE = ROOT / "public/content/reference.json"

TERMINAL_PUNCT = ('.', '?', '!', ':', ';', '"', '”', '’', ')')
LIST_START_RE = re.compile(
    r'^(?:[0-9]+\.|[A-Z]\.|[a-z]\.|[▪■●•–]\s|\bStep\s+\d+:|\bExample:|\bQuestion:|\bAnswer:|\bStudy note:?)',
    re.I,
)
CONNECTOR_RE = re.compile(
    r'\b(and|or|the|a|an|of|in|to|for|with|on|at|by|from|that|which|is|are|was|were|be|been|as|than|into|through|between|including|relative to|such as)\s*$',
    re.I,
)
PHASE_HEADINGS = ('Trough:', 'Expansion:', 'Peak:', 'Contraction/recession:', 'Contraction:')


def clean_text_spacing(text: str) -> str:
    text = text.replace('\u00a0', ' ').replace('\u200b', '')
    text = re.sub(r'[^\S\r\n]{2,}', ' ', text)
    text = re.sub(r'^(–|•|▪|■|●)\s+', r'\1 ', text)
    return text.strip()


def split_embedded_patterns(text: str) -> list[str]:
    text = clean_text_spacing(text)

    # Glued phase headers: e.g. "...rate. Expansion:"
    text = re.sub(r'(?<=[.?!;])\s+(Trough:|Expansion:|Peak:|Contraction(?:/recession)?:)', r'\n\1', text)

    # Glued numbered items: e.g. "...late in expansions. 3. Speculative"
    text = re.sub(r'(?<=[.?!;])\s+(\d+\.\s+[A-Z])', r'\n\1', text)

    # Glued steps: e.g. "...first step. Step 2: Survey..."
    text = re.sub(r'(?<=[.?!;])\s+(Step\s+\d+:\s+)', r'\n\1', text, flags=re.I)

    # Glued bullets: e.g. "...rate increases. –  The unemployment..."
    text = re.sub(r'(?<=[.?!;])\s+([–•▪■●]\s+)', r'\n\1', text)

    # Bullet followed by another bullet on the same line:
    text = re.sub(r'([^\s])\s+([–•▪■●]\s+)', r'\1\n\2', text)

    lines = [clean_text_spacing(line) for line in text.split('\n') if clean_text_spacing(line)]
    return lines


def should_merge_paragraphs(p1_text: str, p2_text: str) -> tuple[bool, str]:
    t1 = p1_text.strip()
    t2 = p2_text.strip()
    if not t1 or not t2:
        return False, "empty"

    if LIST_START_RE.match(t2):
        return False, "t2_is_list"

    if t1 in PHASE_HEADINGS or t2 in PHASE_HEADINGS:
        return False, "is_phase_heading"

    # Case 1: t1 ends with hyphen or en-dash
    if t1.endswith('-') or t1.endswith('–'):
        return True, "ends_hyphen"

    # Case 2: t2 starts with lowercase
    if re.match(r'^[a-z]', t2):
        return True, "t2_starts_lower"

    # Case 3: t2 starts with closing punctuation, or math equality/operator
    if re.match(r'^[),;:\]=<>]', t2):
        return True, "t2_starts_punct_or_math"

    # Case 4: t1 ends with a dangling connector/preposition/conjunction and no terminal punct
    if not t1.endswith(TERMINAL_PUNCT):
        if CONNECTOR_RE.search(t1):
            return True, "ends_connector"

    # Case 5: t1 ends with a comma
    if t1.endswith(','):
        return True, "ends_comma"

    # Case 6: Special source splits without terminal punctuation
    if not t1.endswith(TERMINAL_PUNCT):
        if re.search(r'\b(Professional Conduct|CFA|expand|cost|is H0: μ =|Level I CFA curriculum:¹)\s*$', t1):
            return True, "specific_known_split"

    return False, "no"


def merge_two_texts(t1: str, t2: str, reason: str) -> str:
    t1 = t1.strip()
    t2 = t2.strip()
    if reason == "ends_hyphen":
        if t1.endswith('-'):
            return t1 + t2
        elif t1.endswith('–'):
            return t1[:-1] + '-' + t2
    if re.match(r'^[),;:\]]', t2):
        return t1 + t2
    return t1 + ' ' + t2


def process_block_list(blocks: list[dict]) -> list[dict]:
    expanded = []
    for b in blocks:
        if b.get('type') == 'paragraph':
            text = b.get('text', '')
            pieces = split_embedded_patterns(text)
            if len(pieces) > 1:
                for piece in pieces:
                    expanded.append({'type': 'paragraph', 'text': piece})
            else:
                b_copy = deepcopy(b)
                b_copy['text'] = clean_text_spacing(text)
                expanded.append(b_copy)
        else:
            expanded.append(deepcopy(b))

    merged = []
    i = 0
    while i < len(expanded):
        curr = expanded[i]
        if curr.get('type') == 'paragraph':
            while i + 1 < len(expanded) and expanded[i + 1].get('type') == 'paragraph':
                next_b = expanded[i + 1]
                should, reason = should_merge_paragraphs(curr['text'], next_b['text'])
                if should:
                    curr['text'] = merge_two_texts(curr['text'], next_b['text'], reason)
                    curr['text'] = clean_text_spacing(curr['text'])
                    i += 1
                else:
                    break
            merged.append(curr)
        else:
            merged.append(curr)
        i += 1

    return merged


def process_reading_file(file_path: Path) -> dict:
    data = json.loads(file_path.read_text(encoding="utf-8"))

    if 'introduction' in data:
        data['introduction'] = process_block_list(data['introduction'])
    for m in data.get('modules', []):
        m['blocks'] = process_block_list(m['blocks'])
    if 'review' in data:
        data['review'] = process_block_list(data['review'])

    for qs in data.get('quizSets', []):
        for q in qs.get('questions', []):
            if 'prompt' in q:
                q['prompt'] = clean_text_spacing(q['prompt'])
            if 'explanation' in q:
                q['explanation'] = clean_text_spacing(q['explanation'])
            if 'supportingBlocks' in q:
                q['supportingBlocks'] = process_block_list(q['supportingBlocks'])
            if 'solutionBlocks' in q:
                q['solutionBlocks'] = process_block_list(q['solutionBlocks'])

    return data


def main() -> None:
    reading_files = sorted(READINGS_DIR.glob("*.json"))
    print(f"Normalizing spacing and text across {len(reading_files)} readings...")
    for rf in reading_files:
        cleaned = process_reading_file(rf)
        rf.write_text(json.dumps(cleaned, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    if REFERENCE_FILE.exists():
        ref_data = json.loads(REFERENCE_FILE.read_text(encoding="utf-8"))
        for s in ref_data.get('sections', []):
            s['blocks'] = process_block_list(s.get('blocks', []))
        REFERENCE_FILE.write_text(json.dumps(ref_data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print("Completed normalization of all readings and reference library.")


if __name__ == "__main__":
    main()
