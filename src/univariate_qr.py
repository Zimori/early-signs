# Step 3, first part: one 5% quantile regression per predictor, 1 and 20 quarters
# ahead, on revised data, ranked by pinball loss against a model with no predictor.
# At 1 quarter, two targets, one CSV each: q-on-q GDP growth one quarter ahead (the
# project's target) and year-on-year growth (only to compare with the note, see README).
# At 20 quarters, one target: average annual growth over the next 5 years, the note's
# wording. Average q-on-q growth gives the same ranking, about 4 times smaller.
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
# left out: vstoxx is in the note at 20 quarters, but starts in 1999, so its loss
# would come from a shorter sample and couldn't be ranked with the others


def pinball(y, fitted):
    error = y - fitted
    return (error * (QUANTILE - (error < 0))).mean()


# target dated t = GDP growth after t, predictors dated t
targets = [
    (1, "qoq", gdp_growth.shift(-1)),
    (1, "yoy", annual_growth("gdp").shift(-1)),
    (20, "avg_annual", 100 * ((data["gdp"].shift(-20) / data["gdp"]) ** (1 / 5) - 1)),
]

for h, target_name, target in targets:
    table = pd.DataFrame(predictors)
    table["target"] = target
    table = table.loc[FIRST:LAST]
    table = table[table.index <= pd.Period(LAST, freq="Q") - h]  # target must be inside the sample
    assert table.notna().all().all(), table.columns[table.isna().any()].tolist()
    y = table["target"]

    baseline = sm.QuantReg(y, pd.Series(1.0, index=y.index)).fit(q=QUANTILE)
    baseline_loss = pinball(y, baseline.fittedvalues)

    rows = []
    for name in predictors:
        x = sm.add_constant(table[name])
        # default is 1000 steps, credit gap with the y/y target needs about 1600
        fit = sm.QuantReg(y, x).fit(q=QUANTILE, max_iter=5000)
        loss = pinball(y, fit.fittedvalues)
        # the baseline is nested in every model, so in-sample it can't do better
        assert loss <= baseline_loss + 1e-9, name
        rows.append({
            "predictor": name,
            "coef": fit.params[name],
            # 20-quarter targets overlap by 19 quarters, so the p-value is meaningless there
            "p_value": fit.pvalues[name] if h == 1 else None,
            "pinball": loss,
            "gain_vs_baseline_%": 100 * (1 - loss / baseline_loss),
            # y/y target shares 3 of its 4 quarters with this predictor, so it wins by construction
            "mechanical": target_name == "yoy" and name == "gdp_growth_annual",
        })

    results = pd.DataFrame(rows).sort_values("pinball").reset_index(drop=True)
    results.index += 1

    print(f"\ntarget {target_name}, sample: {y.index[0]} to {y.index[-1]} ({len(y)} quarters), quantile {QUANTILE}, h={h}")
    print(f"baseline (no predictor): 5% quantile {baseline.params.iloc[0]:.2f} pp, pinball {baseline_loss:.4f}")
    print(results.round(4).to_string())
    results.to_csv(f"report/univariate_qr_h{h}_{target_name}.csv", index_label="rank")
