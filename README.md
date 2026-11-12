# Early Signs

Growth-at-Risk for the French economy: how bad could growth get over the next quarters, and how early can we tell?

> Status: design stage. Nothing below is implemented yet. The plan and its order are in [docs/roadmap.md](docs/roadmap.md).

## The question

Most recession models answer a yes/no question: will there be a recession in the next 12 months? For France that question is hard to test. The official chronology lists five recessions since 1970, and one of them (Covid) was an outside shock that no economic indicator could see coming. A classifier trained and evaluated on so few events produces scores that mostly reflect luck.

This project asks a different question, borrowed from central-bank work on Growth-at-Risk (Adrian, Boyarchenko and Giannone, 2019): given what was known at the end of a quarter, what does the distribution of French GDP growth look like over the next one and four quarters, and in particular its left tail? A 5% quantile is the growth rate we expect to fall below one time in twenty. If that number turns negative, the economy is at risk, whether or not a recession follows.

With this framing every quarter since the 1970s is an observation. The five dated recessions stay in the project as a check: did the lower quantiles drop before them?

## Approach

### Target

For a quarter $t$ and a horizon $h \in \{1, 4\}$ quarters, the target is the average annualised growth of real GDP between $t$ and $t+h$:

$$y_{t+h} = \frac{400}{h} \left( \ln \mathrm{GDP}_{t+h} - \ln \mathrm{GDP}_t \right)$$

We forecast the 5%, 25%, 50%, 75% and 95% quantiles of $y_{t+h}$.

### Predictors

Three groups, chosen because the Growth-at-Risk literature finds that financial conditions move the left tail much more than the median:

- current activity: past GDP growth, industrial production;
- business surveys: INSEE and Banque de France business-climate indices;
- financial conditions: the slope of the French yield curve, the OAT-Bund spread, equity returns and volatility, credit growth.

Which series go in depends on how far back each one goes. That check is the first step of the roadmap.

### Data known at the time

Macroeconomic series get revised, sometimes by a lot. Training on today's revised GDP to predict what forecasters could have known in 2008 is a form of look-ahead bias. The plan is to use real-time vintages where they exist: the OECD Original Release Data and Revisions Database (monthly vintages since 1999) and the Dallas Fed's real-time OECD dataset for earlier years. Market data such as yields and equity prices are not revised and can be used as published. Where no vintage exists, the series is lagged by its publication delay and the README will say so.

### Models

- Benchmark 1: the unconditional historical quantiles (what you would predict knowing nothing).
- Benchmark 2: quantile regression on past growth only.
- Main baseline: linear quantile regression on all predictor groups, as in the original Growth-at-Risk papers.
- Challenger: gradient-boosted trees with a quantile loss (LightGBM).

With roughly 200 quarters of data, the boosted model may not beat the linear one. If so, the results will show it.

### Validation

Forecasts are produced with an expanding walk-forward window: train on everything up to quarter $t$, forecast $t+h$, move one quarter forward. For $h = 4$, consecutive targets overlap by three quarters, so the last $h-1$ training observations before each forecast date are dropped (purging, as described by López de Prado, 2018). Tests will check that no training target uses data from after the forecast date.

### Evaluation

- Quantile (pinball) loss against the two benchmarks.
- Coverage: the 5% quantile should be breached about 5% of the time. This is tested the way banks backtest Value-at-Risk, with the Kupiec and Christoffersen tests.
- Event check: the path of the 5% quantile before each recession dated by the French business-cycle dating committee (CDCEF), with Covid reported separately.

## Data sources

| Source | What | Access |
|---|---|---|
| INSEE | Quarterly national accounts, industrial production, business surveys | `pynsee`, DBnomics |
| Banque de France | Business surveys, credit, interest rates | Webstat, DBnomics |
| OECD | Real-time vintages since 1999 | OECD Data Explorer |
| Dallas Fed | Real-time OECD vintages, 1962 to 1998 | dallasfed.org |
| AFSE (CDCEF) | Reference dates of French recessions | Committee press releases and Aviat et al. (2023) |

## How the project changed

Early Signs started in June 2026 as a recession early-warning model on US data, became a French recession classifier, and was then reframed as Growth-at-Risk in November 2026. Each change, and the reason for it, is written up in [docs/history.md](docs/history.md).

## References

- Adrian, T., Boyarchenko, N. and Giannone, D. (2019). Vulnerable Growth. *American Economic Review*, 109(4).
- Aviat, A., Bec, F., Diebolt, C., Doz, C., Ferrand, D., Ferrara, L., Heyer, E., Mignon, V. and Pionnier, P.-A. (2023). Les cycles économiques de la France : une datation de référence. *Revue économique*, 74.
- Christoffersen, P. (1998). Evaluating Interval Forecasts. *International Economic Review*, 39(4).
- Kupiec, P. (1995). Techniques for Verifying the Accuracy of Risk Measurement Models. *Journal of Derivatives*, 3(2).
- López de Prado, M. (2018). *Advances in Financial Machine Learning*. Wiley.

## License

See [LICENSE](LICENSE).
