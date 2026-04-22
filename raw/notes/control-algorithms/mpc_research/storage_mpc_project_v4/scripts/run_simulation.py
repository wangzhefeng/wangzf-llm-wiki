from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from storage_mpc.config import load_config
from storage_mpc.data_generator import generate_synthetic_data
from storage_mpc.hierarchical_simulator import run_hierarchical_simulation
from storage_mpc.plotting import save_plots


def main() -> None:
    config = load_config(PROJECT_ROOT / "configs" / "default_config.json")

    data_dir = PROJECT_ROOT / "data"
    results_dir = PROJECT_ROOT / "results"
    data_dir.mkdir(parents=True, exist_ok=True)
    results_dir.mkdir(parents=True, exist_ok=True)

    df_actual = generate_synthetic_data(config)
    df_actual.to_csv(data_dir / "synthetic_inputs.csv", index=False, encoding="utf-8-sig")

    day_df, intra_df, rt_df = run_hierarchical_simulation(df_actual, config, results_dir)
    save_plots(rt_df, results_dir)

    print("=== Hierarchical Simulation Finished ===")
    print(f"Day-ahead rows: {len(day_df)}")
    print(f"Intra-day rows: {len(intra_df)}")
    print(f"Real-time rows: {len(rt_df)}")
    print(f"Total real-time cost: {rt_df['stage_cost'].sum():.4f}")
    print(f"Final SOC: {rt_df['soc_next'].iloc[-1]:.4f}")
    print(f"Results saved to: {results_dir}")


if __name__ == "__main__":
    main()
