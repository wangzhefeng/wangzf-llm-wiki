from __future__ import annotations

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd


def save_plots(result_df: pd.DataFrame, output_dir: str | Path) -> None:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(10, 4))
    plt.plot(result_df["time_index"], result_df["soc"], label="SOC")
    plt.xlabel("Time Index")
    plt.ylabel("SOC")
    plt.title("SOC Trajectory")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path / "soc_trajectory.png", dpi=150)
    plt.close()

    plt.figure(figsize=(10, 4))
    plt.step(result_df["time_index"], result_df["p_batt_mw"], where="post", label="Battery Power (MW)")
    plt.step(result_df["time_index"], result_df["p_grid_mw"], where="post", label="Grid Power (MW)")
    plt.xlabel("Time Index")
    plt.ylabel("Power (MW)")
    plt.title("Battery Dispatch and Grid Power")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path / "power_dispatch.png", dpi=150)
    plt.close()

    fig = plt.figure(figsize=(10, 4))
    ax1 = fig.add_subplot(111)
    ax1.plot(result_df["time_index"], result_df["load_actual_mw"], label="Load (MW)")
    ax1.set_xlabel("Time Index")
    ax1.set_ylabel("Load (MW)")
    ax1.grid(True)

    ax2 = ax1.twinx()
    ax2.plot(result_df["time_index"], result_df["price_actual"], label="Price", linestyle="--")
    ax2.set_ylabel("Price")

    ax1.set_title("Load and Price Overview")
    fig.tight_layout()
    fig.savefig(output_path / "price_load_overview.png", dpi=150)
    plt.close(fig)
