"""Turn imported reading JSON into learner-facing questions and interactive quizzes.

This is a deterministic post-processing step. Source objective identifiers remain
in structured metadata for validation, but are removed from learner-facing copy.
"""
from __future__ import annotations

import json
import re
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
READINGS = ROOT / "public/content/readings"
OBJECTIVE_HEADING = re.compile(r"^LOS\s+(\d+\.[a-z]+)(?::\s*(.*))?$", re.S)
OBJECTIVE_TAG = re.compile(r"\s*\(LOS\s+[\d.a-z, ]+\)")
QUESTION_START = re.compile(r"(?m)^\s*(\d+)\.\s+")
OPTION_START = re.compile(r"(?m)^\s*([A-C])[.)]\s*")
ANSWER_START = re.compile(r"^\s*(\d+)\.\s*([A-C])(?:[.\s]|$)", re.S)
SOURCE_NOTE_START = re.compile(
    r"^\s*\d+\s+(?:[A-Z�]|Copyright|Reproduced|Republished|Reprinted|Source:|Ibid|Definition per)",
)


VISUAL_OPTION_OVERRIDES = {
    "e85d519d312de160b985.png": [
        ("A", "Report the goodwill, but not the patent."),
        ("B", "Report the patent, but not the goodwill."),
        ("C", "Report neither the goodwill nor the patent."),
    ],
    "39c347fbb135ee9a1dc6.png": [
        ("A", "Liquidity: current ratio; solvency: quick ratio."),
        ("B", "Liquidity: debt-to-equity ratio; solvency: financial leverage ratio."),
        ("C", "Liquidity: cash ratio; solvency: total debt ratio."),
    ],
    "0b5060743d1bd04ba9ed.png": [
        ("A", "Inventory turnover: 2.00 times; total asset turnover: 7.00 times."),
        ("B", "Inventory turnover: 7.00 times; total asset turnover: 2.00 times."),
        ("C", "Inventory turnover: 0.33 times; total asset turnover: 0.50 times."),
    ],
    "a00fc35837198e75350f.png": [
        ("A", "Receivables turnover: 2.1 times; average collection period: 174 days."),
        ("B", "Receivables turnover: 3.3 times; average collection period: 111 days."),
        ("C", "Receivables turnover: 4.0 times; average collection period: 91 days."),
    ],
    "2b641346ef3eb9bf30f1.png": [
        ("A", "Portfolio A: expected return 7%; expected standard deviation 14%."),
        ("B", "Portfolio B: expected return 9%; expected standard deviation 26%."),
        ("C", "Portfolio C: expected return 12%; expected standard deviation 22%."),
    ],
    "b8a7edef2c13faf0422f.png": [
        ("A", "Expected return 6.0%; standard deviation 6.8%."),
        ("B", "Expected return 8.0%; standard deviation 4.8%."),
        ("C", "Expected return 10.0%; standard deviation 6.6%."),
    ],
}


def learner_question(statement: str, objective_id: str) -> str:
    statement = re.sub(r"\s+", " ", statement).strip().rstrip(".")
    if objective_id == "8.c":
        return "How do parametric and nonparametric tests differ, and when should we use each one?"
    patterns = [
        ("Compare and contrast ", "How do we compare and contrast "),
        ("Calculate ", "How do we calculate "),
        ("Describe ", "What should we know about "),
        ("Explain ", "How can we explain "),
        ("Define ", "How do we define "),
        ("Compare ", "How can we compare "),
        ("Contrast ", "How can we distinguish "),
        ("Identify ", "How can we identify "),
        ("Evaluate ", "How should we evaluate "),
        ("Analyze ", "How do we analyze "),
        ("Determine ", "How do we determine "),
        ("Demonstrate ", "How can we demonstrate "),
        ("Interpret ", "How should we interpret "),
        ("Formulate ", "How do we formulate "),
        ("Construct ", "How do we construct "),
        ("Discuss ", "What should we understand about "),
        ("Recommend ", "How should we recommend "),
    ]
    for start, replacement in patterns:
        if statement.startswith(start):
            return replacement + statement[len(start):].lower()[0:1] + statement[len(start):][1:] + "?"
    return "What should we understand about " + statement[0].lower() + statement[1:] + "?"


