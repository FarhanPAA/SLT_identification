# SLT (Single Lowest Tender) Calculator

A small Streamlit app and Python module to calculate the **SLT lower limit** and identify the winning bidder among responsive tenders.

## Requirements

- Python 3.12
- `uv`

## Setup (uv)

```powershell
uv python install 3.12
uv venv --python 3.12
uv sync
```

## Run the app

```powershell
uv run streamlit run interface.py
```

## Use the calculator in Python

```powershell
uv run python -c "from slt import compute_slt; print(compute_slt([100,110,120], 150, 0.9, [True,True,True]).lower_limit)"
```

