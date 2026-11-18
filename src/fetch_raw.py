# Downloads the raw data for every series in docs/source-checks.md into data/raw/.
# Files are saved as they come, with today's date in the name, and never edited after.
# Also writes data/raw/manifest_<date>.csv with the url and a sha256 checksum of each file.
# Run from the repo root: python src/fetch_raw.py
# python src/fetch_raw.py 2026-11-15 only rewrites the manifest of that old snapshot, no downloads

import csv
import hashlib
import os
import sys
from datetime import date

import requests

bis = "https://stats.bis.org/api/v1/data/"
oecd = "https://sdmx.oecd.org/public/rest/data/"
house_prices = oecd + "OECD.ECO.MPD,DSD_AN_HOUSE_PRICES@DF_HOUSE_PRICES,/"
finmark = oecd + "OECD.SDD.STES,DSD_STES@DF_FINMARK,/"
fred = "https://fred.stlouisfed.org/graph/fredgraph.csv?id="

# file name -> url
sources = {
    # BIS: credit to GDP, credit gap, house prices
    "bis_credit_private.csv": bis + "WS_TC/Q.FR.P.A.M.770.A?format=csv",
    "bis_credit_households.csv": bis + "WS_TC/Q.FR.H.A.M.770.A?format=csv",
    "bis_credit_corporates.csv": bis + "WS_TC/Q.FR.N.A.M.770.A?format=csv",
    "bis_credit_gap.csv": bis + "WS_CREDIT_GAP/Q.FR.P.A.C?format=csv",
    "bis_house_prices.csv": bis + "WS_SPP/Q.FR.N.628?format=csv",

    # OECD: house prices, share prices, rates
    "oecd_house_prices.csv": house_prices + "FRA.Q.HPI.IX?format=csvfile",
    "oecd_price_to_rent.csv": house_prices + "FRA.Q.HPI_RPI.IX?format=csvfile",
    "oecd_shares_france.csv": finmark + "FRA.M.SHARE.IX._Z._Z._Z._Z.N?format=csvfile",
    "oecd_shares_euro_area.csv": finmark + "EA20.M.SHARE.IX._Z._Z._Z._Z.N?format=csvfile",
    "oecd_shares_us.csv": finmark + "USA.M.SHARE.IX._Z._Z._Z._Z.N?format=csvfile",
    "oecd_rate_3m.csv": finmark + "FRA.M.IR3TIB.PA._Z._Z._Z._Z.N?format=csvfile",
    "oecd_rate_10y.csv": finmark + "FRA.M.IRLT.PA._Z._Z._Z._Z.N?format=csvfile",

    # ECB CISS for France (daily, big file)
    "ecb_ciss.csv": "https://data-api.ecb.europa.eu/service/data/CISS/D.FR.Z0Z.4F.EC.SS_CIN.IDX?format=csvdata",

    # INSEE real GDP (only comes as xml)
    "insee_gdp.xml": "https://bdm.insee.fr/series/sdmx/data/SERIES_BDM/011794860",

    # FRED
    "fred_vix.csv": fred + "VIXCLS",
    "fred_commodities.csv": fred + "PALLFNFINDEXM",
    "fred_brent_monthly.csv": fred + "POILBREUSDM",
    "fred_brent_daily.csv": fred + "DCOILBRENTEU",

    # other files
    "vstoxx.txt": "https://www.stoxx.com/document/Indices/Current/HistoricalData/h_v2tx.txt",
    "epu.xlsx": "https://www.policyuncertainty.com/media/Europe_Policy_Uncertainty_Data.xlsx",
    "gpr.xls": "https://www.matteoiacoviello.com/gpr_files/data_gpr_export.xls",

    # GDP vintages (real-time data)
    "vintages_dallasfed.xls": "https://www.dallasfed.org/~/media/documents/research/international/oecd/frarealGDP.xls",
    "vintages_oecd.csv": oecd + "OECD.SDD.STES,DSD_STES_REVISIONS@DF_STES_REVISIONS,/FRA..B1GQ_Q......?format=csvfile",

    # TODO: ALFRED vintages for credit (QFRPAM770A), needs a FRED API key
}

os.makedirs("data/raw", exist_ok=True)
today = str(date.today())
download = True
if len(sys.argv) > 1:
    today = sys.argv[1]
    download = False  # never save new data under an old date
errors = []
manifest = [["file", "url", "sha256"]]

for name, url in sources.items():
    # bis_credit_gap.csv -> data/raw/bis_credit_gap_2026-11-15.csv
    base, ext = os.path.splitext(name)
    path = f"data/raw/{base}_{today}{ext}"

    if os.path.exists(path):
        print("already have", path)
    elif not download:
        print("MISSING", path)
        errors.append(name)
        continue
    else:
        # note: don't set a browser user agent, FRED blocks it
        try:
            r = requests.get(url, timeout=120)
            r.raise_for_status()
        except Exception as e:
            print("FAILED", name, e)
            errors.append(name)
            continue

        with open(path, "wb") as f:
            f.write(r.content)
        print("saved", path)

    with open(path, "rb") as f:
        checksum = hashlib.sha256(f.read()).hexdigest()
    manifest.append([os.path.basename(path), url, checksum])

# csv module because some OECD urls have commas in them
with open(f"data/raw/manifest_{today}.csv", "w", newline="") as f:
    csv.writer(f).writerows(manifest)
print("wrote", f"data/raw/manifest_{today}.csv")

if errors:
    print("\nsome downloads failed:", errors)
    exit(1)
