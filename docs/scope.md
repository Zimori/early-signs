# Scope

## Research questions

1. How much do financial conditions and business surveys shift the lower quantiles of French GDP growth one and four quarters ahead, compared with past growth alone?
2. Are the 5% quantile forecasts calibrated? Out of sample, is growth below the forecast about 5% of the time, and are the breaches spread out rather than bunched together?
3. Did the lower quantiles fall before the recessions dated by the CDCEF, and how many quarters ahead?
4. Does a gradient-boosted model improve on linear quantile regression with about 200 quarterly observations?
5. How different are the forecasts when they are made with the data available at the time instead of today's revised data?

## In scope

- France, quarterly frequency, from the 1970s (or later, depending on which predictors go back that far).
- Horizons of one and four quarters.
- Quantile forecasts at 5%, 25%, 50%, 75% and 95%.
- Real-time vintages for GDP and other revised series where they exist.
- A reproducible pipeline: data download, versioned snapshots, training, evaluation report.

## Out of scope for now

- Text features from central-bank communication. They can be added later as a predictor.
- Other countries. A euro-area panel is a possible extension.
- Monthly forecasts. Industrial production could support a monthly version later.
- A yes/no recession classifier (see [history.md](history.md) for why).

## Definitions

- **Quantile forecast.** The value the target should fall below with a given probability. A 5% quantile of -1% means a one-in-twenty chance that growth comes in under -1%.
- **Growth-at-Risk.** The lower quantile (usually 5%) of the forecast distribution of GDP growth.
- **Vintage.** A copy of a data series as it was published on a given date, before later revisions.
- **Purging.** Removing training observations whose target window overlaps with the forecast date, so the model never trains on outcomes it should not know yet.
- **Coverage test.** A check that a quantile forecast is breached as often as it should be. The Kupiec test looks at the breach rate; the Christoffersen test also checks that breaches are independent over time.

## Risks

- Small sample: about 200 quarters is little for a tree model. Linear quantile regression may be the best model, and the evaluation has to be honest about uncertainty.
- Vintage coverage: real-time data may not exist for every predictor. Each series will be labelled as real-time, lagged by its publication delay, or revised.
- Structural change: the economy of the 1970s differs from today's, and the euro changed monetary policy in 1999. Results will be reported by sub-period as well as in total.
- Quantile crossing: separately estimated quantiles can cross (a 5% forecast above the 25% one). They will be sorted after estimation, which is the standard fix.

## Questions from version 1

These were the original questions. The first two are close to questions 1 and 3 above; the regime question is not covered by the current plan.

- Which economic indicators are most predictive of a recession?
- How far in advance can we predict a recession using these indicators?
- What are the limitations of using economic indicators for recession prediction?
- When do they fail? Are there specific economic regimes where they are more or less effective?