def clean_visible_text(text: str) -> str:
    text = re.sub(
        r"\s+\d+\s+(?:Copyright|Reproduced|Republished|Source:)\b.*$",
        "",
        text,
        flags=re.I | re.S,
    )
    if SOURCE_NOTE_START.match(text) or re.match(
        r"^\s*(?:\d+\s*)?(?:Copyright|Reproduced|Republished|Source:|Ibid\.?|with permission\b|permission from\b|All rights reserved\b|Handbook,\s*\d+)",
        text,
        flags=re.I,
    ):
        return ""
    text = re.sub(
        r"\s*These Standards and their application are described in the Standards of Practice Handbook[^.]*\.",
        "",
        text,
        flags=re.I,
    )
    text = OBJECTIVE_TAG.sub("", text)
    text = re.sub(r"\s*\((?:Module\s+[\d.]+,\s*)?LOS(?:\s+[\d.a-z,]+|\s*)?(?:\)|$)", "", text, flags=re.I)
    text = re.sub(r"\s*(?:Module\s+[\d.]+,\s*)?LOS\s+[\d.a-z]+(?:,\s*LOS\s+[\d.a-z]+)*\)?", "", text, flags=re.I)
    text = re.sub(r"^\s*\(?(?:Module\s+[\d.]+,?)?\s*$", "", text, flags=re.I)
    text = re.sub(r"^\s*\d+\.[a-z]+\)?\s*$", "", text, flags=re.I)
    text = re.sub(r"\bThe LOS requires us to\b", "This lesson asks us to", text, flags=re.I)
    text = re.sub(r"\b(?:this|the|next) LOS\b", "this lesson", text, flags=re.I)
    text = re.sub(r"\bIn this lesson, the curriculum\b", "In this lesson, we", text, flags=re.I)
    return re.sub(r"[ \t]+\n", "\n", text).strip()


def strip_source_notes(blocks: list[dict]) -> list[dict]:
    """Discard trailing citation/permission footnotes from a learner-facing block list."""
    result = []
    for block in blocks:
        if SOURCE_NOTE_START.match(block.get("text", "")):
            break
        result.append(block)
    return result


def objective_map() -> dict[str, dict]:
    source = json.loads((ROOT / "src/data/sourceManifest.json").read_text(encoding="utf-8"))
    result = {}
    for module in source:
        for objective in module["objectives"]:
            result[objective["id"]] = {
                "id": objective["id"],
                "statement": objective["sourceStatement"],
                "question": learner_question(objective["sourceStatement"], objective["id"]),
            }
    return result


def visible_block(block: dict, objectives: dict[str, dict]) -> dict | None:
    item = deepcopy(block)
    text = item.get("text", "")
    match = OBJECTIVE_HEADING.match(text.strip()) if text else None
    if match:
        objective_id = match.group(1)
        item = {
            "type": "question",
            "objectiveId": objective_id,
            "text": objectives[objective_id]["question"],
        }
    elif text:
        item["text"] = clean_visible_text(text)
        if not item["text"]:
            return None
    if item.get("alt"):
        item["alt"] = clean_visible_text(item["alt"])
    return item


def question_groups(blocks: list[dict]) -> tuple[list[dict], list[dict]]:
    lesson_blocks, groups = [], []
    active = None
    for block in blocks:
        if block.get("type") == "heading" and block.get("text", "").startswith("Practice "):
            if active:
                groups.append(active)
            active = {"title": block["text"], "blocks": []}
            continue
        if active is None:
            lesson_blocks.append(block)
        else:
            active["blocks"].append(block)
    if active:
        groups.append(active)
    return lesson_blocks, groups


