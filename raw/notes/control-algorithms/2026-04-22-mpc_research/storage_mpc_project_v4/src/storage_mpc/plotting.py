from __future__ import annotations

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd


def save_plots(real_time_df: pd.DataFrame, output_dir: str | Path) -> None:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(10, 4))
    plt.plot(real_time_df["time_index"], real_time_df["soc"], label="SOC")
    plt.xlabel("Time Index")
    plt.ylabel("SOC")
    plt.title("SOC Trajectory")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path / "soc_trajectory.png", dpi=150)
    plt.close()

    plt.figure(figsize=(10, 4))
    plt.step(real_time_df["time_index"], real_time_df["p_charge_mw"], where="post", label="Charge")
    plt.step(real_time_df["time_index"], real_time_df["p_discharge_mw"], where="post", label="Discharge")
    plt.step(real_time_df["time_index"], real_time_df["p_buy_mw"], where="post", label="Grid Buy")
    plt.step(real_time_df["time_index"], real_time_df["p_sell_mw"], where="post", label="Grid Sell")
    plt.xlabel("Time Index")
    plt.ylabel("Power (MW)")
    plt.title("Power Dispatch")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path / "power_dispatch.png", dpi=150)
    plt.close()

    plt.figure(figsize=(10, 4))
    plt.plot(real_time_df["time_index"], real_time_df["energy_cost"], label="Energy Cost")
    plt.plot(real_time_df["time_index"], real_time_df["plan_track_cost"], label="Plan Track Cost")
    plt.xlabel("Time Index")
    plt.ylabel("Cost")
    plt.title("Cost Overview")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path / "cost_overview.png", dpi=150)
    plt.close()
