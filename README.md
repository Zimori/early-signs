# Early Signs

Do the warning signs of a sharp slowdown in French growth hold up when you only use what was known at the time?

## Where the project stands

Early Signs began as a pipeline for testing economic early-warning signals without cheating: forecasts made walk-forward, with overlapping targets purged, on data as it was published at the time. The first target was a yes/no recession label, which turned out to be too rare in France to evaluate (five recessions since 1970, see [docs/history.md](docs/history.md)).

In October 2026 the Banque de France published Eco Notepad 468, *How can we anticipate extreme risks to growth in France?* (Fourel, Gauthier and Kerdelhué). It applies the Growth-at-Risk approach of Adrian, Boyarchenko and Giannone (2019) to France: instead of predicting average growth, it predicts the 5% quantile of future GDP growth, the bad outcome that happens one time in twenty. Its main finding is that private-sector debt and market uncertainty (the VIX) best predict downside risk one quarter ahead, while economic uncertainty and geopolitical risk matter at five years.

The note fits its models on the full sample since 1993, using today's revised data. That is the usual way to describe which indicators matter, and it is also exactly what the Early Signs pipeline was built to test. So the project now takes the note's question and runs it through that pipeline:

1. Replicate the note's results in-sample at both horizons (1 and 20 quarters), as a check that the data and code match.
2. Produce the same forecasts out of sample, walk-forward, so that each forecast only uses data from before its date.
3. Redo it with real-time data vintages instead of revised data.
4. Backtest the 5% quantile forecasts the way banks backtest Value-at-Risk.
5. See whether a gradient-boosted model adds anything over linear quantile regression.

If debt and the VIX still stand out at step 3, the note's finding holds up under a test it did not run itself. If they don't, that is worth knowing too.

## Approach

### Target

For a quarter $t$ and a horizon $h \in \{1, 4\}$ quarters, the target is the average annualised growth of real GDP between $t$ and $t+h$:

$$y_{t+h} = \frac{400}{h} \left( \ln \mathrm{GDP}_{t+h} - \ln \mathrm{GDP}_t \right)$$

We forecast the 5%, 25%, 50%, 75% and 95% quantiles of $y_{t+h}$. The note's second horizon, twenty quarters, is left out of the out-of-sample work: with a sample starting in 1993, five-year targets overlap so much that only a few independent observations would remain. It is still replicated in-sample.

The note doesn't define its target beyond an "average annual future growth rate", so the in-sample replication (step 3) is run twice. Once on quarter-on-quarter growth, which is the target above at $h = 1$ and the way INSEE reports growth (the script uses plain % change instead of $400 \ln$, which mostly changes the scale). And once on year-on-year growth, $100\,(\mathrm{GDP}_{t+1}/\mathrm{GDP}_{t-3} - 1)$, because of the variants I tried it is the closest to the note's coefficients (about −1.2 for corporate debt against "about 1 percentage point" in the note). Year-on-year is only there to compare with the note: three of its four quarterly changes are already in the predictors dated $t$, so last year's GDP growth predicts most of it by construction (flagged `mechanical` in `report/univariate_qr_h1_yoy.csv`). At twenty quarters there is one target, the average annual growth over the next five years, $100\,((\mathrm{GDP}_{t+20}/\mathrm{GDP}_t)^{1/5} - 1)$ (`report/univariate_qr_h20_avg_annual.csv`). Average quarterly growth gives the same ranking. The target has to end by 2020Q4, so forecast dates stop at 2015Q4, and p-values are left out because neighbouring targets share 19 of their 20 quarters.

### Predictors

The starting list follows the note, so that results can be compared:

- household and corporate debt as a share of GDP, and credit growth;
- market uncertainty (VIX) and financial stress (the ECB's CISS, which also stands in for the note's financial conditions index, not public for France);
- economic policy uncertainty (Baker, Bloom and Davis, 2016) and geopolitical risk (Caldara and Iacoviello, 2022);
- house prices, commodity prices and equity returns;
- current GDP growth.

Business surveys from INSEE and the Banque de France are added as a second step, since they are published early and are not revised.

### Data known at the time