def split_questions(group: dict) -> list[dict]:
    entries: list[dict] = []
    current = None
    preamble: list[dict] = []
    collecting_preamble = False
    for block in group["blocks"]:
        text = block.get("text", "")
        starts = list(QUESTION_START.finditer(text))
        if starts:
            for index, match in enumerate(starts):
                if current:
                    entries.append(current)
                current = {
                    "number": int(match.group(1)),
                    "blocks": preamble,
                    "textParts": [text[match.end():starts[index + 1].start() if index + 1 < len(starts) else len(text)]],
                }
                preamble = []
                collecting_preamble = False
        elif block.get("type") == "heading" and re.search(r"\bUse .+Questions?\s+\d", text, re.I):
            item = deepcopy(block)
            item["_quizPreamble"] = True
            preamble = [item]
            collecting_preamble = True
        elif collecting_preamble:
            item = deepcopy(block)
            item["_quizPreamble"] = True
            preamble.append(item)
        elif current:
            current["blocks"].append(deepcopy(block))
            if text:
                current["textParts"].append(text)
        else:
            item = deepcopy(block)
            item["_quizPreamble"] = True
            preamble.append(item)
    if current:
        entries.append(current)
    return entries


def split_answers(blocks: list[dict]) -> list[dict]:
    answers, current, pending_number = [], None, None
    for block in blocks:
        text = block.get("text", "")
        match = ANSWER_START.match(text)
        number_only = re.fullmatch(r"\s*(\d+)\.\s*", text)
        if number_only:
            pending_number = int(number_only.group(1))
            continue
        if pending_number is not None and re.fullmatch(r"[A-C]", text.strip()):
            if current:
                answers.append(current)
            current = {
                "number": pending_number,
                "correctOptionId": text.strip(),
                "objectiveIds": [],
                "blocks": [],
            }
            pending_number = None
            continue
        if match:
            if current:
                answers.append(current)
            current = {
                "number": int(match.group(1)),
                "correctOptionId": match.group(2),
                "objectiveIds": re.findall(r"\bLOS\s+(\d+\.[a-z]+)", text),
                "blocks": [],
            }
            item = deepcopy(block)
            remainder = clean_visible_text(text[match.end():])
            if remainder or item.get("type") == "image":
                item["text"] = remainder
                current["blocks"].append(item)
        elif current:
            if block.get("type") == "heading" and text.startswith("Module Quiz"):
                continue
            current["objectiveIds"].extend(re.findall(r"\bLOS\s+(\d+\.[a-z]+)", text))
            item = deepcopy(block)
            if text:
                item["text"] = clean_visible_text(text)
            if item.get("text") or item.get("type") == "image":
                current["blocks"].append(item)
    if current:
        answers.append(current)
    return answers


def parse_options(entry: dict) -> tuple[str, list[dict], list[dict]]:
    text = "\n".join(part.strip() for part in entry["textParts"] if part.strip())
    matches = list(OPTION_START.finditer(text))
    visual = next((Path(b.get("src", "")).name for b in entry["blocks"] if Path(b.get("src", "")).name in VISUAL_OPTION_OVERRIDES), None)
    if visual:
        options = [{"id": option_id, "text": option_text} for option_id, option_text in VISUAL_OPTION_OVERRIDES[visual]]
        support = [b for b in entry["blocks"] if Path(b.get("src", "")).name != visual and (b.get("type") == "image" or b.get("_quizPreamble"))]
        for block in support:
            if block.pop("_quizPreamble", False) and block.get("type") == "image":
                block["visualKindHint"] = "table"
        return re.sub(r"\s+", " ", text).strip(), options, support
    if len(matches) != 3:
        raise ValueError(f"Question {entry['number']} has {len(matches)} options: {text[:180]}")
    prompt = re.sub(r"\s+", " ", text[:matches[0].start()]).strip()
    options = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        option_text = re.sub(r"\s+", " ", text[match.end():end]).strip()
        options.append({"id": match.group(1), "text": option_text})
    support = [b for b in entry["blocks"] if b.get("type") == "image" or b.get("_quizPreamble")]
    for block in support:
        if block.pop("_quizPreamble", False) and block.get("type") == "image":
            block["visualKindHint"] = "table"
    return prompt, options, support


