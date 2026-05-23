"""Visualization for BFI-10 stability experiments.

Generates three plots and a combined dashboard:
  1. Fleiss kappa vs temperature, per (model, prompt) — temperature effect.
  2. Mean Fleiss kappa per prompt (averaged across models) — prompt effect.
  3. Final ranking of (model, prompt) configurations at the reference temperature.
"""

import json
import os
from collections import defaultdict

import matplotlib.pyplot as plt
import numpy as np


MODEL_ORDER = ["mistral", "llama3.1", "gpt-oss"]
PROMPT_ORDER = ["baseline", "few_shot", "format_constrained"]
PROMPT_COLORS = {
    "baseline": "#4C72B0",
    "few_shot": "#55A868",
    "format_constrained": "#C44E52",
}
MODEL_MARKERS = {"mistral": "o", "llama3.1": "s", "gpt-oss": "^"}


def _load_summaries(paths: list[str]) -> list[dict]:
    """Load and flatten summary JSONs into a list of row dicts."""
    rows = []
    for p in paths:
        if not os.path.exists(p):
            continue
        with open(p) as f:
            d = json.load(f)
        for _, v in d.items():
            if v.get("n_successful", 0) == 0:
                continue
            rows.append(v)
    return rows


def plot_temperature_effect(rows: list[dict], out_path: str) -> None:
    """One subplot per model; lines per prompt; x = temperature, y = Fleiss κ."""
    by_model = defaultdict(lambda: defaultdict(list))  # model -> prompt -> [(T, κ)]
    for r in rows:
        by_model[r["model_name"]][r["prompt_type"]].append(
            (r["temperature"], r["stability_fleiss_kappa"])
        )

    models = [m for m in MODEL_ORDER if m in by_model]
    fig, axes = plt.subplots(1, len(models), figsize=(5 * len(models), 4.2), sharey=True)
    if len(models) == 1:
        axes = [axes]

    for ax, m in zip(axes, models):
        for prompt in PROMPT_ORDER:
            pts = sorted(by_model[m].get(prompt, []))
            if not pts:
                continue
            xs, ys = zip(*pts)
            ax.plot(
                xs, ys,
                marker=MODEL_MARKERS.get(m, "o"),
                color=PROMPT_COLORS[prompt],
                label=prompt,
                linewidth=2,
                markersize=8,
            )
        ax.set_title(m, fontsize=12, fontweight="bold")
        ax.set_xlabel("Temperature")
        ax.set_ylim(-0.05, 1.05)
        ax.grid(True, alpha=0.3)
        ax.axhline(0, color="gray", linewidth=0.5)
    axes[0].set_ylabel("Fleiss κ (powtarzalność)")
    axes[-1].legend(loc="lower left", fontsize=9, framealpha=0.9)
    fig.suptitle("Wpływ temperatury na stabilność (Fleiss κ)", fontsize=13, fontweight="bold")
    fig.tight_layout()
    fig.savefig(out_path, dpi=140, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {out_path}")


def plot_prompt_effect(rows: list[dict], out_path: str, ref_temp: float = 0.7) -> None:
    """Two-panel: (left) mean κ per prompt across all (model, T); (right) κ per prompt at ref temp."""
    by_prompt_all = defaultdict(list)
    by_prompt_ref = defaultdict(list)
    for r in rows:
        by_prompt_all[r["prompt_type"]].append(r["stability_fleiss_kappa"])
        if abs(r["temperature"] - ref_temp) < 1e-6:
            by_prompt_ref[r["prompt_type"]].append(r["stability_fleiss_kappa"])

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

    # Left: aggregate over all (model, T)
    means_all = [np.mean(by_prompt_all[p]) for p in PROMPT_ORDER]
    stds_all = [np.std(by_prompt_all[p]) for p in PROMPT_ORDER]
    colors = [PROMPT_COLORS[p] for p in PROMPT_ORDER]
    bars = axes[0].bar(PROMPT_ORDER, means_all, yerr=stds_all, color=colors, capsize=6, edgecolor="black")
    for bar, mean in zip(bars, means_all):
        axes[0].text(bar.get_x() + bar.get_width() / 2, mean + 0.02,
                     f"{mean:.3f}", ha="center", fontsize=10, fontweight="bold")
    axes[0].set_title(f"Średnia κ per prompt\n(uśredniona po modelach i temp.)", fontsize=11)
    axes[0].set_ylabel("Fleiss κ")
    axes[0].set_ylim(0, 1.1)
    axes[0].grid(True, alpha=0.3, axis="y")

    # Right: per-model bars at ref temp
    x = np.arange(len(PROMPT_ORDER))
    width = 0.25
    models_present = sorted(
        {r["model_name"] for r in rows if abs(r["temperature"] - ref_temp) < 1e-6},
        key=lambda m: MODEL_ORDER.index(m) if m in MODEL_ORDER else 99,
    )
    for i, m in enumerate(models_present):
        ys = []
        for p in PROMPT_ORDER:
            vals = [r["stability_fleiss_kappa"] for r in rows
                    if r["model_name"] == m and r["prompt_type"] == p
                    and abs(r["temperature"] - ref_temp) < 1e-6]
            ys.append(vals[0] if vals else 0)
        axes[1].bar(x + (i - len(models_present) / 2 + 0.5) * width, ys, width, label=m, edgecolor="black")
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(PROMPT_ORDER)
    axes[1].set_title(f"Stabilność per (model, prompt) przy T={ref_temp}", fontsize=11)
    axes[1].set_ylabel("Fleiss κ")
    axes[1].set_ylim(0, 1.1)
    axes[1].legend(fontsize=9)
    axes[1].grid(True, alpha=0.3, axis="y")

    fig.suptitle("Wpływ typu promptu na stabilność", fontsize=13, fontweight="bold")
    fig.tight_layout()
    fig.savefig(out_path, dpi=140, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {out_path}")


def plot_ranking(rows: list[dict], out_path: str, ref_temp: float = 0.7) -> None:
    """Horizontal bar chart ranking (model, prompt) configurations at ref_temp."""
    at_ref = [r for r in rows if abs(r["temperature"] - ref_temp) < 1e-6]
    at_ref.sort(key=lambda r: r["stability_fleiss_kappa"])

    labels = [f"{r['model_name']} + {r['prompt_type']}" for r in at_ref]
    kappas = [r["stability_fleiss_kappa"] for r in at_ref]
    colors = [PROMPT_COLORS.get(r["prompt_type"], "gray") for r in at_ref]

    fig, ax = plt.subplots(figsize=(9, 0.45 * len(labels) + 1.5))
    bars = ax.barh(labels, kappas, color=colors, edgecolor="black")
    for bar, k in zip(bars, kappas):
        ax.text(min(k, 1.0) + 0.01, bar.get_y() + bar.get_height() / 2,
                f"{k:.3f}", va="center", fontsize=10, fontweight="bold")
    ax.set_xlim(0, 1.15)
    ax.set_xlabel("Fleiss κ")
    ax.set_title(f"Ranking konfiguracji (T={ref_temp}) — im wyżej, tym stabilniej", fontsize=12, fontweight="bold")
    ax.axvline(0.8, color="green", linestyle="--", alpha=0.5, label="„substantial agreement\" (κ≥0.8)")
    ax.axvline(0.6, color="orange", linestyle="--", alpha=0.5, label="„moderate agreement\" (κ≥0.6)")
    ax.legend(loc="lower right", fontsize=9)
    ax.grid(True, alpha=0.3, axis="x")
    fig.tight_layout()
    fig.savefig(out_path, dpi=140, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {out_path}")


def generate_all(summary_paths: list[str], out_dir: str = "results/plots", ref_temp: float = 0.7) -> None:
    os.makedirs(out_dir, exist_ok=True)
    rows = _load_summaries(summary_paths)
    print(f"Loaded {len(rows)} non-empty summary rows from {len(summary_paths)} files")
    plot_temperature_effect(rows, os.path.join(out_dir, "01_temperature_effect.png"))
    plot_prompt_effect(rows, os.path.join(out_dir, "02_prompt_effect.png"), ref_temp=ref_temp)
    plot_ranking(rows, os.path.join(out_dir, "03_ranking.png"), ref_temp=ref_temp)


if __name__ == "__main__":
    default_paths = [
        "results/results_tmptr_3_summary.json",
        "results/results_tmptr_5_summary.json",
        "results/results_summary.json",
        "results/results_tmptr_10_summary.json",
        "results/results_gpt_oss_summary.json",
        "results/results_gpt_oss_temp_0.3_summary.json",
        "results/results_gpt_oss_temp_0.5_summary.json",
        "results/results_gpt_oss_temp_1.0_summary.json",
    ]
    generate_all(default_paths)
