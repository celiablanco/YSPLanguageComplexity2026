#!/usr/bin/env python3
"""
compare_sizes.py

Measures the file sizes of all .txt files across the 'source', 'translated',
and 'ipa' pipeline folders and plots a grouped bar chart comparing them.

Setup:
    pip install matplotlib

Usage:
    python file_size.py
    python file_size.py --unit kb       # show sizes in KB (default: bytes)
    python file_size.py --unit kb --output report.png
"""

import argparse
import sys
from pathlib import Path

try:
    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker
    import numpy as np
except ImportError:
    sys.exit("Missing dependency 'matplotlib'.\nInstall it with: pip install matplotlib")

# ── Config ────────────────────────────────────────────────────────────────────
FOLDERS = {
    "source":     Path("source"),
    "translated": Path("translated"),
    "ipa":        Path("ipa"),
}

COLORS = {
    "source":     "#4C9BE8",
    "translated": "#57C27A",
    "ipa":        "#E87B4C",
}

UNIT_DIVISORS = {"bytes": 1, "kb": 1_024, "mb": 1_048_576}


# ── Helpers ───────────────────────────────────────────────────────────────────
def collect_sizes(unit: str) -> dict[str, dict[str, float]]:
    """
    Returns {folder_label: {stem: size}} for every .txt file found.
    Files missing from a folder get size 0 so the chart bars still align.
    """
    divisor = UNIT_DIVISORS[unit]

    # Gather all unique file stems across all folders
    all_stems: set[str] = set()
    raw: dict[str, dict[str, float]] = {label: {} for label in FOLDERS}

    for label, folder in FOLDERS.items():
        if not folder.exists():
            print(f"  Warning: folder '{folder}/' not found — skipping.")
            continue
        for f in sorted(folder.glob("*.txt")):
            # Normalise stem: strip suffixes like _es, _ipa added by the pipeline
            norm = f.stem
            for suffix in ("_ipa", "_es", "_fr", "_de", "_ja", "_pt", "_it",
                           "_zh", "_ru", "_ar", "_ko", "_nl", "_pl", "_sv",
                           "_tr", "_hi", "_id", "_uk", "_cs", "_ro", "_hu"):
                if norm.endswith(suffix):
                    norm = norm[: -len(suffix)]
                    break
            raw[label][norm] = f.stat().st_size / divisor
            all_stems.add(norm)

    # Fill missing entries with 0
    stems = sorted(all_stems)
    data: dict[str, dict[str, float]] = {}
    for label in FOLDERS:
        data[label] = {s: raw[label].get(s, 0.0) for s in stems}

    return data


def plot(data: dict[str, dict[str, float]], unit: str, output: str | None):
    labels = list(FOLDERS.keys())
    stems  = list(next(iter(data.values())).keys())

    if not stems:
        sys.exit("No .txt files found in any of the three folders.")

    n_files   = len(stems)
    n_folders = len(labels)
    x         = np.arange(n_files)
    bar_w     = 0.22
    offsets   = np.linspace(-(n_folders - 1) / 2, (n_folders - 1) / 2, n_folders) * bar_w

    # ── Figure ────────────────────────────────────────────────────────────────
    fig_w = max(9, n_files * 1.8)
    fig, ax = plt.subplots(figsize=(fig_w, 6))
    fig.patch.set_facecolor("#F7F8FA")
    ax.set_facecolor("#F7F8FA")

    bars_all = []
    for i, label in enumerate(labels):
        sizes = [data[label][s] for s in stems]
        bars  = ax.bar(
            x + offsets[i],
            sizes,
            width=bar_w,
            label=label.capitalize(),
            color=COLORS[label],
            edgecolor="white",
            linewidth=0.6,
            zorder=3,
        )
        bars_all.append(bars)

        # Value labels on top of each bar
        for bar, val in zip(bars, sizes):
            if val > 0:
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + ax.get_ylim()[1] * 0.005,
                    f"{val:,.1f}" if unit != "bytes" else f"{int(val):,}",
                    ha="center", va="bottom",
                    fontsize=7.5, color="#444",
                )

    # ── Axes styling ──────────────────────────────────────────────────────────
    unit_label = {"bytes": "Bytes", "kb": "Kilobytes (KB)", "mb": "Megabytes (MB)"}[unit]

    ax.set_xticks(x)
    ax.set_xticklabels(stems, fontsize=10, rotation=20, ha="right")
    ax.set_ylabel(f"File size ({unit_label})", fontsize=11, labelpad=10)
    ax.set_title("File Size Comparison Across Pipeline Stages", fontsize=14, fontweight="bold", pad=16)

    ax.yaxis.set_major_formatter(
        ticker.FuncFormatter(lambda v, _: f"{v:,.0f}" if unit == "bytes" else f"{v:,.2f}")
    )
    ax.set_ylim(bottom=0)
    ax.margins(x=0.04)
    ax.grid(axis="y", color="white", linewidth=1.2, zorder=0)
    ax.spines[["top", "right", "left", "bottom"]].set_visible(False)
    ax.tick_params(axis="both", length=0)

    # ── Legend ────────────────────────────────────────────────────────────────
    legend = ax.legend(
        title="Pipeline stage",
        title_fontsize=9,
        fontsize=9,
        frameon=True,
        framealpha=0.9,
        edgecolor="#ddd",
        loc="upper right",
    )
    legend.get_frame().set_facecolor("#F7F8FA")

    plt.tight_layout()

    if output:
        fig.savefig(output, dpi=150, bbox_inches="tight")
        print(f"Chart saved to: {output}")
    else:
        plt.show()


# ── Summary table ─────────────────────────────────────────────────────────────
def print_summary(data: dict[str, dict[str, float]], unit: str):
    stems  = list(next(iter(data.values())).keys())
    labels = list(data.keys())

    col_w   = max(len(s) for s in stems) + 2
    num_w   = 12
    divider = "─" * (col_w + num_w * len(labels) + len(labels))

    unit_suffix = {"bytes": "B", "kb": "KB", "mb": "MB"}[unit]

    print(f"\n{'File':<{col_w}}", end="")
    for label in labels:
        print(f"{label.capitalize() + ' (' + unit_suffix + ')':>{num_w}}", end="")
    print(f"\n{divider}")

    for stem in stems:
        print(f"{stem:<{col_w}}", end="")
        for label in labels:
            val = data[label][stem]
            fmt = f"{val:,.1f}" if unit != "bytes" else f"{int(val):,}"
            print(f"{fmt:>{num_w}}", end="")
        print()

    # Totals row
    print(divider)
    print(f"{'TOTAL':<{col_w}}", end="")
    for label in labels:
        total = sum(data[label].values())
        fmt   = f"{total:,.1f}" if unit != "bytes" else f"{int(total):,}"
        print(f"{fmt:>{num_w}}", end="")
    print("\n")


# ── Entry point ───────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Compare .txt file sizes across source/, translated/, and ipa/ folders."
    )
    parser.add_argument(
        "--unit",
        choices=["bytes", "kb", "mb"],
        default="bytes",
        help="Unit for file sizes (default: bytes)",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Save the chart to this file instead of displaying it (e.g. report.png)",
    )
    args = parser.parse_args()

    print("Scanning folders...")
    data = collect_sizes(args.unit)

    print_summary(data, args.unit)
    plot(data, args.unit, args.output)


if __name__ == "__main__":
    main()