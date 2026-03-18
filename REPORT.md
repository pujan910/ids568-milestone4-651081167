# Milestone 4 Report

## 1. Overview
This project implements a distributed feature engineering pipeline using Ray. The goal was to process large scale synthetic transaction data (10M rows) and compare performance between local and distributed execution.

---

## 2. Data Generation
- Generated using generate_data.py
- Rows: 10,000,000
- Seed: 42 (for reproducibility)
- Format: Parquet

Columns:
- user_id
- transaction_amount
- transaction_type
- timestamp

---

## 3. Pipeline Design

### Local Execution
- Entire dataset processed on single machine
- Steps:
  - compute amount_squared
  - group by transaction_type
  - calculate mean

### Distributed Execution
- Dataset split into chunks
- Each chunk processed in parallel using Ray
- Each worker computes:
  - sum and count
- Final aggregation:
  - global mean = total sum / total count

This ensures deterministic and correct output.

---

## 4. Performance Comparison

| Metric | Local | Distributed |
|-------|------|------------|
| Runtime | ~0.4 sec | ~2.9 sec |
| Parallelism | 1 core | 4 workers |
| Data Size | 10M rows | 10M rows |

---

## 5. Analysis

- Local execution is faster because:
  - no scheduling overhead
  - no inter-process communication

- Distributed execution is slower because:
  - Ray startup overhead
  - task scheduling cost
  - data splitting overhead

- However, distributed approach is useful when:
  - dataset does not fit in memory
  - running on multi-node systems
  - scaling horizontally

---

## 6. Reliability & Cost Analysis

### Reliability
- Distributed systems allow:
  - task re-execution on failure
  - better fault tolerance
- But introduces complexity in debugging and coordination

### Cost
- Local:
  - low compute cost
  - simple execution

- Distributed:
  - higher compute cost (multiple workers)
  - communication overhead
  - potential network cost in real systems

### Trade-off
- small datasets → local is better
- large datasets → distributed becomes beneficial

---

## 7. Bottlenecks

- Ray initialization time
- overhead of splitting data
- communication between workers

---

## 8. Conclusion

- Local execution performs better for this dataset size
- Distributed processing introduces overhead but provides scalability
- Ray is effective for parallel feature engineering tasks
- This pipeline can scale to larger datasets or multi-node environments
