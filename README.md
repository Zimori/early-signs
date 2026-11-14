# Early Signs

Do the warning signs of a sharp slowdown in French growth hold up when you only use what was known at the time?

> Status: design stage. Nothing below is implemented yet. The plan and its order are in [docs/roadmap.md](docs/roadmap.md).

## Where the project stands

Early Signs began as a pipeline for testing economic early-warning signals without cheating: forecasts made walk-forward, with overlapping targets purged, on data as it was published at the time. The first target was a yes/no recession label, which turned out to be too rare in France to evaluate (five recessions since 1970, see [docs/history.md](docs/history.md)).

In October 2026 the Banque de France published Eco Notepad 468, *How can we anticipate extreme risks to growth in France?* (Fourel, Gauthier and Kerdelhué). It applies the Growth-at-Risk approach of Adrian, Boyarchenko and Giannone (2019) to France: instead of predicting average growth, it predicts the 5% quantile of future GDP growth, the bad outcome that happens one time in twenty. Its main finding is that private-sector debt and market uncertainty (the VIX) best predict downside risk one quarter ahead, while economic uncertainty and geopolitical risk matter at five years.

The note fits its models on the full sample since 1993, using today's revised data. That is the usual way to describe which indicators matter, and it is also exactly what the Early Signs pipeline was built to test. So the project now takes the note's question and runs it through that pipeline:

1. Replicate the note's one-quarter results in-sample, as a check that the data and code match.
2. Produce the same forecasts out of sample, walk-forward, so that each forecast only uses data from before its date.
3. Redo it with real-time data vintages instead of revised data.
4. Backtest the 5% quantile forecasts the way banks backtest Value-at-Risk.
5. See whether a gradient-boosted model adds anything over linear quantile regression.

If debt and the VIX still stand out at step 3, the note's finding holds up under a test it did not run itself. If they don't, that is worth knowing too.

## Approach

### Target

For a quarter $t$ and a horizon $h \in \{1, 4\}$ quarters, the target is the average annualised growth of real GDP between $t$ and $t+h$:

$$y_{t+h} = \frac{400}{h} \left( \ln \mathrm{GDP}_{t+h} - \ln \mathrm{GDP}_t \right)$$

We forecast the 5%, 25%, 50%, 75% and 95% quantiles of $y_{t+h}$. The note's second horizon, twenty quarters, is left out of the out-of-sample work: with a sample starting in 1993, five-year targets overlap so much that only a few independent observations would remain.

### Predictors

The starting list follows the note, so that results can be compared:

- household and corporate debt as a share of GDP, and credit growth;
- market uncertainty (VIX) and financial stress (the ECB's CISS);
- a financial conditions index;
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
| INSEE | Quarterly national accounts, business surveys | `pynsee`, DBnomics |
| Banque de France | Credit and debt, interest rates, business surveys | Webstat, DBnomics |
| ECB | CISS financial stress indicator | ECB Data Portal |
| CBOE | VIX | public download |
| Baker, Bloom and Davis; Caldara and Iacoviello | Policy uncertainty and geopolitical risk indices | policyuncertainty.com, matteoiacoviello.com |
| OECD | Real-time vintages since 1999 | OECD Data Explorer |
| Dallas Fed | Real-time OECD vintages, 1962 to 1998 | dallasfed.org |
| AFSE (CDCEF) | Reference dates of French recessions | Committee press releases and Aviat et al. (2023) |

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
