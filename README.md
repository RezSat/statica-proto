# Statica (prototype)

Statica: a small domain-specific language (DSL) for statistical analysis that
auto-generates human-readable conclusions and can ask for statistical table
values from the user when needed.

## Features
- load CSV datasets
- descriptive `describe`
- t-tests (one-sample, two-sample by group)
- linear regression (OLS) with summary
- plotting (histogram, scatter, box)
- `conclude` — template-based human-like conclusions
- `ask_table` — ask user for statistical table values if required

## Setup
1. Create and activate a Python 3.10+ virtualenv.
2. Install dependencies:
