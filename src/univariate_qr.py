# Step 3, first part: one 5% quantile regression per predictor, 1 quarter ahead,
# on revised data, ranked by pinball loss against a model with no predictor.
# Transforms follow the note's charts (see docs/data-map.md).
# Run from the repo root: python src/univariate_qr.py

import pandas as pd
import statsmodels.api as sm

QUANTILE = 0.05
FIRST, LAST = "1993Q1", "2020Q4"  # the note's charts stop in 2020

data = pd.read_csv("data/processed/quarterly_revised.csv", index_col="quarter")
data.index = pd.PeriodIndex(data.index, freq="Q")


def quarterly_change(name):
    return data[name].diff()


def annual_growth(name):
    return 100 * data[name].pct_change(4, fill_method=None)


gdp_growth = 100 * data["gdp"].pct_change(fill_method=None)

predictors = {
    "gdp_growth": gdp_growth,
    "gdp_growth_annual": annual_growth("gdp"),
    "credit_private_gdp (q change)": quarterly_change("credit_private_gdp"),
    "credit_households_gdp (q change)": quarterly_change("credit_households_gdp"),
    "credit_corporates_gdp (q change)": quarterly_change("credit_corporates_gdp"),
    "credit_gap": data["credit_gap"],
    "vix": data["vix"],
    "ciss (q change)": quarterly_change("ciss"),
    "house_prices (annual)": annual_growth("house_prices"),
    "price_to_rent (annual)": annual_growth("price_to_rent"),
    "commodities (annual)": annual_growth("commodities"),
    "brent (annual)": annual_growth("brent"),
    "shares_france (annual)": annual_growth("shares_france"),
    "shares_euro_area (annual)": annual_growth("shares_euro_area"),
    "shares_us (annual)": annual_growth("shares_us"),
    "epu_france (annual)": annual_growth("epu_france"),
    "gpr": data["gpr"],
    "gpr_france": data["gpr_france"],
    "rate_3m": data["rate_3m"],
    "rate_10y": data["rate_10y"],
}
# left out: vstoxx starts in 1999 and is only in the note at 20 quarters

# target dated t = GDP growth in t+1, predictors dated t
table = pd.DataFrame(predictors)
table["target"] = gdp_growth.shift(-1)
table = table.loc[FIRST:LAST]
table = table[table.index <= pd.Period(LAST, freq="Q") - 1]  # target must be inside the sample
assert table.notna().all().all(), table.columns[table.isna().any()].tolist()
y = table["target"]


def pinball(y, fitted):
    error = y - fitted
    return (error * (QUANTILE - (error < 0))).mean()


baseline = sm.QuantReg(y, pd.Series(1.0, index=y.index)).fit(q=QUANTILE)
baseline_loss = pinball(y, baseline.fittedvalues)

rows = []
for name in predictors:
    x = sm.add_constant(table[name])
    fit = sm.QuantReg(y, x).fit(q=QUANTILE)
    loss = pinball(y, fit.fittedvalues)
    # the baseline is nested in every model, so in-sample it can't do better
    assert loss <= baseline_loss + 1e-9, name
    rows.append({
        "predictor": name,
        "coef": fit.params[name],
        "p_value": fit.pvalues[name],
        "pinball": loss,
        "gain_vs_baseline_%": 100 * (1 - loss / baseline_loss),
    })

results = pd.DataFrame(rows).sort_values("pinball").reset_index(drop=True)
results.index += 1

print(f"sample: {y.index[0]} to {y.index[-1]} ({len(y)} quarters), quantile {QUANTILE}, h=1")
print(f"baseline (no predictor): 5% quantile {baseline.params.iloc[0]:.2f} pp, pinball {baseline_loss:.4f}")
print(results.round(4).to_string())
results.to_csv("report/univariate_qr_h1.csv", index_label="rank")
