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
from datetime import date
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

    # 创建 12 行、31 列的空表
    calendar = [[float("nan")] * 31 for _ in range(12)]

    # 把每日降水量放进对应的格子
    for day, amount in table:
        current = date.fromisoformat(day)

        if amount is None:
            raise ValueError(f"Missing precipitation: {day}")

        calendar[current.month - 1][current.day - 1] = amount

       # 累加每个月的降水量
    monthly = [0.0] * 12

    for day, amount in table:
        current = date.fromisoformat(day)
        monthly[current.month - 1] += amount

    print("\nMonthly precipitation:")
    for month, total in enumerate(monthly, start=1):
        print(f"{month:02}: {total:.1f} mm")

    # 用颜色显示每个格子的数值
    fig, (ax, bars) = plt.subplots(
        1, 2,
        figsize=(16, 6),
        gridspec_kw={"width_ratios": [4, 1]},
        sharey=True,
    )

    colors = plt.get_cmap("YlGnBu").copy()
    colors.set_bad("#eeeeee")

    image = ax.imshow(
        calendar,
        cmap=colors,
        aspect="auto",
        vmin=0,
        interpolation="nearest",
    )

    ax.set_xticks(range(31))
    ax.set_xticklabels(range(1, 32))
    ax.set_yticks(range(12))
    ax.set_yticklabels([
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
    ])

    ax.set_xlabel("Day of month")
    ax.set_ylabel("Month")
    ax.set_title("Hong Kong daily precipitation | 2025")
        # 找到降水量最大的一条记录
    peak_day, peak_amount = max(table, key=lambda row: row[1])
    peak_date = date.fromisoformat(peak_day)

    ax.scatter(
        peak_date.day - 1,
        peak_date.month - 1,
        s=150,
        facecolors="none",
        edgecolors="#d07836",
        linewidths=2,
    )

    ax.set_title(
        "Hong Kong daily precipitation | 2025\n"
        f"Wettest day: {peak_day} / {peak_amount:.1f} mm"
    )

    # 找出降水最多的月份，用橙色突出显示
    wettest = monthly.index(max(monthly))
    bar_colors = [
        "#d07836" if month == wettest else "#277d87"
        for month in range(12)
    ]

    bars.barh(range(12), monthly, color=bar_colors, height=0.65)
    bars.set_title("Monthly total")
    bars.set_xlabel("Precipitation (mm)")
    bars.set_xlim(0, max(monthly) * 1.3)
    bars.tick_params(axis="y", left=False, labelleft=False)

    # 在每根条形右侧写出数值
    for month, total in enumerate(monthly):
        bars.text(
            total + 5, month, f"{total:.1f}",
            va="center", fontsize=9,
        )
    fig.colorbar(image, ax=ax, label="Daily precipitation (mm)")
    fig.text(
        0.01, 0.02,
        "Source: Open-Meteo / ERA5 | Gridded estimates | "
        "Grey cells: dates that do not exist",
        fontsize=9,
    )

    fig.tight_layout(rect=[0, 0.06, 1, 1])

    OUT.mkdir(exist_ok=True)
    fig.savefig(OUT / PICTURE, dpi=150)
    print(f"Saved: {OUT / PICTURE}")
    plt.show()


if __name__ == "__main__":
    main()
