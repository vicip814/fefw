"""Refresh Game8 Preferred Skills (boons) and Non-Ideal Skills (banes)."""

from __future__ import annotations

import json
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "game8-skills.json"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; FEFW-guide-data-refresh/1.0)"}


def skill_names(cell):
    if cell is None:
        return []
    names = []
    for image in cell.select("img[alt]"):
        value = image.get("alt", "").strip()
        if value.endswith(" Skill") and value not in names:
            names.append(value[:-6])
    return names


def scrape(name: str, url: str):
    response = requests.get(url, headers=HEADERS, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    result = {"name": name, "source_url": url, "boons": [], "banes": []}
    labels = {"Preferred Skills": "boons", "Non-Ideal Skills": "banes"}
    for row in soup.select("tr"):
        header = row.find("th")
        if not header:
            continue
        field = labels.get(header.get_text(" ", strip=True))
        if field:
            result[field] = skill_names(row.find("td"))
    if not result["boons"] and not result["banes"]:
        raise RuntimeError(f"No skill affinity table found for {name}: {url}")
    return result


def main():
    characters = json.loads((ROOT / "characters.json").read_text(encoding="utf-8"))
    records = []
    failures = []
    for character in characters:
        if character.get("sourceAdditional"):
            continue
        try:
            records.append(scrape(character["name"], character["url"]))
            print(f"OK {character['name']}")
        except Exception as error:  # retain a complete failure report for review
            failures.append({"name": character["name"], "url": character["url"], "error": str(error)})
            print(f"FAIL {character['name']}: {error}")
        time.sleep(0.15)
    payload = {
        "source_index_url": "https://game8.co/games/Fire-Emblem-Fortunes-Weave/archives/624024",
        "definition": {
            "boons": "Preferred Skills: skills the character learns efficiently.",
            "banes": "Non-Ideal Skills: skills the character learns inefficiently.",
        },
        "record_count": len(records),
        "characters": records,
        "failures": failures,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUT.name}: {len(records)} records, {len(failures)} failures")
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
