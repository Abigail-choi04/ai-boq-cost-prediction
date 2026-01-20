import pandas as pd
import numpy as np

# Load real BOQ base data
real = pd.read_csv("data/boq_real_raw.csv")

N = 300   # number of synthetic BOQ projects
synthetic = []

# helper to add controlled variation
def vary(x, pct):
    return max(0, x * np.random.uniform(1 - pct, 1 + pct))

for _ in range(N):
    base = real.sample(1).iloc[0]

    # Realistic quantity variation (based on civil estimation practice)
    cement = vary(base["cement_cum"], 0.08)     # ±8%
    steel  = vary(base["steel_mt"], 0.10)       # ±10%
    bricks = vary(base["brickwork_cum"], 0.08)  # ±8%
    sand   = vary(base["sand_cum"], 0.12)       # ±12%
    labor  = vary(base["labor_cost"], 0.25)     # ±25%

    # Indian 2024–25 approximate unit rates
    CEMENT_RATE = 5500     # ₹ per m³
    STEEL_RATE  = 70000    # ₹ per MT
    BRICK_RATE  = 4500     # ₹ per m³
    SAND_RATE   = 900      # ₹ per m³

    # Cost computed using civil engineering pricing logic
    cost = (
        cement * CEMENT_RATE +
        steel  * STEEL_RATE +
        bricks * BRICK_RATE +
        sand   * SAND_RATE +
        labor
    )

    synthetic.append([
        cement,
        steel,
        bricks,
        sand,
        labor,
        cost
    ])

synthetic_df = pd.DataFrame(synthetic, columns=[
    "cement_cum",
    "steel_mt",
    "brickwork_cum",
    "sand_cum",
    "labor_cost",
    "total_cost"
])

synthetic_df.to_csv("data/boq_synthetic.csv", index=False)

print("Synthetic BOQ dataset created:", len(synthetic_df))
