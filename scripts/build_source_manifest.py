from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


MODULE_RE = re.compile(r"(?m)^\f?MODULE\s+(\d+\.\d+):\s*(.+)$")
LOS_RE = re.compile(r"^\f?LOS\s+(\d+\.[a-z]+):\s*(.*)")


def parse_args() -> argparse.Namespace:
    default_sources = Path(__file__).resolve().parents[2] / "work" / "pdf_text"
    parser = argparse.ArgumentParser(
        description="Build the internal learning-outcome/source-page coverage manifest."
    )
    parser.add_argument("--source-dir", type=Path, default=default_sources)
    return parser.parse_args()


def normalize(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def parse_los(block: str) -> list[dict[str, str]]:
    objectives: list[dict[str, str]] = []
    lines = block.splitlines()
    index = 0
    while index < len(lines):
        match = LOS_RE.match(lines[index].strip())
        if not match:
            index += 1
            continue

        statement = match.group(2).strip()
        next_index = index + 1
        while (
            next_index < len(lines)
            and lines[next_index].strip()
            and not LOS_RE.match(lines[next_index].strip())
        ):
            statement += f" {lines[next_index].strip()}"
            next_index += 1
        objectives.append(
            {"id": match.group(1), "sourceStatement": normalize(statement)}
        )
        index = next_index
    return objectives


def main() -> None:
    args = parse_args()
    project = Path(__file__).resolve().parents[1]
    curriculum = json.loads(
        (project / "src" / "data" / "curriculum.json").read_text(encoding="utf-8")
    )
    modules_by_id = {
        module["id"]: (reading, module)
        for reading in curriculum
        for module in reading["modules"]
    }

    records: list[dict] = []
    for book in range(1, 5):
        source = (args.source_dir / f"book{book}.txt").read_text(
            encoding="utf-8", errors="replace"
        )
        matches = list(MODULE_RE.finditer(source))
        for index, match in enumerate(matches):
            module_id = match.group(1)
            end = matches[index + 1].start() if index + 1 < len(matches) else len(source)
            reading, module = modules_by_id[module_id]
            records.append(
                {
                    "moduleId": module_id,
                    "readingId": reading["number"],
                    "readingTitle": reading["title"],
                    "moduleTitle": module["title"],
                    "source": {
                        "book": book,
                        "pdfPage": source.count("\f", 0, match.start()) + 1,
                        "heading": normalize(match.group(2)),
                    },
                    "objectives": parse_los(source[match.start() : end]),
                    "status": "mapped",
                }
            )

    records.sort(key=lambda item: tuple(map(int, item["moduleId"].split("."))))
    missing = sorted(set(modules_by_id) - {item["moduleId"] for item in records})
    objective_count = sum(len(item["objectives"]) for item in records)
    if missing or len(records) != 152 or objective_count != 365:
        raise SystemExit(
            f"Coverage mismatch: modules={len(records)}, objectives={objective_count}, missing={missing}"
        )

    output = project / "src" / "data" / "sourceManifest.json"
    output.write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Mapped {len(records)} modules and {objective_count} learning outcomes.")


if __name__ == "__main__":
    main()
