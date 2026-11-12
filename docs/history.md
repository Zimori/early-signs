# How the project changed

The project has had three versions so far. Each section says what the plan was, what was wrong with it, and what carried over.

## Version 1: a US recession early-warning model (June 2026)

The first README asked how reliable economic indicators are as early warnings of recessions, and whether that reliability depends on the economic regime. The data was to come from FRED, with recessions dated by the NBER. The research questions are still in [scope.md](scope.md) under "Questions from version 1".

The question was a good one, but the setup was the most common student data project there is. US data from FRED with NBER dates is used by thousands of tutorials and Kaggle notebooks, so the project would not have stood out. It also had nothing to do with France, where I study and plan to work.

The "regime" idea also had a circularity problem. Regimes such as stagflation are usually defined from growth and inflation, which are the same indicators the model would use to predict recessions. Using them on both sides of the model needs care that the first draft did not have.

Carried over: the question of when indicators fail, and the plan to forecast at several horizons.

## Version 2: a French recession classifier (autumn 2026)

The second plan moved to France. Labels would come from the official French chronology published by the AFSE's business-cycle dating committee (CDCEF), predictors from INSEE and Banque de France series, and text features from Banque de France survey notes. Validation would use purged walk-forward cross-validation, so that overlapping forecast windows could not leak future information into training.

Checking the data showed that this could not produce meaningful results:

- The CDCEF dates five recessions since 1970: 1974-75, 1980, 1992-93, 2008-09 and 2020.
- The 2020 recession came from the pandemic. No macroeconomic indicator could have predicted it, so it does not test a forecasting model.
- With a ten-year minimum training window, the first test period starts in the mid-1980s. That leaves 1992-93 and 2008-09 as the only recessions a model could be tested on. An AUC or a Brier score computed on two events says very little.
- The text sources are shorter still. Banque de France survey reports are easy to find online from about 2014, and the ECB speeches dataset starts in 1997. Between them they cover at most one predictable recession.
- The plan described its data as "point-in-time", but the planned sources only return the latest revised values. Revisions to GDP and industrial production can be large around turning points, so that claim would not have held.

Carried over: the focus on France, the CDCEF chronology, and the leak-free walk-forward validation.

## Version 3: Growth-at-Risk (November 2026, current)

The current plan forecasts the distribution of future French GDP growth and focuses on its lower quantiles. The method comes from the Growth-at-Risk literature (Adrian, Boyarchenko and Giannone, 2019), which central banks and the IMF use to monitor downside risk.

Why this works better with French data:

- The target is continuous, so all of the roughly 200 quarters since the 1970s carry information. Five recessions are too few to train on, but they are enough to check against.
- The method is established and documented, which makes the results easy to compare with published work.
- Forecast quantiles can be backtested the same way banks backtest Value-at-Risk, with coverage tests that have known statistical properties.
- Real-time data exists for the main French series. The OECD has kept monthly vintages since 1999, and the Dallas Fed rebuilt earlier vintages from printed OECD publications. A 2025 OECD study on recession risk found that using real-time data changed its 2008 forecasts by 15 to 30 percentage points for several countries, so the effort is justified.

Dropped for now: text features. They can come back later as one more predictor, judged by whether they improve the quantile forecasts.

Possible extension: pooling several euro-area countries to get more downturns to evaluate on. The CEPR-EABCN committee publishes a euro-area chronology that would make this possible.
