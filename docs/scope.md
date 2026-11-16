# Scope

## Research questions

1. Can the results of Banque de France Eco Notepad 468, at 1 and 20 quarters, be reproduced in-sample from public data?
2. Do the predictors the note ranks first (household and corporate debt, the VIX) still lead when the 5% quantile is forecast out of sample, walk-forward?
3. How much do the forecasts and the ranking change when real-time vintages replace today's revised data?
4. Are the 5% quantile forecasts calibrated? Out of sample, is growth below the forecast about 5% of the time, and are the breaches spread out rather than bunched together?
5. Does a gradient-boosted model improve on linear quantile regression with about 130 quarterly observations?
6. Did the 5% quantile fall before the 2008-09 recession dated by the CDCEF, and how many quarters ahead?

## In scope

- France, quarterly frequency, from 1993 to match the note. A longer sample from the 1970s can be tried for the predictors that go back that far.
- Horizons of one and four quarters.
- Quantile forecasts at 5%, 25%, 50%, 75% and 95%.
- The note's predictors first, business surveys second.
- Real-time vintages for GDP and other revised series where they exist.
- A reproducible pipeline: data download, versioned snapshots, training, evaluation report.

## Out of scope for now

- The note's five-year horizon out of sample (too few independent observations since 1993). It is replicated in-sample only.
- Text features from central-bank communication. They can be added later as a predictor.
- Other countries. A euro-area panel is a possible extension.
- Monthly forecasts.
- A yes/no recession classifier (see [history.md](history.md) for why).

## Definitions

- **Quantile forecast.** The value the target should fall below with a given probability. A 5% quantile of -1% means a one-in-twenty chance that growth comes in under -1%.
- **Growth-at-Risk.** The lower quantile (usually 5%) of the forecast distribution of GDP growth.
- **In-sample / out-of-sample.** In-sample results come from a model fitted on the whole period, including the quarters it is judged on. Out-of-sample forecasts are made with a model that has only seen earlier data.
- **Vintage.** A copy of a data series as it was published on a given date, before later revisions.
- **Purging.** Removing training observations whose target window overlaps with the forecast date, so the model never trains on outcomes it should not know yet.
- **Coverage test.** A check that a quantile forecast is breached as often as it should be. The Kupiec test looks at the breach rate; the Christoffersen test also checks that breaches are independent over time.

## Risks

- Replication gap: the note does not list exact series codes or transformations. Small differences are expected; the comparison is on rankings and signs more than on exact values.
- Small sample: about 130 quarters since 1993 is little for a tree model, and the out-of-sample period is shorter still. The evaluation has to be honest about uncertainty.
- Vintage coverage: real-time data may not exist for every predictor. Each series will be labelled as real-time, lagged by its publication delay, or revised.
- Structural change: the euro (1999), the 2008 crisis and Covid all changed how the economy behaves. Results will be reported by sub-period as well as in total.
- Quantile crossing: separately estimated quantiles can cross (a 5% forecast above the 25% one). They will be sorted after estimation, which is the standard fix.

## Questions from version 1

These were the original questions. The first two became questions 2 and 6 above; the regime question is not covered by the current plan.

- Which economic indicators are most predictive of a recession?
- How far in advance can we predict a recession using these indicators?
- What are the limitations of using economic indicators for recession prediction?
- When do they fail? Are there specific economic regimes where they are more or less effective?
