# Builds one quarterly table from the newest raw files in data/raw/ (revised data).
# Only levels for now, growth rates and lags come later with the models.
# Daily and monthly series are averaged over each quarter.
# Run from the repo root: python src/build_dataset.py

import glob
import os
import xml.etree.ElementTree as ET

import pandas as pd


def newest_file(name):
    # names end with the download date, so the last one after sorting is the newest
    files = sorted(glob.glob(f"data/raw/{name}_*"))
    if len(files) == 0:
        print("missing raw file for", name, "-> run src/fetch_raw.py first")
        exit(1)
    return files[-1]


def to_quarter(period):
    # BIS/OECD periods look like "1969-Q4" (quarterly) or "1955-01" (monthly)
    if "Q" in period:
        return pd.Period(period, freq="Q")
    month = pd.Period(period, freq="M")
    return month.asfreq("Q")


# column name -> raw file name, grouped by file format
bis_oecd = {
    "credit_private_gdp": "bis_credit_private",
    "credit_households_gdp": "bis_credit_households",
    "credit_corporates_gdp": "bis_credit_corporates",
    "credit_gap": "bis_credit_gap",
    "house_prices_bis": "bis_house_prices",
    "house_prices": "oecd_house_prices",
    "price_to_rent": "oecd_price_to_rent",
    "shares_france": "oecd_shares_france",
    "shares_euro_area": "oecd_shares_euro_area",
    "shares_us": "oecd_shares_us",
    "rate_3m": "oecd_rate_3m",
    "rate_10y": "oecd_rate_10y",
}
fred = {
    "vix": "fred_vix",
    "commodities": "fred_commodities",
    "brent": "fred_brent_monthly",
}
# TODO: EPU (xlsx) and GPR (xls), need openpyxl and xlrd

columns = {}

# GDP from INSEE, only comes as xml (real GDP, millions of euros, chained)
root = ET.parse(newest_file("insee_gdp")).getroot()
gdp = {}
for obs in root.iter("Obs"):
    gdp[to_quarter(obs.get("TIME_PERIOD"))] = float(obs.get("OBS_VALUE"))
columns["gdp"] = pd.Series(gdp)

for col, name in bis_oecd.items():
    df = pd.read_csv(newest_file(name))
    df["quarter"] = df["TIME_PERIOD"].apply(to_quarter)
    columns[col] = df.groupby("quarter")["OBS_VALUE"].mean()

for col, name in fred.items():
    df = pd.read_csv(newest_file(name), parse_dates=["observation_date"])
    # FRED has empty cells on holidays
    df["value"] = pd.to_numeric(df.iloc[:, 1], errors="coerce")
    df["quarter"] = df["observation_date"].dt.to_period("Q")
    columns[col] = df.groupby("quarter")["value"].mean()

# ECB CISS, daily
df = pd.read_csv(newest_file("ecb_ciss"), usecols=["TIME_PERIOD", "OBS_VALUE"], parse_dates=["TIME_PERIOD"])
df["quarter"] = df["TIME_PERIOD"].dt.to_period("Q")
columns["ciss"] = df.groupby("quarter")["OBS_VALUE"].mean()

# VSTOXX, daily, dates like 04.01.1999
df = pd.read_csv(newest_file("vstoxx"), sep=";")
df["Date"] = pd.to_datetime(df["Date"], format="%d.%m.%Y")
df["quarter"] = df["Date"].dt.to_period("Q")
columns["vstoxx"] = df.groupby("quarter")["Indexvalue"].mean()

data = pd.DataFrame(columns).sort_index()

# add empty rows for missing quarters, so the gap check below can see them
all_quarters = pd.period_range(data.index[0], data.index[-1], freq="Q")
data = data.reindex(all_quarters)
data.index.name = "quarter"

# drop the quarter we're in, its averages only cover part of it
# (the download date is at the end of the file name: insee_gdp_2026-11-15.xml)
file_name = os.path.basename(newest_file("insee_gdp"))
download_date = file_name.replace("insee_gdp_", "").replace(".xml", "")
current_quarter = pd.Period(download_date, freq="Q")
data = data[data.index < current_quarter]

# checks
assert data.loc["1993Q1":, "gdp"].notna().all(), "GDP has gaps since 1993"
for col in data.columns:
    # between a series' first and last value, no quarter should be empty
    first = data[col].first_valid_index()
    last = data[col].last_valid_index()
    missing = data.loc[first:last, col].isna().sum()
    assert missing == 0, f"{col} has {missing} empty quarters"

os.makedirs("data/processed", exist_ok=True)
data.to_csv("data/processed/quarterly_revised.csv")
print("values since 1993Q1:")
print(data.loc["1993Q1":].count().to_string())
print(f"saved data/processed/quarterly_revised.csv, {data.index[0]} to {data.index[-1]}")
