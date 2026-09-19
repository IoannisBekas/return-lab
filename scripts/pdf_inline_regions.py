"""Preserve PDF paragraphs whose inline equations are separate image objects.

PDF text blocks can overlap in the vertical direction when an inline formula
interrupts a sentence. Sorting those whole blocks reverses sentence fragments.
Group only vertically connected blocks containing both text and a real image;
the caller renders the whole region once, retaining every original disposition.
"""
from __future__ import annotations

import re

import pymupdf


BOUNDARY = re.compile(r"^(?:READING\s+\d+$|MODULE\s+\d+\.\d+:|MODULE QUIZ|KEY CONCEPTS|ANSWER KEY|LOS\s+\d+\.[a-z]+:|EXAMPLE:|Figure\s+\d+\.\d+:)")


def decorative_icon(block: dict) -> bool:
    if block["type"] != 1:
        return False
    rect = pymupdf.Rect(block["bbox"])
    return (block["width"] == 46 and block["height"] == 31 and 29 <= rect.width <= 31) or (
        block["width"] == 25 and block["height"] == 30 and 18 <= rect.width <= 20
    )


def paragraph_regions(blocks: list[dict]) -> dict[int, dict]:
    eligible = []
    for index, block in enumerate(blocks):
        if block["type"] == 1:
            if not decorative_icon(block):
                eligible.append(index)
        elif block["type"] == 0:
            lines = ["".join(s["text"] for s in line["spans"]).strip() for line in block["lines"]]
            if not any(BOUNDARY.match(line) for line in lines):
                eligible.append(index)

    # Connected components of overlapping vertical intervals. Touching endpoints
    # do not join successive paragraphs; only a true shared line/region does.
    components: list[list[int]] = []
    for index in eligible:
        top, bottom = blocks[index]["bbox"][1], blocks[index]["bbox"][3]
        matches = [c for c in components if any(
            min(bottom, blocks[other]["bbox"][3]) - max(top, blocks[other]["bbox"][1]) > 1
            for other in c
        )]
        if not matches:
            components.append([index])
        else:
            component = [index]
            for other in matches:
                component.extend(other)
                components.remove(other)
            components.append(component)

    result = {}
    for component in components:
        if not any(blocks[i]["type"] == 0 for i in component) or not any(blocks[i]["type"] == 1 for i in component):
            continue
        rect = pymupdf.Rect(blocks[component[0]]["bbox"])
        lines = []
        for index in component:
            rect |= pymupdf.Rect(blocks[index]["bbox"])
            for line in blocks[index].get("lines", []):
                lines.append(line)
        # Sort by baseline bands then x, rather than by PDF block order. The crop
        # itself carries exact mathematics; text supports search and alt prose.
        lines.sort(key=lambda line: (round(line["bbox"][3] / 3), line["bbox"][0]))
        text = " ".join("".join(span["text"] for span in line["spans"]).strip() for line in lines)
        indices = sorted(component)
        result[indices[0]] = {"indices": indices, "bbox": rect, "text": text}
    return result
