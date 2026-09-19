"""Independently inventory original instructional pages and validate imported lessons.

Run with the bundled Python runtime (PyMuPDF is required). Counts below detect
missing material; passing them does not establish mathematical or visual fidelity.
Source locations stay in internal audit output, never learner-facing content.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import pymupdf


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = Path("G:/My Drive/Music - Videos - Photos - Audiobooks/AudioBooks Books/C F A")
BOOK_RANGES = {1: (1, 26), 2: (27, 46), 3: (47, 75), 4: (76, 93)}
REFERENCE_RANGES = {1: (283, 294), 2: (363, 368), 3: (228, 233), 4: (210, 211)}
LAST_READING_END = {1: 281, 2: 361, 3: 226, 4: 209}
MODULE_RE = re.compile(r"\bMODULE\s+(\d+\.\d+):")
LOS_RE = re.compile(r"\bLOS\s+(\d+\.[a-z]+)\b")
PUBLISHER_REFERENCE = re.compile(
    r"\b(?:Schweser(?:Notes)?|Kaplan|QBank)\b|schweser\.com|"
    r"\b(?:Book\s+[1-4]|PDF\s+page|source map|verification scope)\b",
    re.IGNORECASE,
)


def words(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9]+(?:['-][A-Za-z0-9]+)*", text))


def quiz_inventory(text: str) -> list[dict]:
    result = []
    boundaries = list(re.finditer(
        r"(?m)^\s*(MODULE QUIZ\s+[\d.,– -]+|MODULE\s+\d+\.\d+:|KEY CONCEPTS|ANSWER KEY FOR MODULE QUIZZES)",
        text,
    ))
    for index, match in enumerate(boundaries):
        if not match.group(1).startswith("MODULE QUIZ"):
            continue
        end = boundaries[index + 1].start() if index + 1 < len(boundaries) else len(text)
        content = text[match.end():end]
        result.append({
            "heading": re.sub(r"\s+", " ", match.group(1)).strip(),
            "questionNumbers": re.findall(r"(?m)^\s*(\d+)\.\s", content),
        })
    return result


def page_inventory(page: pymupdf.Page) -> dict:
    text = page.get_text()
    images = []
    for image in page.get_image_info(xrefs=True):
        rect = pymupdf.Rect(image["bbox"])
        # This exact small repeated professor-note icon is decorative. Do not
        # classify arbitrary small images as icons: they may be inline equations.
        note_icon = image["width"] == 46 and image["height"] == 31 and 29 <= rect.width <= 31
        quiz_icon = image["width"] == 25 and image["height"] == 30 and 18 <= rect.width <= 20
        decorative = note_icon or quiz_icon
        images.append({
            "xref": image["xref"],
            "bbox": [round(v, 3) for v in image["bbox"]],
            "width": image["width"],
            "height": image["height"],
            "decorative": decorative,
        })
    return {
        "page": page.number + 1,
        "textWords": words(text),
        "textBlocks": len([b for b in page.get_text("blocks") if b[6] == 0]),
        "images": images,
        "vectorDrawingGroups": len(page.get_drawings()),
    }


def source_inventory(source_dir: Path, curriculum: list[dict]) -> dict:
    readings = []
    references = []
    excluded_topic_pages = []
    files = []
    for book, (first, last) in BOOK_RANGES.items():
        candidates = list(source_dir.glob(f"SchweserNotesTM 2026 CFA*Level 1 Book {book} *.pdf"))
        if len(candidates) != 1:
            raise ValueError(f"Expected one original PDF for source {book}; found {len(candidates)}.")
        with pymupdf.open(candidates[0]) as document:
            texts = [page.get_text() for page in document]
            # After front matter, actual chapter heading is at the beginning of
            # the page. Chapters 83 and 84 have a heading-only first page.
            starts = {}
            for index, text in enumerate(texts):
                match = re.match(r"\s*READING\s+(\d+)\s*\n", text)
                if index >= 10 and match and first <= int(match.group(1)) <= last:
                    starts[int(match.group(1))] = index + 1
            if sorted(starts) != list(range(first, last + 1)):
                raise ValueError(f"Chapter boundaries incomplete for source {book}: {sorted(starts)}")
            files.append({"source": book, "pages": len(document), "filename": candidates[0].name})
            for reading_id in range(first, last + 1):
                start = starts[reading_id]
                end = starts[reading_id + 1] - 1 if reading_id < last else LAST_READING_END[book]
                page_numbers = []
                for number in range(start, end + 1):
                    if re.match(r"\s*TOPIC QUIZ:", texts[number - 1], re.IGNORECASE):
                        excluded_topic_pages.append({"source": book, "page": number})
                    else:
                        page_numbers.append(number)
                combined = "\n".join(texts[n - 1] for n in page_numbers)
                title = next(r["title"] for r in curriculum if r["number"] == reading_id)
                pages = [page_inventory(document[n - 1]) for n in page_numbers]
                readings.append({
                    "readingId": reading_id,
                    "title": title,
                    "source": book,
                    "startPage": start,
                    "endPage": end,
                    "pages": pages,
                    "textWords": words(combined),
                    "moduleIds": sorted(set(MODULE_RE.findall(combined))),
                    "objectiveIds": sorted(set(LOS_RE.findall(combined))),
                    "exampleHeadings": re.findall(r"(?m)^\s*EXAMPLE:\s*([^\n]+)", combined),
                    "figureHeadings": re.findall(r"(?m)^\s*Figure\s+(\d+\.\d+):\s*([^\n]+)", combined),
                    "quizzes": quiz_inventory(combined),
                    "hasKeyConcepts": "KEY CONCEPTS" in combined,
                    "hasAnswerKey": "ANSWER KEY FOR MODULE QUIZZES" in combined,
                    "nonDecorativeImageOccurrences": sum(not i["decorative"] for p in pages for i in p["images"]),
                    "decorativeImageOccurrences": sum(i["decorative"] for p in pages for i in p["images"]),
                    "publisherReferenceMatches": len(PUBLISHER_REFERENCE.findall(combined)),
                })
            lo, hi = REFERENCE_RANGES[book]
            references.append({"source": book, "startPage": lo, "endPage": hi,
                               "pages": [page_inventory(document[n - 1]) for n in range(lo, hi + 1)]})
    return {"method": "Independent original-PDF page/marker/image inventory; not a claim of semantic or visual completeness.",
            "files": files, "readings": readings, "references": references,
            "excludedExternalTopicQuizPages": excluded_topic_pages}


def collect_blocks(reading: dict) -> list[dict]:
    blocks = list(reading.get("introduction", []))
    for module in reading.get("modules", []):
        blocks.extend(module.get("blocks", []))
    blocks.extend(reading.get("review", []))
    blocks.extend(reading.get("practice", []))
    for quiz_set in reading.get("quizSets", []):
        for question in quiz_set.get("questions", []):
            blocks.extend(question.get("supportingBlocks", []))
            blocks.extend(question.get("solutionBlocks", []))
    return blocks


def validate_content(inventory: dict, content_dir: Path, failures: list[str], warnings: list[str]) -> dict:
    counts = {"readings": 0, "blocks": 0, "images": 0, "textWords": 0}
    verified_assets = set()
    audit_file = ROOT / "docs/full-reading-import-audit.json"
    audit = json.loads(audit_file.read_text(encoding="utf-8")) if audit_file.exists() else None
    if audit is None:
        failures.append("Missing per-source-block import audit")
    for expected in inventory["readings"]:
        number = expected["readingId"]
        prefix = f"Reading {number}"
        path = content_dir / "readings" / f"{number:03d}.json"
        if not path.exists():
            failures.append(f"{prefix}: missing {path.relative_to(ROOT)}")
            continue
        actual = json.loads(path.read_text(encoding="utf-8"))
        counts["readings"] += 1
        if actual.get("readingId") != number:
            failures.append(f"{prefix}: wrong readingId")
        actual_module_ids = [m.get("id") for m in actual.get("modules", [])]
        if sorted(actual_module_ids) != expected["moduleIds"]:
            failures.append(f"{prefix}: module IDs {actual_module_ids} != {expected['moduleIds']}")
        blocks = collect_blocks(actual)
        counts["blocks"] += len(blocks)
        text = "\n".join(str(b.get("text", "")) for b in blocks)
        counts["textWords"] += words(text)
        objective_ids = {objective.get("id") for objective in actual.get("objectives", [])}
        missing_objectives = set(expected["objectiveIds"]) - objective_ids
        if missing_objectives:
            failures.append(f"{prefix}: missing objective markers {sorted(missing_objectives)}")
        actual_examples = len(re.findall(r"\b(?:EXAMPLE|Worked example):", text, re.IGNORECASE))
        if actual_examples < len(expected["exampleHeadings"]):
            failures.append(f"{prefix}: {actual_examples} example markers vs {len(expected['exampleHeadings'])} originals")
        figure_ids = set(re.findall(r"\bFigure\s+(\d+\.\d+):", text))
        missing_figures = {f[0] for f in expected["figureHeadings"]} - figure_ids
        if missing_figures:
            failures.append(f"{prefix}: missing figure captions {sorted(missing_figures)}")
        if PUBLISHER_REFERENCE.search(text):
            failures.append(f"{prefix}: learner content retains publisher/book/source references")
        actual_quizzes = [{
            "heading": quiz_set.get("title", "").replace("Knowledge check", "MODULE QUIZ", 1),
            "questionNumbers": [str(question.get("number")) for question in quiz_set.get("questions", [])],
        } for quiz_set in actual.get("quizSets", [])]
        if actual_quizzes != expected["quizzes"]:
            failures.append(f"{prefix}: numbered module-quiz questions differ from the original inventory")
        images = [b for b in blocks if b.get("type") in {"image", "math"}]
        counts["images"] += len(images)
        if audit:
            statistics = audit.get("readings", {}).get(str(number), {})
            missing_pages = {p["page"] for p in expected["pages"]} - set(statistics.get("sourcePages", []))
            if missing_pages:
                failures.append(f"{prefix}: import audit misses original instructional pages {sorted(missing_pages)}")
            if statistics.get("importedImageOccurrences") != expected["nonDecorativeImageOccurrences"]:
                failures.append(f"{prefix}: imported source image count does not match independent inventory")
            if statistics.get("decorativeImages") != expected["decorativeImageOccurrences"]:
                failures.append(f"{prefix}: decorative exclusions do not match independently identified icons")
            records = [b for b in audit.get("blocks", []) if b.get("readingId") == number]
            source_ids = [b.get("sourceId") for b in records]
            if len(source_ids) != len(set(source_ids)):
                failures.append(f"{prefix}: duplicate source block dispositions")
            expected_ids = {f"{expected['source']}:{p['page']}:{index}" for p in expected["pages"]
                            for index in range(p["textBlocks"] + len(p["images"]))}
            missing_ids = expected_ids - set(source_ids)
            if missing_ids:
                failures.append(f"{prefix}: {len(missing_ids)} original blocks have no import disposition")
            assets = {Path(b.get("src") or b.get("sourceAsset", "")).name for b in images}
            rebuilt = {item["asset"] for item in json.loads((ROOT / "docs/math-visual-classification.json").read_text(encoding="utf-8"))["assets"] if item["classification"] == "rebuilt-table"}
            assets.update(rebuilt)
            for record in records:
                if record.get("kind") == "image" and record.get("action") == "imported" and record.get("asset") not in assets:
                    failures.append(f"{prefix}: image {record.get('sourceId')} is marked imported but has no emitted asset")
        elif len(images) < expected["nonDecorativeImageOccurrences"]:
            warnings.append(f"{prefix}: {len(images)} image blocks vs {expected['nonDecorativeImageOccurrences']} original nondecorative occurrences; verify merged figures in block audit")
        if not actual.get("review") and expected["hasKeyConcepts"]:
            failures.append(f"{prefix}: missing review content")
        if not actual.get("practice") and not actual.get("quizSets") and expected["quizzes"]:
            warnings.append(f"{prefix}: practice field empty; verify quizzes retained in module blocks")
        for block in blocks:
            kind = block.get("type")
            if kind not in {"paragraph", "heading", "question", "image", "math"}:
                failures.append(f"{prefix}: unsupported block type {kind!r}")
            if kind not in {"image", "math"}:
                if not str(block.get("text", "")).strip():
                    failures.append(f"{prefix}: empty {kind} block")
                continue
            src = block.get("src", "") if kind == "image" else f"content/figures/{block.get('sourceAsset', '')}"
            if not re.match(r"^/?content/figures/[^/]+\.(?:png|webp|jpe?g)$", src) or ".." in Path(src).parts:
                failures.append(f"{prefix}: invalid image path {src}")
                continue
            asset = ROOT / "public" / src.lstrip("/")
            if asset in verified_assets:
                continue
            verified_assets.add(asset)
            if not asset.is_file() or not asset.stat().st_size:
                failures.append(f"{prefix}: missing image asset {src}")
            else:
                try:
                    pixmap = pymupdf.Pixmap(str(asset))
                    if not pixmap.width or not pixmap.height:
                        failures.append(f"{prefix}: zero-size image {src}")
                except Exception as error:
                    failures.append(f"{prefix}: cannot decode image {src}: {error}")
    reference_file = content_dir / "reference.json"
    if not reference_file.exists():
        failures.append("Missing instructional formula/appendix reference library")
    else:
        reference = json.loads(reference_file.read_text(encoding="utf-8"))
        if not reference.get("sections"):
            failures.append("Reference library has no sections")
        reference_text = "\n".join(b.get("text", "") for s in reference.get("sections", []) for b in s.get("blocks", []))
        if PUBLISHER_REFERENCE.search(reference_text):
            failures.append("Reference library retains publisher/book/source references")
        if audit:
            records = [b for b in audit.get("blocks", []) if b.get("readingId") is None]
            source_ids = [b.get("sourceId") for b in records]
            expected_ids = {f"{section['source']}:{p['page']}:{index}" for section in inventory["references"]
                            for p in section["pages"] for index in range(p["textBlocks"] + len(p["images"]))}
            if expected_ids - set(source_ids):
                failures.append("Reference library has original instructional blocks without an import disposition")
            if len(source_ids) != len(set(source_ids)):
                failures.append("Reference library has duplicate source block dispositions")
            assets = {Path(b.get("src") or b.get("sourceAsset", "")).name for s in reference["sections"] for b in s["blocks"] if b.get("type") in {"image", "math"}}
            for record in records:
                if record.get("kind") == "image" and record.get("action") == "imported" and record.get("asset") not in assets:
                    failures.append(f"Reference image {record.get('sourceId')} is marked imported but has no emitted asset")
    return counts


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--content-dir", type=Path, default=ROOT / "public/content")
    parser.add_argument("--inventory", type=Path, default=ROOT / "work/full-reading-source-inventory.json")
    parser.add_argument("--inventory-only", action="store_true")
    parser.add_argument("--reuse-inventory", action="store_true")
    args = parser.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    curriculum = json.loads((ROOT / "src/data/curriculum.json").read_text(encoding="utf-8"))
    if args.reuse_inventory:
        inventory = json.loads(args.inventory.read_text(encoding="utf-8"))
    else:
        inventory = source_inventory(args.source_dir, curriculum)
        args.inventory.parent.mkdir(parents=True, exist_ok=True)
        args.inventory.write_text(json.dumps(inventory, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    totals = {"readings": len(inventory["readings"]),
              "instructionalPages": sum(len(r["pages"]) for r in inventory["readings"]),
              "referencePages": sum(len(r["pages"]) for r in inventory["references"]),
              "moduleIds": sum(len(r["moduleIds"]) for r in inventory["readings"]),
              "objectiveIds": sum(len(r["objectiveIds"]) for r in inventory["readings"]),
              "exampleHeadings": sum(len(r["exampleHeadings"]) for r in inventory["readings"]),
              "figureHeadings": sum(len(r["figureHeadings"]) for r in inventory["readings"]),
              "quizQuestionStarts": sum(len(q["questionNumbers"]) for r in inventory["readings"] for q in r["quizzes"]),
              "nonDecorativeImageOccurrences": sum(r["nonDecorativeImageOccurrences"] for r in inventory["readings"])}
    print(json.dumps({"sourceInventory": totals}, indent=2))
    if args.inventory_only:
        return
    failures, warnings = [], []
    actual = validate_content(inventory, args.content_dir, failures, warnings)
    report = {"sourceInventory": totals, "importedContent": actual, "failures": failures, "warnings": warnings,
              "limitation": "Marker and file checks do not establish equation correctness, reading order, image/text alignment, or knowledge completeness. Reconcile the import block audit and visually inspect original-to-app examples."}
    output = ROOT / "work/full-reading-validation.json"
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"importedContent": actual, "failures": failures, "warnings": warnings}, indent=2))
    raise SystemExit(1 if failures else 0)


if __name__ == "__main__":
    main()
