"""Import supplied instructional content as reflowable lessons, retaining visual math.

Requires PyMuPDF. Source paths are CLI inputs and never shipped to students.
Every source block has an internal disposition so omissions can be reviewed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

import pymupdf as fitz
from pdf_inline_regions import paragraph_regions

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "public/content"
READING = re.compile(r"^READING\s+(\d+)$")
MODULE = re.compile(r"^MODULE\s+(\d+\.\d+):\s*(.*)", re.S)
LAST_PAGES = {1: 281, 2: 361, 3: 226, 4: 209}
REFERENCE_PAGES = {1: (283, 294), 2: (363, 368), 3: (228, 233), 4: (210, 211)}
SUPERSCRIPTS = str.maketrans("0123456789+-=()n", "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ⁿ")
SOURCE_CORRECTIONS = [{
    "original": "The sample standard deviation can be interpreted as an unbiased estimator of the population standard deviation.",
    "replacement": "For independent, identically distributed observations with finite variance, the sample variance calculated with n − 1 in the denominator is an unbiased estimator of population variance. Taking its square root does not preserve unbiasedness: the sample standard deviation is generally downward biased as an estimator of population standard deviation.",
    "reason": "Corrected source error: unbiased sample variance does not imply unbiased sample standard deviation.",
}]


def clean(text: str) -> str:
    text = text.replace("\u00ad", "").replace("\u00a0", " ")
    for correction in SOURCE_CORRECTIONS:
        text = text.replace(correction["original"], correction["replacement"])
    if text.startswith("You should carefully read the Standards of Practice Handbook multiple times"):
        return "Study each standard, its guidance, recommended procedures, and examples. Revisit difficult cases and test whether you can explain why a proposed action complies with or violates a standard."
    text = re.sub(r"PROFESSOR[’']S NOTE", "Study note", text)
    text = re.sub(r"(?:our )?SchweserNotes[™®]?", "these lessons", text, flags=re.I)
    text = re.sub(r"Appendix section of this book", "statistical reference library", text, flags=re.I)
    text = re.sub(r"Appendix ([A-E]) of this book", r"the statistical reference library (table \1)", text, flags=re.I)
    text = re.sub(r"this book[’']s Appendix", "the statistical reference library", text, flags=re.I)
    text = re.sub(r"\bthe Appendix\b", "the statistical reference library", text, flags=re.I)
    text = re.sub(r"\bin this book\b", "in these lessons", text, flags=re.I)
    text = re.sub(r"\(Module\s+\d+\.\d+,\s*LOS\s+[\d.a-z, ]+\)", "", text)
    return text.strip()


def text_lines(block: dict) -> list[dict]:
    lines = []
    for line in block["lines"]:
        spans = line["spans"]
        text = "".join(s["text"].translate(SUPERSCRIPTS) if s["flags"] & 1 else s["text"] for s in spans)
        if text.strip():
            lines.append({"text": text, "bold": all(s["flags"] & 16 for s in spans if s["text"].strip()), "size": max(s["size"] for s in spans), "bbox": line["bbox"]})
    return lines


def join_lines(lines: list[dict]) -> str:
    result = ""
    for line in lines:
        text = line["text"].strip()
        separator = "\n" if re.match(r"^(?:[A-D][.)]|\d+\.|[▪■●•])\s", text) else " "
        # Keep lexical hyphens, including risk-free and time-weighted, at line wraps.
        result += ("" if result.endswith("-") else separator if result else "") + text
    return clean(result)


def groups(block: dict) -> list[list[dict]]:
    result: list[list[dict]] = []
    for line in text_lines(block):
        header = bool(re.match(r"^(?:READING \d+$|MODULE |LOS |EXAMPLE:|Answer:|KEY CONCEPTS|ANSWER KEY|PROFESSOR[’']S NOTE|Figure \d)", line["text"]))
        if not result or header or (line["bold"] != result[-1][-1]["bold"] and (line["bold"] or len(result[-1]) == 1)):
            result.append([line])
        else:
            result[-1].append(line)
    return result


def skip_reason(text: str) -> str | None:
    if re.search(r"(?:Schweser|Kaplan|Resource Library|Topic Quiz:|online Topic Quiz|online topic quiz|Topic Quiz online|Log in to your|log into your|logging in to your)", text, re.I):
        return "publisher service promotion"
    if "download a PDF of the Standards of Practice Handbook" in text:
        return "external handbook access instructions"
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", type=Path, default=Path("G:/My Drive/Music - Videos - Photos - Audiobooks/AudioBooks Books/C F A"))
    args = parser.parse_args()
    (OUTPUT / "readings").mkdir(parents=True, exist_ok=True)
    (OUTPUT / "figures").mkdir(parents=True, exist_ok=True)
    curriculum = json.loads((ROOT / "src/data/manifest.json").read_text(encoding="utf-8"))
    index = {r["number"]: r for r in curriculum}
    lessons = {}
    audit = {"sources": [], "readings": {}, "blocks": [], "referenceSections": []}
    reference = {"title": "Formula and statistical reference", "sections": []}
    image_cache = {}

    for book in range(1, 5):
        paths = list(args.source_dir.glob(f"*Level 1 Book {book}*.pdf"))
        if len(paths) != 1:
            raise ValueError(f"Expected one supplied volume {book}; found {len(paths)}")
        doc = fitz.open(paths[0])
        audit["sources"].append({"volume": book, "sha256": hashlib.sha256(paths[0].read_bytes()).hexdigest(), "pages": len(doc)})
        current = None
        target = None
        mode = "introduction"
        last_context = ""
        reference_section = None

        for page_index, page in enumerate(doc):
            page_num = page_index + 1
            ref_start, ref_end = REFERENCE_PAGES[book]
            in_reference = ref_start <= page_num <= ref_end
            if page_num > LAST_PAGES[book] and not in_reference:
                continue
            if in_reference and reference_section is None:
                titles = {1: "Quantitative methods, economics, corporate finance, and statistical tables", 2: "Financial analysis and equity valuation", 3: "Fixed income and derivatives", 4: "Portfolio management and performance"}
                reference_section = {"id": f"reference-{book}", "title": titles[book], "blocks": []}
                reference["sections"].append(reference_section)
            page_blocks = sorted(page.get_text("dict")["blocks"], key=lambda b: (round(b["bbox"][1], 1), b["bbox"][0]))
            inline_regions = paragraph_regions(page_blocks)
            merged_indices = {index for region in inline_regions.values() for index in region["indices"]}
            page_text = "\n".join("\n".join(l["text"] for l in text_lines(b)) for b in page_blocks if b["type"] == 0)
            # Chapter headings are large display type. Contents entries use smaller type.
            start_ids = []
            for block in page_blocks:
                if block["type"] != 0:
                    continue
                for line in text_lines(block):
                    match = READING.fullmatch(line["text"].strip())
                    if match and line["size"] > 18:
                        start_ids.append(int(match.group(1)))
            if start_ids and not in_reference:
                number = start_ids[0]
                if number not in index or number in lessons:
                    raise ValueError(f"Unexpected repeated chapter {number} on {book}:{page_num}")
                current = {"readingId": number, "title": index[number]["title"], "introduction": [], "modules": [], "review": [], "practice": []}
                lessons[number] = current
                audit["readings"][str(number)] = {"volume": book, "sourcePages": [], "rawTextBlocks": 0, "rawImageOccurrences": 0, "importedTextBlocks": 0, "importedImageOccurrences": 0, "omittedTextBlocks": 0, "decorativeImages": 0}
                target = current["introduction"]
                mode = "introduction"
            if current is None and not in_reference:
                continue
            if in_reference:
                target = reference_section["blocks"]
            if not in_reference:
                stats = audit["readings"][str(current["readingId"])]
                stats["sourcePages"].append(page_num)

            for block_index, block in enumerate(page_blocks):
                source_id = f"{book}:{page_num}:{block_index}"
                if block_index in inline_regions:
                    region = inline_regions[block_index]
                    rect = region["bbox"] + (-0.5, -0.5, 0.5, 0.5)
                    pixmap = page.get_pixmap(matrix=fitz.Matrix(2.5, 2.5), clip=rect, alpha=False)
                    digest = hashlib.sha256(pixmap.samples).hexdigest()[:20]
                    filename = f"{digest}.png"
                    if digest not in image_cache:
                        pixmap.save(OUTPUT / "figures" / filename)
                        image_cache[digest] = True
                    region_text = clean(region["text"])
                    target.append({"type": "image", "src": f"content/figures/{filename}", "text": region_text,
                                   "alt": f"Mathematical explanation with original notation: {region_text}",
                                   "width": round(rect.width * 1.3), "height": round(rect.height * 1.3)})
                    last_context = region_text
                    for merged_index in region["indices"]:
                        original = page_blocks[merged_index]
                        is_image = original["type"] == 1
                        audit["blocks"].append({"sourceId": f"{book}:{page_num}:{merged_index}",
                            "readingId": None if in_reference else current["readingId"],
                            "kind": "image" if is_image else "text", "action": "imported",
                            "reason": "preserved in combined inline-math region", "asset": filename,
                            "outputBlocks": 1 if merged_index == block_index else 0})
                        if not in_reference:
                            stats["rawImageOccurrences" if is_image else "rawTextBlocks"] += 1
                            stats["importedImageOccurrences" if is_image else "importedTextBlocks"] += 1
                    continue
                if block_index in merged_indices:
                    continue
                record = {"sourceId": source_id, "readingId": None if in_reference else current["readingId"], "kind": "image" if block["type"] == 1 else "text", "action": "imported"}
                audit["blocks"].append(record)
                if block["type"] == 1:
                    if not in_reference:
                        stats["rawImageOccurrences"] += 1
                    rect = fitz.Rect(block["bbox"])
                    # Repeated note icons carry no teaching information; retain every other image.
                    is_icon = (block["width"], block["height"]) in {(46, 31), (25, 30)}
                    if is_icon:
                        record.update(action="skipped", reason="decorative study-note or quiz icon")
                        if not in_reference:
                            stats["decorativeImages"] += 1
                        continue
                    pixmap = page.get_pixmap(matrix=fitz.Matrix(2.5, 2.5), clip=rect, alpha=False)
                    digest = hashlib.sha256(pixmap.samples).hexdigest()[:20]
                    filename = f"{digest}.png"
                    if digest not in image_cache:
                        # Render occurrence rather than copying bytes: preserves masks and original colors.
                        pixmap.save(OUTPUT / "figures" / filename)
                        image_cache[digest] = True
                    alt_context = re.sub(r"\s+", " ", last_context)[-180:]
                    target.append({"type": "image", "src": f"content/figures/{filename}", "alt": f"Equation, table, or diagram: {alt_context}" if alt_context else "Supporting equation, table, or diagram", "width": round(rect.width * 1.3), "height": round(rect.height * 1.3)})
                    record["asset"] = filename
                    if not in_reference:
                        stats["importedImageOccurrences"] += 1
                    continue

                if not in_reference:
                    stats["rawTextBlocks"] += 1
                emitted = 0
                skipped = []
                for group in groups(block):
                    text = join_lines(group)
                    if not text:
                        continue
                    raw_text = " ".join(l["text"] for l in group)
                    for correction in SOURCE_CORRECTIONS:
                        if correction["original"] in raw_text:
                            record.setdefault("corrections", []).append(correction)
                    if READING.fullmatch(raw_text.strip()) or (not in_reference and text.upper() == current["title"].upper()):
                        skipped.append("chapter title rendered by app")
                        continue
                    reason = skip_reason(text)
                    if reason:
                        skipped.append(reason)
                        record.setdefault("omittedText", []).append(text)
                        continue
                    module_match = MODULE.match(text)
                    if module_match and not in_reference:
                        module_id = module_match.group(1)
                        known = next((m for m in index[current["readingId"]]["modules"] if m["id"] == module_id), None)
                        if not known:
                            raise ValueError(f"Unknown module {module_id}")
                        module = {"id": module_id, "title": known["title"], "blocks": []}
                        current["modules"].append(module)
                        target = module["blocks"]
                        mode = "module"
                        emitted += 1
                        continue
                    if text == "KEY CONCEPTS" and not in_reference:
                        target = current["review"]
                        mode = "review"
                        emitted += 1
                        continue
                    if text.startswith("ANSWER KEY FOR MODULE QUIZ") and not in_reference:
                        target = current["practice"]
                        mode = "practice"
                        emitted += 1
                        continue
                    if text == "FORMULAS" or text == "APPENDIX":
                        skipped.append("reference heading rendered by app")
                        continue
                    is_heading = all(l["bold"] for l in group) and len(text) < 450
                    if re.match(r"^(?:LOS \d+\.[a-z]+:|EXAMPLE:|MODULE QUIZ|Study note$)", text):
                        is_heading = True
                    if text.startswith("EXAMPLE:"):
                        text = "Worked example: " + text[len("EXAMPLE:"):].strip()
                    if text.startswith("MODULE QUIZ"):
                        text = text.replace("MODULE QUIZ", "Practice", 1)
                    if re.fullmatch(r"Module \d+\.\d+", text) and mode == "practice":
                        text = "Solutions for " + text.lower()
                        is_heading = True
                    target.append({"type": "heading" if is_heading else "paragraph", "text": text})
                    last_context = text
                    emitted += 1
                record["outputBlocks"] = emitted
                if skipped:
                    record["notes"] = skipped
                if not emitted:
                    record.update(action="skipped", reason="; ".join(skipped) or "empty block")
                if not in_reference:
                    stats["importedTextBlocks" if emitted else "omittedTextBlocks"] += 1

        print(f"Imported volume {book}: {sum(1 for r in audit['readings'].values() if r['volume'] == book)} readings", flush=True)

    if set(lessons) != set(index):
        raise ValueError(f"Missing readings: {set(index) - set(lessons)}")
    for number, lesson in lessons.items():
        expected = [m["id"] for m in index[number]["modules"]]
        actual = [m["id"] for m in lesson["modules"]]
        if actual != expected:
            raise ValueError(f"Reading {number}: modules {actual} do not match {expected}")
        (OUTPUT / "readings" / f"{number:03}.json").write_text(json.dumps(lesson, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (OUTPUT / "reference.json").write_text(json.dumps(reference, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (ROOT / "docs/full-reading-import-audit.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Imported {len(lessons)} readings, {len(image_cache)} distinct visual assets, and {len(reference['sections'])} reference sections.")


if __name__ == "__main__":
    main()
