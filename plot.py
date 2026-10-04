# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib"]
# ///

"""
Read the file in data/, make one picture, save it to out/.

    uv run plot.py

Three parts, and you will replace all three: rows() reads the file the way *your*
file needs reading, the loop in main() picks the numbers out of it, and the plot at
the bottom is the transformation you chose. Print before you plot.
"""

import json
from pathlib import Path

import matplotlib.pyplot as plt

FILE = "hong-kong-precipitation-2025.json"   # CHANGE ME: the same name as in fetch.py
PICTURE = "plot.png"                           # what goes into out/, and into the README

HERE = Path(__file__).parent
DATA = HERE / "data" / FILE
OUT = HERE / "out"


def rows(path):
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)

    dates = data["daily"]["time"]
    amounts = data["daily"]["precipitation_sum"]

    if len(dates) != len(amounts):
        raise ValueError("日期和降水数值的数量不一致")

    return list(zip(dates, amounts))


def main():
    table = rows(DATA)
    print(f"{DATA.name}: {len(table)} rows.")

    for day, amount in table[:5]:
        print(f"{day}: {amount} mm")


if __name__ == "__main__":
    main()
