# Source checks

Here I checked the start dates from [`data-map.md`](data-map.md) directly at each provider (API or file), not on DBnomics. Done on 14 November 2026.

A series "starts" at its first actual value, not its first row. For example the CISS for France has empty rows from January 1980 but no value before 4 February 1985, which is why I first had the wrong date in the map.

## Results

"Last" = latest value available on the day I checked.

| Series | Code | First value | Last | Matches map | URL |
|---|---|---|---|---|---|
| Private non-financial credit / GDP | BIS `WS_TC` `Q.FR.P.A.M.770.A` | 1969Q4 | 2026Q1 | Yes | `https://stats.bis.org/api/v1/data/WS_TC/Q.FR.P.A.M.770.A?format=csv` |
| Household credit / GDP | BIS `WS_TC` `Q.FR.H.A.M.770.A` | 1977Q4 | 2026Q1 | Yes | `https://stats.bis.org/api/v1/data/WS_TC/Q.FR.H.A.M.770.A?format=csv` |
| Corporate credit / GDP | BIS `WS_TC` `Q.FR.N.A.M.770.A` | 1977Q4 | 2026Q1 | Yes | `https://stats.bis.org/api/v1/data/WS_TC/Q.FR.N.A.M.770.A?format=csv` |
| Credit-to-GDP gap | BIS `WS_CREDIT_GAP` `Q.FR.P.A.C` | 1979Q4 | 2026Q1 | Yes | `https://stats.bis.org/api/v1/data/WS_CREDIT_GAP/Q.FR.P.A.C?format=csv` |
| House prices (BIS) | BIS `WS_SPP` `Q.FR.N.628` | 1970Q1 | 2026Q2 | Yes | `https://stats.bis.org/api/v1/data/WS_SPP/Q.FR.N.628?format=csv` |
| House prices (OECD) | `FRA.Q.HPI.IX` | 1970Q1 | 2026Q2 | Yes | `https://sdmx.oecd.org/public/rest/data/OECD.ECO.MPD,DSD_AN_HOUSE_PRICES@DF_HOUSE_PRICES,/FRA.Q.HPI.IX` |
| Price-to-rent | `FRA.Q.HPI_RPI.IX` | 1970Q1 | 2026Q2 | Yes | `https://sdmx.oecd.org/public/rest/data/OECD.ECO.MPD,DSD_AN_HOUSE_PRICES@DF_HOUSE_PRICES,/FRA.Q.HPI_RPI.IX` |
| Share prices, France | `FRA.M.SHARE.IX._Z._Z._Z._Z.N` | 1955-01 | 2026-10 | Yes | `https://sdmx.oecd.org/public/rest/data/OECD.SDD.STES,DSD_STES@DF_FINMARK,/FRA.M.SHARE.IX._Z._Z._Z._Z.N` |
| Share prices, euro area | `EA20.M.SHARE.IX._Z._Z._Z._Z.N` | 1986-12 | 2026-10 | Yes | same, with `EA20` |
| Share prices, US | `USA.M.SHARE.IX._Z._Z._Z._Z.N` | 1957-01 | 2026-10 | Yes | same, with `USA` |
| 3-month rate, France | `FRA.M.IR3TIB.PA._Z._Z._Z._Z.N` | 1970-01 | 2026-10 | Yes | same dataflow |
| 10-year rate, France | `FRA.M.IRLT.PA._Z._Z._Z._Z.N` | 1960-01 | 2026-10 | Yes | same dataflow |
| CISS France | ECB `CISS/D.FR.Z0Z.4F.EC.SS_CIN.IDX` | 1985-02-04 | 2026-10 | **Fixed** (was 1980-01) | `https://data-api.ecb.europa.eu/service/data/CISS/D.FR.Z0Z.4F.EC.SS_CIN.IDX?format=csvdata` |
| Real GDP, France | INSEE idbank `011794860` | 1949Q1 | 2026Q3 | Yes | `https://bdm.insee.fr/series/sdmx/data/CNT-2020-PIB-EQB-RF/T.CNT-EQUILIBRE_PIB.SO.PIB.SO.VALEUR_ABSOLUE.FE.L.EUROS.CVS-CJO.FALSE` |
| VIX | FRED `VIXCLS` | 1990-01-02 | 2026-11-12 | Yes | `https://fred.stlouisfed.org/series/VIXCLS` |
| Commodity prices | FRED `PALLFNFINDEXM` | 1992-01 | 2026-09 | Yes | `https://fred.stlouisfed.org/series/PALLFNFINDEXM` |
| Brent, monthly | FRED `POILBREUSDM` | 1992-01 | 2026-09 | Yes | `https://fred.stlouisfed.org/series/POILBREUSDM` |
| Brent, daily | FRED `DCOILBRENTEU` | 1987-05-20 | — | Yes | `https://fred.stlouisfed.org/series/DCOILBRENTEU` |
| VSTOXX | STOXX `V2TX` | 1999-01-04 | 2026-11-13 | Yes | `https://www.stoxx.com/document/Indices/Current/HistoricalData/h_v2tx.txt` |
| EPU France | column `France_News_Index` | 1987-01 | 2026-10 | Yes | `https://www.policyuncertainty.com/media/Europe_Policy_Uncertainty_Data.xlsx` |
| GPR global, France | columns `GPR`, `GPRC_FRA` | 1985-01 | 2026-10 | Yes | `https://www.matteoiacoviello.com/gpr_files/data_gpr_export.xls` |

## Vintages

| Source | What I found | URL |
|---|---|---|
| Dallas Fed real-time OECD data, France real GDP | Vintages Feb 1962 to Nov 1998 | `https://www.dallasfed.org/~/media/documents/research/international/oecd/frarealGDP.xls` (the old `/institute/oecd/` path is a 404) |
| OECD revisions database, `B1GQ_Q`, France | 334 monthly editions, Feb 1999 to Nov 2026 | `https://sdmx.oecd.org/public/rest/data/OECD.SDD.STES,DSD_STES_REVISIONS@DF_STES_REVISIONS,/FRA..B1GQ_Q......` |
| ALFRED `QFRPAM770A` | First vintage 6 June 2016 | `https://alfred.stlouisfed.org/series?seid=QFRPAM770A` |

## Notes

- The BIS v1 API works and goes to 2026Q1. The v2 URL gave a 404. DBnomics' copy of the BIS data stops at 2024Q4.
- The OECD API doesn't return rows in date order, so sort by period before taking the first value.
- Values can differ a bit between sources because of revisions. Example: private credit / GDP in 2025Q4 is 214.6 at the BIS but 215.4 on FRED.

## Screenshots

The real record is the raw files in `data/raw/`, downloaded by `src/fetch_raw.py` and never edited. The screenshots in [`images/series/`](../images/series/) are just an extra visual check, taken on the providers' websites on 15 November 2026. I only kept the ones that show exactly the series above:

- BIS: the three `WS_TC` series, the credit gap, `WS_SPP`
- OECD: share prices, euro area
- FRED: 10-year rate, France (OECD data, monthly)
