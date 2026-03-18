import argparse
import logging
import time
from pathlib import Path

import pandas as pd
import ray


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


def process_local(df: pd.DataFrame) -> pd.Series:
    df = df.copy()
    df["amount_squared"] = df["transaction_amount"] ** 2
    return df.groupby("transaction_type")["amount_squared"].mean()


@ray.remote
def process_chunk(df_chunk: pd.DataFrame) -> pd.DataFrame:
    df_chunk = df_chunk.copy()
    df_chunk["amount_squared"] = df_chunk["transaction_amount"] ** 2
    grouped = df_chunk.groupby("transaction_type")["amount_squared"].agg(["sum", "count"])
    return grouped


def process_distributed(df: pd.DataFrame, n_chunks: int) -> pd.Series:
    if n_chunks <= 0:
        raise ValueError("--chunks must be greater than 0")

    chunk_size = len(df) // n_chunks
    chunks = []

    for i in range(n_chunks):
        start_idx = i * chunk_size
        end_idx = len(df) if i == n_chunks - 1 else (i + 1) * chunk_size
        chunks.append(df.iloc[start_idx:end_idx])

    logging.info("Created %s chunks for distributed processing", len(chunks))

    futures = [process_chunk.remote(chunk) for chunk in chunks]
    results = ray.get(futures)

    combined = pd.concat(results)
    final_stats = combined.groupby(level=0).sum()
    final_result = final_stats["sum"] / final_stats["count"]
    return final_result


def run_pipeline(input_path: str, mode: str, n_chunks: int, output_path: str | None) -> None:
    input_obj = Path(input_path)

    if input_obj.is_dir():
        input_file = input_obj / "data.parquet"
    else:
        input_file = input_obj

    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")

    start = time.time()
    logging.info("Reading input from %s", input_file)
    df = pd.read_parquet(input_file)

    if mode == "local":
        logging.info("Running pipeline in local mode")
        result = process_local(df)
    elif mode == "distributed":
        logging.info("Running pipeline in distributed mode with %s chunks", n_chunks)
        ray.init(ignore_reinit_error=True)
        result = process_distributed(df, n_chunks)
    else:
        raise ValueError("Mode must be 'local' or 'distributed'.")

    end = time.time()

    print(f"Mode: {mode}")
    print("Final Result:")
    print(result)
    print(f"Execution Time: {end - start:.2f} seconds")

    if output_path:
        output_obj = Path(output_path)
        output_obj.mkdir(parents=True, exist_ok=True)
        result.to_csv(output_obj / "results.csv")
        logging.info("Saved results to %s", output_obj / "results.csv")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run local or distributed feature pipeline.")
    parser.add_argument("--input", type=str, default="data.parquet")
    parser.add_argument("--mode", type=str, default="distributed")
    parser.add_argument("--chunks", type=int, default=4)
    parser.add_argument("--output", type=str, default=None)

    args = parser.parse_args()

    run_pipeline(args.input, args.mode, args.chunks, args.output)



