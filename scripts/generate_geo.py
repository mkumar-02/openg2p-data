"""Parse master-data SQL files into geo/*.json."""

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MASTER_DATA = Path("/Volumes/Work/OpenG2P/master-data")
OUT_DIR = REPO_ROOT / "geo"

VALUE_ROW_RE = re.compile(
    r"\(\s*'([^']+)'\s*,\s*'([^']+)'\s*,\s*'([^']+)'\s*,\s*(NULL|'[^']*')\s*\)",
    re.IGNORECASE,
)

LEVEL_FILES = {
    0: ("level-0.sql", "level-0-country.json"),
    1: ("level-1.sql", "level-1-regions.json"),
    2: ("level-2.sql", "level-2-districts.json"),
    3: ("level-3.sql", "level-3-wards.json"),
    4: ("level-4.sql", "level-4-villages.json"),
}


def parse_level_values(sql_path: Path) -> list[dict]:
    text = sql_path.read_text()
    rows = []
    for m in VALUE_ROW_RE.finditer(text):
        level_value_id, level_id, mnemonic, parent = m.groups()
        parent_value = None if parent.upper() == "NULL" else parent.strip("'")
        rows.append(
            {
                "level_value_id": level_value_id,
                "level_id": level_id,
                "level_value_mnemonic": mnemonic,
                "parent_level_value_id": parent_value,
            }
        )
    return rows


def parse_levels(sql_path: Path) -> list[dict]:
    text = sql_path.read_text()
    pattern = re.compile(
        r"VALUES\s*\(\s*'([^']+)'\s*,\s*'([^']+)'\s*,\s*(NULL|'[^']*')\s*\)",
        re.IGNORECASE,
    )
    rows = []
    for m in pattern.finditer(text):
        level_id, mnemonic, parent = m.groups()
        parent_id = None if parent.upper() == "NULL" else parent.strip("'")
        rows.append(
            {
                "level_id": level_id,
                "level_mnemonic": mnemonic,
                "parent_level_id": parent_id,
            }
        )
    return rows


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    levels = parse_levels(MASTER_DATA / "g2p_geo_levels.sql")
    (OUT_DIR / "levels.json").write_text(json.dumps(levels, indent=2) + "\n")
    print(f"Wrote levels.json: {len(levels)} levels")

    for level_num, (sql_name, out_name) in LEVEL_FILES.items():
        rows = parse_level_values(MASTER_DATA / sql_name)
        (OUT_DIR / out_name).write_text(json.dumps(rows, indent=2) + "\n")
        print(f"Wrote {out_name}: {len(rows)} entries")


if __name__ == "__main__":
    main()