def solution_text(blocks: list[dict]) -> str:
    text = " ".join(block.get("text", "") for block in blocks if block.get("text"))
    return re.sub(r"\s+", " ", text).strip()


def enhance_reading(path: Path, objectives: dict[str, dict]) -> tuple[int, int]:
    reading = json.loads(path.read_text(encoding="utf-8"))
    quiz_groups = []
    for module in reading["modules"]:
        module["blocks"], groups = question_groups(module["blocks"])
        for group in groups:
            group["moduleId"] = module["id"]
            quiz_groups.append(group)
    answers = split_answers(reading.get("practice", []))
    raw_questions = [(group, entry) for group in quiz_groups for entry in split_questions(group)]
    if len(raw_questions) != len(answers):
        raise ValueError(f"Reading {reading['readingId']}: {len(raw_questions)} questions != {len(answers)} answers")

    quiz_sets, cursor = [], 0
    for set_index, group in enumerate(quiz_groups, 1):
        entries = split_questions(group)
        questions = []
        for entry in entries:
            answer = answers[cursor]
            cursor += 1
            prompt, options, supporting = parse_options(entry)
            objective_ids = list(dict.fromkeys(answer["objectiveIds"]))
            answer_blocks = strip_source_notes(answer["blocks"])
            explanation = solution_text(answer_blocks)
            question_id = f"r{reading['readingId']}-q{cursor}"
            questions.append({
                "id": question_id,
                "number": entry["number"],
                "objectiveIds": objective_ids,
                "prompt": prompt,
                "supportingBlocks": supporting,
                "options": options,
                "correctOptionId": answer["correctOptionId"],
                "explanation": explanation,
                "solutionBlocks": answer_blocks,
            })
        quiz_sets.append({
            "id": f"reading-{reading['readingId']}-quiz-{set_index}",
            "title": group["title"].replace("Practice", "Knowledge check", 1),
            "moduleId": group["moduleId"],
            "questions": questions,
        })

    reading["objectives"] = [
        objectives[objective_id]
        for objective_id in objectives
        if objective_id.startswith(f"{reading['readingId']}.")
    ]
    reading["quizSets"] = quiz_sets
    reading["practice"] = []
    reading["introduction"] = [b for block in reading.get("introduction", []) if (b := visible_block(block, objectives))]
    reading["review"] = [b for block in reading.get("review", []) if (b := visible_block(block, objectives))]
    for module in reading["modules"]:
        module["blocks"] = [b for block in module["blocks"] if (b := visible_block(block, objectives))]
    for quiz_set in reading["quizSets"]:
        for question in quiz_set["questions"]:
            question["supportingBlocks"] = [b for block in question["supportingBlocks"] if (b := visible_block(block, objectives))]
            question["solutionBlocks"] = [b for block in question["solutionBlocks"] if (b := visible_block(block, objectives))]
            question["explanation"] = clean_visible_text(question["explanation"])
    path.write_text(json.dumps(reading, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return len(reading["objectives"]), sum(len(item["questions"]) for item in quiz_sets)


def main() -> None:
    objectives = objective_map()
    objective_count = question_count = 0
    for path in sorted(READINGS.glob("*.json")):
        objectives_added, questions_added = enhance_reading(path, objectives)
        objective_count += objectives_added
        question_count += questions_added
    reference_path = ROOT / "public/content/reference.json"
    reference = json.loads(reference_path.read_text(encoding="utf-8"))
    for section in reference["sections"]:
        section["blocks"] = [b for block in section["blocks"] if (b := visible_block(block, objectives))]
    reference_path.write_text(json.dumps(reference, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if objective_count != 365 or question_count != 565:
        raise ValueError(f"Expected 365 objectives and 565 questions; produced {objective_count} and {question_count}")
    (ROOT / "src/data/objectiveQuestions.json").write_text(
        json.dumps(list(objectives.values()), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Enhanced 93 readings with {objective_count} learner questions and {question_count} interactive questions.")


if __name__ == "__main__":
    main()