Macroeconomic series get revised, sometimes by a lot around turning points. Debt ratios are affected twice, since both the debt figure and the GDP denominator change. The plan is to use real-time vintages where they exist: the OECD Original Release Data and Revisions Database (monthly vintages since 1999) and the Dallas Fed's real-time OECD dataset for earlier years. Market data such as the VIX are not revised and can be used as published. Where no vintage exists, the series is lagged by its publication delay and the results say so.

### Models

- Benchmark 1: the unconditional historical quantiles (what you would predict knowing nothing).
- Benchmark 2: quantile regression on past growth only.
- Main model: quantile regression with the selected predictors, including the LASSO-penalised version used in the note.
- Challenger: gradient-boosted trees with a quantile loss (LightGBM).

With about 130 quarters since 1993, the boosted model may well lose to the linear one. If so, the results will show it.

### Validation

Forecasts are produced with an expanding walk-forward window: train on everything up to quarter $t$, forecast $t+h$, move one quarter forward. For $h = 4$, consecutive targets overlap by three quarters, so the last $h-1$ training observations before each forecast date are dropped (purging, as described by López de Prado, 2018). Variable selection, including the LASSO penalty, is redone inside each training window. Tests will check that no training target uses data from after the forecast date.

### Evaluation

- Quantile (pinball) loss against the two benchmarks.
- Coverage: the 5% quantile should be breached about 5% of the time. This is tested with the Kupiec and Christoffersen tests used for Value-at-Risk backtesting.
- Comparison with the note: which predictors rank first in-sample, out of sample, and on real-time data.
- Event check: the path of the 5% quantile before the 2008-09 and 2020 recessions dated by the French business-cycle dating committee (CDCEF), with Covid reported separately.

## Data sources

| Source | What | Access |
|---|---|---|
| INSEE | Real GDP | insee.fr API |
| BIS | Debt-to-GDP (households, firms), credit gap, house prices | BIS API |
| OECD | House prices, price-to-rent, share prices, interest rates, GDP vintages since 1999 | OECD API |
| ECB | CISS financial stress indicator | ECB API |
| FRED | VIX, commodity prices, Brent oil, credit vintages since 2016 (ALFRED) | fred.stlouisfed.org |
| STOXX | VSTOXX | stoxx.com |
| Baker, Bloom and Davis; Caldara and Iacoviello | Policy uncertainty and geopolitical risk indices | policyuncertainty.com, matteoiacoviello.com |
| Dallas Fed | Real-time OECD vintages, 1962 to 1998 | dallasfed.org |
| AFSE (CDCEF) | Reference dates of French recessions | Committee press releases and Aviat et al. (2023) |

The exact series and their start dates are in [docs/data-map.md](docs/data-map.md). `src/fetch_raw.py` downloads everything into `data/raw/`, with the date in each file name and a manifest of URLs and checksums. `src/build_dataset.py` then rebuilds the quarterly table from those files, once as is and once with each series lagged by its publication delay.

## How the project changed

Early Signs started in June 2026 as a recession early-warning model on US data, became a French recession classifier with a leak-free validation pipeline, and took its current form after the Banque de France note of October 2026. Each change, and the reason for it: [docs/history.md](docs/history.md).

## References

- Adrian, T., Boyarchenko, N. and Giannone, D. (2019). Vulnerable Growth. *American Economic Review*, 109(4).
- Aviat, A., Bec, F., Diebolt, C., Doz, C., Ferrand, D., Ferrara, L., Heyer, E., Mignon, V. and Pionnier, P.-A. (2023). Les cycles économiques de la France : une datation de référence. *Revue économique*, 74.
- Baker, S., Bloom, N. and Davis, S. (2016). Measuring Economic Policy Uncertainty. *Quarterly Journal of Economics*, 131(4).
- Caldara, D. and Iacoviello, M. (2022). Measuring Geopolitical Risk. *American Economic Review*, 112(4).
- Christoffersen, P. (1998). Evaluating Interval Forecasts. *International Economic Review*, 39(4).
- Fourel, V., Gauthier, D. and Kerdelhué, L. (2026). How can we anticipate extreme risks to growth in France? Banque de France, Eco Notepad 468.
- Kupiec, P. (1995). Techniques for Verifying the Accuracy of Risk Measurement Models. *Journal of Derivatives*, 3(2).
- López de Prado, M. (2018). *Advances in Financial Machine Learning*.

## License

See [LICENSE](LICENSE).
