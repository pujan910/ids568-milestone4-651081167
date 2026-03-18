import argparse
import time
import pandas as pd
import ray


def process_local(df):
    df = df.copy()
    df["amount_squared"] = df["transaction_amount"] ** 2
    return df.groupby("transaction_type")["amount_squared"].mean()


@ray.remote
def process_chunk(df_chunk):
    df_chunk = df_chunk.copy()
    df_chunk["amount_squared"] = df_chunk["transaction_amount"] ** 2
    grouped = df_chunk.groupby("transaction_type")["amount_squared"].agg(["sum", "count"])
    return grouped


def process_distributed(df, n_chunks):
    chunk_size = len(df) // n_chunks
    chunks = []

    for i in range(n_chunks):
        start_idx = i * chunk_size
        end_idx = len(df) if i == n_chunks - 1 else (i + 1) * chunk_size
        chunks.append(df.iloc[start_idx:end_idx])

    futures = [process_chunk.remote(chunk) for chunk in chunks]
    results = ray.get(futures)

    combined = pd.concat(results)
    final_stats = combined.groupby(level=0).sum()
    final_result = final_stats["sum"] / final_stats["count"]
    return final_result


def run_pipeline(input_file, mode, n_chunks):
    start = time.time()
    df = pd.read_parquet(input_file)

    if mode == "local":
        result = process_local(df)
    elif mode == "distributed":
        ray.init(ignore_reinit_error=True)
        result = process_distributed(df, n_chunks)
    else:
        raise ValueError("Mode must be 'local' or 'distributed'.")

    end = time.time()

    print(f"Mode: {mode}")
    print("Final Result:")
    print(result)
    print(f"Execution Time: {end - start:.2f} seconds")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, default="data.parquet")
    parser.add_argument("--mode", type=str, default="distributed")
    parser.add_argument("--chunks", type=int, default=4)

    args = parser.parse_args()

    run_pipeline(args.input, args.mode, args.chunks)







