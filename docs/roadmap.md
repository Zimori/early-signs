# Roadmap

Only the first steps are planned in detail. Each one starts when the step before it gives a usable result, and what it finds can change the steps after it.

## 1. Check the data (before writing any model code)

- [ ] Map each predictor in Banque de France Eco Notepad 468 to a public series: debt-to-GDP for households and firms, credit gap, VIX, CISS, financial conditions index, policy uncertainty, geopolitical risk, house and commodity prices, equity returns.
- [ ] Record each series' source, start date and publication delay.
- [ ] Check which revised series (GDP, debt, credit) have real-time vintages in the OECD revisions database and the Dallas Fed dataset.
- [ ] Encode the CDCEF recession dates with their source.
- [ ] Decide what to do with predictors that have no public source: replace, approximate, or drop and say so.

Exit: a table of series with source, start date, vintage status and publication lag. If too many key predictors are missing, the plan gets revised here, before any code.

## 2. Data pipeline

- [ ] Download scripts with a manifest (URL, date, checksum) for every raw file.
- [ ] Build the quarterly dataset on revised data first.
- [ ] Data checks: no gaps, no future dates, publication lags applied.
- [ ] Replace the version-1 `requirements.txt` with the real dependencies and a lock file.

Exit: one command rebuilds the dataset from raw downloads.

## 3. Replicate the note in-sample

- [ ] One-quarter horizon: univariate quantile regressions at 5%, ranked by fit as in the note's Chart 1.
- [ ] LASSO-penalised quantile regression with current values and four lags, as in Chart 2.
- [ ] Write down where the results match the note and where they differ.

Exit: a replication table next to the note's chart.

## After that

The goal stays the one in the [README](../README.md): out-of-sample forecasts, real-time vintages, coverage backtests, and a boosted-tree challenger. How to get there will be planned once the replication works and the data's limits are known.
