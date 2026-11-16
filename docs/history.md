# How the project changed

The project has had three versions so far. Each section says what the plan was, what was wrong with it, and what carried over.

## Version 1: a US recession early-warning model (June 2026)

The first README asked how reliable economic indicators are as early warnings of recessions, and whether that reliability depends on the economic regime. The data was to come from FRED, with recessions dated by the NBER. The research questions are still in [scope.md](scope.md) under "Questions from version 1".

The question wasn't necessarily uninteresting, but I realized it's an extremely common student data project, not particularly innovative. US data from FRED with NBER dates is used by thousands of tutorials and Kaggle notebooks, so the project would not have stood out. I also had little intuition for the US economy, the project would have been a long way from my own experience.

The "regime" idea also had a circularity problem. Regimes such as "stagflation" are usually defined from growth and inflation, which are the same indicators the model would use to predict recessions. Using them on both sides of the model needs care that the first draft did not have.

Carried over: the question of when indicators fail, and the plan to forecast at several horizons.

## Version 2: a French recession classifier (autumn 2026)

The move to France started with my Machine Learning Techniques and Applications (MLTA) teacher. He asked to see me at the end of a class, and we talked about what I was interested in. I told him about the recession model, which at that point was a general idea and a list of research questions with little structure. The next week he asked how it was going. Honestly, not much had happened: every paper I read covered the same ground, the subject was already very well documented, and I had lost motivation and moved on to other things.

During a lab session he took some time to draw on the board the problem he thought I would run into, and a different direction. His idea was to work with documents in French and to build a benchmark for evaluating models on them. French gets far less attention than English, so there is less competition, and multilingual work is a real challenge: a model that performs well in English does not necessarily perform as well in French. He offered to help me formulate the project, by email or through questions in a shared Google Doc.

The second plan kept the French focus and the French-language text, though as a source of predictors rather than as a benchmark. Labels would come from the official French chronology published by the AFSE's business-cycle dating committee (CDCEF), predictors from INSEE and Banque de France series, and text features from Banque de France survey notes. Validation would use purged walk-forward cross-validation, so that overlapping forecast windows could not leak future information into training.

Checking the data showed that this could not produce meaningful results:

- The CDCEF dates five recessions since 1970: 1974-75, 1980, 1992-93, 2008-09 and 2020.
- The 2020 recession came from the pandemic. No macroeconomic indicator could have predicted it, so it does not test a forecasting model.
- With a ten-year minimum training window, the first test period starts in the mid-1980s. That leaves 1992-93 and 2008-09 as the only recessions a model could be tested on. An AUC or a Brier score computed on two events says very little.
- The text sources are shorter still. Banque de France survey reports are easy to find online from about 2014, and the ECB speeches dataset starts in 1997. Between them they cover at most one predictable recession.
- The plan described its data as "point-in-time", but the planned sources only return the latest revised values. Revisions to GDP and industrial production can be large around turning points, so that claim would not have held.

Carried over: the focus on France, the CDCEF chronology, and the leak-free walk-forward validation.

## Version 3: testing the Banque de France's Growth-at-Risk findings (November 2026, current)

Version 2 left a validation pipeline with no usable target. The answer came from the Growth-at-Risk literature (Adrian, Boyarchenko and Giannone, 2019), which forecasts the lower quantiles of future GDP growth instead of a recession label. Central banks and the IMF use it to monitor downside risk.

On 23 October 2026 the Banque de France published Eco Notepad 468, *How can we anticipate extreme risks to growth in France?* It applies Growth-at-Risk to French GDP since 1993 with about thirty predictors, first one at a time and then together in a LASSO-penalised quantile regression. One quarter ahead, household and corporate debt and the VIX come out as the best predictors of the 5% quantile. Five years ahead, economic uncertainty and geopolitical risk do.

The note answers the question version 2 was asking, for France and with a target that works. What it does not do is test its answer the way version 2 was designed to: its models are fitted on the whole sample, on today's revised data, and it reports no out-of-sample forecasts or coverage tests. That's normal for a short note, so this project starts from its setup and checks whether the findings hold when each forecast only uses the data available on its date.

Why this works better than version 2:

- The target is continuous, so every quarter carries information. The recessions are too few to train on, but they are enough to check against.
- A published result exists to replicate first. If the in-sample numbers match the note, the data and code are probably right before any new claim is made.
- Forecast quantiles can be backtested the same way banks backtest Value-at-Risk, with coverage tests that have known statistical properties.
- Real-time data exists for French GDP: OECD monthly vintages since 1999, and Dallas Fed vintages rebuilt from printed OECD publications before that. It matters: in an OECD recession model, redoing the June 2008 forecasts with today's data raised recession probabilities by 15 to 30 points for seven countries, and France is one of the three countries where the vintage changes results most ([Chalaux, Turner and Cassimon, 2025](https://doi.org/10.1787/46880adc-en), pp. 26–27). Debt is only half covered: I found no debt vintages before 2016, so before then only the GDP part of debt-to-GDP is real-time (see [data-map.md](data-map.md)).

Other work on the same question: the IMF did an in-sample Growth-at-Risk for France in 2019, to size a bank stress test ([Country Report 19/322](https://www.imf.org/en/publications/cr/issues/2019/10/28/france-financial-sector-assessment-program-technical-note-risk-analysis-of-banking-and-48758), Appendix V). An ECB paper forecasts it out of sample for euro-area countries including France, but without real-time vintages or coverage tests ([Lang, Rusnák and Greiwe, 2023](https://econpapers.repec.org/RePEc:ecb:ecbwps:20232808)). [Ferrara, Mogliani and Sahuc (2020)](https://crawford.anu.edu.au/sites/default/files/2025-05/97_2020_Ferrara_Mogliani_Sahuc.pdf) use real-time GDP vintages, but for the euro area as a whole. None of these, as far as I found, tests French Growth-at-Risk out of sample on real-time vintages with coverage backtests.

Dropped for now: text features, and with them the French-language angle from version 2. They can come back later as one more predictor, judged by whether they improve the quantile forecasts.

Possible extension: pooling several euro-area countries to get more downturns to evaluate on. The CEPR-EABCN committee publishes a euro-area chronology that would make this possible.
