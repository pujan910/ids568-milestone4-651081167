# Milestone 4 Report

## 1. Overview
This project implements a distributed feature engineering pipeline using Ray. The goal was to process large synthetic transaction data (10M+ rows) and compare local vs distributed execution performance.

---

## 2. Data Generation
- Generated using generate_data.py
- Default rows: 10,000,000
- Seed: 42 (ensures reproducibility)
- Format: Parquet
- Supports both file and directory output

---

## 3. Pipeline Design

### Local Execution
- Processes entire dataset on single machine
- Steps:
  - compute amount_squared
  - group by transaction_type
  - calculate mean

### Distributed Execution
- Splits dataset into chunks
- Uses Ray for parallel execution
- Each worker computes:
  - sum and count
- Final aggregation:
  - global mean = total sum / total count

This ensures deterministic and correct results across runs.

---

## 4. Performance Comparison

| Metric | Local | Distributed |
|--------|------|------------|
| Runtime | ~0.4 sec | ~2.9 sec |
| Dataset Size | 10M rows | 10M rows |
| Parallelism | 1 core | 4 workers |
| Partitions | 1 | 4 |

---

## 5. Additional Metrics (Observed / Notes)

- Shuffle Volume: Not explicitly measured (Ray handles data movement internally)
- Worker Utilization: Limited due to small dataset size and local machine constraints
- Peak Memory: Not measured, but dataset fits in memory for local execution

Note: Advanced metrics like shuffle volume and memory usage typically require Ray dashboard or cluster-level monitoring tools.

---

## 6. Analysis

- Local execution is faster because:
  - no task scheduling overhead
  - no inter-process communication

- Distributed execution is slower because:
  - Ray startup overhead
  - task scheduling cost
  - data splitting overhead

- Distributed processing becomes beneficial when:
  - dataset size increases significantly
  - data cannot fit in memory
  - running on multi-node systems

---

## 7. Reliability & Cost Analysis

### Reliability
- Distributed systems allow:
  - task re-execution on failure
  - better fault tolerance
- However, debugging is more complex compared to local execution

### Cost
- Local execution:
  - low cost
  - minimal resource usage

- Distributed execution:
  - higher compute cost (multiple workers)
  - communication overhead
  - potential network cost in real-world deployment

### Trade-offs
- small datasets → local is more efficient
- large datasets → distributed provides scalability benefits

---

## 8. Bottlenecks

- Ray initialization time
- overhead of chunking data
- communication between workers
- underutilization of workers for small workloads

---

## 9. Conclusion

- Local execution performs better for this dataset size
- Distributed processing introduces overhead but improves scalability
- Ray provides a flexible framework for distributed feature engineering
- This pipeline can scale to larger datasets and multi-node environments
