# Roadmap

Ordered by priority. A step starts only when the one before it gives a usable result.

## 1. Check the data (before writing any model code)

- [ ] Encode the CDCEF recession dates with their source.
- [ ] List candidate series and their start dates: GDP, industrial production, INSEE and Banque de France surveys, OAT and Bund yields, short-term rates, CAC 40, credit to firms.
- [ ] Check which of them have real-time vintages in the OECD revisions database and the Dallas Fed dataset.
- [ ] Record the publication delay of each series.
- [ ] Decide the start date of the sample from the results.

Exit: a table of series with source, start date, vintage status and publication lag.

## 2. Data pipeline

- [ ] Download scripts with a manifest (URL, date, checksum) for every raw file.
- [ ] Build a quarterly dataset as known at each forecast date.
- [ ] Data checks: no gaps, no future dates, publication lags applied.
- [ ] Lock file for dependencies.

## 3. Validation and baselines

- [ ] Walk-forward splitter with purging, and tests that prove no training target uses data from after the forecast date.
- [ ] Benchmarks: historical quantiles, quantile regression on past growth.
- [ ] Main baseline: quantile regression on all predictors.
- [ ] Evaluation: pinball loss, Kupiec and Christoffersen tests, the 5% quantile around each CDCEF recession.

Exit: a first results table that can be reproduced with one command.

## 4. Challenger model

- [ ] LightGBM with quantile loss, same splits and evaluation.
- [ ] Compare real-time and revised data on the same models.

## 5. Running it like a service

- [ ] Experiment tracking (MLflow).
- [ ] Scheduled run in GitHub Actions after each INSEE GDP release, storing the new vintage and the new forecasts.
- [ ] Monitoring of coverage over time and a short model card.

## Later

- Text feature from ECB speeches.
- Euro-area panel.
- Monthly version on industrial production.
