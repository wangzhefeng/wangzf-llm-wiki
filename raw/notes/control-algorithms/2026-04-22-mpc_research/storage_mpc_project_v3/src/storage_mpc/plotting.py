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
    plt.step(result_df["time_index"], result_df["p_charge_mw"], where="post", label="Charge")
    plt.step(result_df["time_index"], result_df["p_discharge_mw"], where="post", label="Discharge")
    plt.step(result_df["time_index"], result_df["p_buy_mw"], where="post", label="Grid Buy")
    plt.step(result_df["time_index"], result_df["p_sell_mw"], where="post", label="Grid Sell")
    plt.xlabel("Time Index")
    plt.ylabel("Power (MW)")
    plt.title("Power Stack")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path / "power_stack.png", dpi=150)
    plt.close()

    plt.figure(figsize=(10, 4))
    plt.plot(result_df["time_index"], result_df["energy_cost"], label="Energy Cost")
    plt.plot(result_df["time_index"], result_df["deviation_cost"], label="Deviation Cost")
    plt.xlabel("Time Index")
    plt.ylabel("Cost")
    plt.title("Cost Breakdown")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path / "cost_breakdown.png", dpi=150)
    plt.close()

    fig = plt.figure(figsize=(10, 4))
    ax1 = fig.add_subplot(111)
    ax1.plot(result_df["time_index"], result_df["buy_price_actual"], label="Buy Price")
    ax1.plot(result_df["time_index"], result_df["sell_price_actual"], label="Sell Price", linestyle="--")
    ax1.set_xlabel("Time Index")
    ax1.set_ylabel("Price")
    ax1.grid(True)
    ax1.legend()
    ax1.set_title("Price Overview")
    fig.tight_layout()
    fig.savefig(output_path / "price_overview.png", dpi=150)
    plt.close(fig)
