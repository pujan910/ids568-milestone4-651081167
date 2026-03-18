import pandas as pd
import numpy as np
import argparse

def generate_data(n_rows, seed, output_file):
    np.random.seed(seed)

    df = pd.DataFrame({
        "user_id": np.random.randint(1, 100000, n_rows),
        "transaction_amount": np.random.uniform(1, 1000, n_rows),
        "transaction_type": np.random.choice(["purchase", "refund", "transfer"], n_rows),
        "timestamp": pd.date_range("2023-01-01", periods=n_rows, freq="s")
    })

    df.to_parquet(output_file)
    print(f"Generated {n_rows} rows and saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--rows", type=int, default=1000000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=str, default="data.parquet")

    args = parser.parse_args()

    generate_data(args.rows, args.seed, args.output)
