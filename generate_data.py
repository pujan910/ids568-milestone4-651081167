import argparse
import os
from pathlib import Path

import numpy as np
import pandas as pd


def generate_data(n_rows: int, seed: int, output_path: str) -> None:
    np.random.seed(seed)

    df = pd.DataFrame(
        {
            "user_id": np.random.randint(1, 100000, n_rows),
            "transaction_amount": np.random.uniform(1, 1000, n_rows),
            "transaction_type": np.random.choice(
                ["purchase", "refund", "transfer"], n_rows
            ),
            "timestamp": pd.date_range("2023-01-01", periods=n_rows, freq="s"),
        }
    )

    output = Path(output_path)

    if output.suffix == "":
        output.mkdir(parents=True, exist_ok=True)
        output_file = output / "data.parquet"
    else:
        output.parent.mkdir(parents=True, exist_ok=True)
        output_file = output

    df.to_parquet(output_file, index=False)
    print(f"Generated {n_rows} rows and saved to {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate synthetic transaction data.")
    parser.add_argument("--rows", type=int, default=10000000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=str, default="data.parquet")

    args = parser.parse_args()

    if args.rows <= 0:
        raise ValueError("--rows must be greater than 0")

    generate_data(args.rows, args.seed, args.output)
