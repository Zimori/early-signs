# Roadmap

Only the first steps are planned in detail. Each one starts when the step before it gives a usable result, and what it finds can change the steps after it.

## 1. Check the data (before writing any model code)

- [x] Map each predictor in Banque de France Eco Notepad 468 to a public series: debt-to-GDP for households and firms, credit gap, VIX, CISS, financial conditions index, policy uncertainty, geopolitical risk, house and commodity prices, equity returns.
- [x] Record each series' source and start date ([data-map.md](data-map.md)).
- [x] Measure each series' publication delay (can finish during step 2). Done in whole quarters from the 15 Nov snapshot: [publication_lags.csv](../data/reference/publication_lags.csv).
- [x] Check which revised series (GDP, debt, credit) have real-time vintages in the OECD revisions database and the Dallas Fed dataset.
- [x] Encode the CDCEF recession dates with their source. Covid trough still to check.
- [x] Decide what to do with predictors that have no public source: replace, approximate, or drop and say so ([data-map.md](data-map.md), gaps and decisions).

Exit: a table of series with source, start date, vintage status and publication lag. If too many key predictors are missing, the plan gets revised here, before any code.

## 2. Data pipeline

- [x] Download scripts with a manifest (URL, date, checksum) for every raw file (`data/raw/manifest_<date>.csv`).
- [x] Build the quarterly dataset on revised data first (`src/build_dataset.py`, levels only for now).
- [x] Data checks: no gaps, no future dates, publication lags applied (asserts in `src/build_dataset.py`).
- [x] Replace the version-1 `requirements.txt` with the real dependencies and a lock file (`requirements-lock.txt`).

Exit: one command rebuilds the dataset from raw downloads.

## 3. Replicate the note in-sample

- [x] Univariate quantile regressions at 5%, at 1 quarter, ranked by fit as in the note's Chart 1 (`src/univariate_qr.py`). Run on two targets, since the note doesn't define its own (see the [README](../README.md#target)).
- [ ] The same at 20 quarters (in-sample only, see [scope](scope.md)).
- [ ] LASSO-penalised quantile regression with current values and four lags, at both horizons, as in Chart 2.
- [ ] Write down where the results match the note and where they differ.

Exit: a replication table next to the note's chart.

## After that

The goal stays the one in the [README](../README.md): out-of-sample forecasts, real-time vintages, coverage backtests, and a boosted-tree challenger. How to get there will be planned once the replication works and the data's limits are known.
