import json
import matplotlib.pyplot as plt


def visualize_results(summary_path: str = "results_summary.json"):
    with open(summary_path) as f:
        data = json.load(f)
    
    models = set()
    for key in data:
        parts = key.split("_")
        if len(parts) >= 2:
            models.add(parts[0])
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    metrics = ["stability_fleiss_kappa", "stability_krippendorff_alpha", 
               "stability_mean_std", "semantic_cosine"]
    titles = ["Fleiss Kappa", "Krippendorff Alpha", "Mean Std", "Cosine Similarity"]
    
    for ax, metric, title in zip(axes.flat, metrics, titles):
        for key, values in data.items():
            ax.bar(key.split("_")[1] if "_" in key else key, values.get(metric, 0))
        ax.set_title(title)
        ax.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig(summary_path.replace(".json", ".png"))
    print(f"Plot saved to {summary_path.replace('.json', '.png')}")


if __name__ == "__main__":
    visualize_results()
