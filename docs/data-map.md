# Data map

Step 1 of the roadmap: for each predictor in the Banque de France note (Eco Notepad 468), find a public series I can actually download. I checked each one by querying the source on 14 November 2026, not just by reading the docs.

## What the note uses

The note says it uses "around thirty" variables, but it only names them in its two charts:

- Chart 1: the ten best single predictors at each horizon
- Chart 2: the variables kept by the LASSO

That's 21 named variables. The other nine or so are only described by category ("financial markets and interest rates", "macroeconomic activity"), so for those I had to pick something myself. That part of the list is my choice, not a match with the note.

Two things I noticed in the charts that the text doesn't say:

- Both charts stop in 2020, so the sample is probably 1993 to around 2020, not up to today.
- Debt and stress variables are used as quarterly changes ("var. trim."), prices and uncertainty as annual growth ("crois. annuelle"). Chart 2 uses lags up to four quarters, (t-1) to (t-4).

## Predictors

"In note": C1 = Chart 1, C2 = Chart 2 (LASSO), h = horizon in quarters.

| Note label (French) | Meaning | In note | Public series | Source and code | Starts | Vintages |
|---|---|---|---|---|---|---|
| Dette SPNF/PIB (var. trim.) | Private non-financial debt / GDP, quarterly change | C1 h=1 (best) | Credit to private non-financial sector, % of GDP | BIS total credit, `Q.FR.P.A.M.770.A` | 1969Q4 | Partly, see below |
| Dette Ménages/PIB (var. trim.) | Household debt / GDP, quarterly change | C1 h=1, C2 h=1 | Credit to households and NPISHs, % of GDP | BIS total credit, `Q.FR.H.A.M.770.A` | 1977Q4 | Partly |
| Dette SNF/PIB (var. trim.) | Corporate debt / GDP, quarterly change | C1 h=1, C2 h=1 (and t-1) | Credit to non-financial corporations, % of GDP | BIS total credit, `Q.FR.N.A.M.770.A` | 1977Q4 | Partly |
| Gap crédit | Credit-to-GDP gap | C1 h=1 and h=20 | Credit-to-GDP gap, private non-financial sector | BIS credit gaps, `Q.FR.P.A.C` | 1979Q4 | No |
| VIX | US implied equity volatility | C1 h=1, C2 h=1 (and t-1) | CBOE VIX, daily close | FRED `VIXCLS` | 1990-01 | Not revised |
| VSTOXX | Euro Stoxx 50 implied volatility | C1 h=20 | VSTOXX (V2TX) | STOXX | 1999-01 | Not revised |
| CISS (var. trim.) | ECB financial stress index for France, quarterly change | C1 h=1 and h=20 | New CISS, France | ECB, `CISS/D.FR.Z0Z.4F.EC.SS_CIN.IDX` | 1985-02 | Not revised in practice |
| ICF: Facteur 1, Facteur 2 (var. trim.) | Two factors of a financial conditions index (Lombardi et al., 2025) | C1 h=20 | None found | Method: Lombardi, Manea and Schrimpf, BIS WP 1272 (US index) | — | — |
| Inc. Pol. Eco. (crois. annuelle) | Economic policy uncertainty, annual growth | C1 h=20 (best), C2 h=20 (t-4) | EPU France, monthly | Baker, Bloom and Davis, `Europe_Policy_Uncertainty_Data.xlsx`, column `France_News_Index` | 1987-01 | Not revised |
| Risques géopolitiques | Geopolitical risk | C2 h=20 (t-1, t-2) | GPR, monthly: global `GPR`, France `GPRC_FRA` | Caldara and Iacoviello, `data_gpr_export.xls` | 1985-01 | Not revised |
| Prix immobiliers (crois. annuelle) | House prices, annual growth | C1 h=1 | Nominal house price index | OECD, `FRA.Q.HPI.IX`; also BIS `WS_SPP/Q.FR.N.628` | 1970Q1 | No |
| Prix immo/loyer (crois. annuelle) | Price-to-rent ratio, annual growth | C1 h=1 | Price-to-rent ratio | OECD, `FRA.Q.HPI_RPI.IX` | 1970Q1 | No |
| Prix des matières premières | Commodity prices | C1 h=1 | IMF all-commodity index, monthly | FRED `PALLFNFINDEXM` | 1992-01 | Not revised |
| Prix pétrole (crois. annuelle) | Oil price, annual growth | C2 h=20 (t-4) | Brent, USD, monthly | FRED `POILBREUSDM` | 1992-01 (daily Brent from 1987) | Not revised |
| Rendement boursier ann. | Annual stock return, France (my guess) | C1 h=1 and h=20, C2 h=20 | Share price index, France | OECD, `FRA.M.SHARE.IX._Z._Z._Z._Z.N` | 1955-01 | Not revised |
| Rendement boursier EU ann. | Annual stock return, Europe | C1 h=20 | Share price index, euro area | OECD, `EA20.M.SHARE.IX._Z._Z._Z._Z.N` | 1986-12 | Not revised |
| Rendement boursier US ann. | Annual stock return, US | C1 h=20 | Share price index, US | OECD, `USA.M.SHARE.IX._Z._Z._Z._Z.N` | 1957-01 | Not revised |
| PIB trim. / PIB annuel (crois. annuelle) | GDP growth, quarterly and annual | C1 h=20, C2 h=1 | Real GDP, chained volumes, SA-WDA | INSEE quarterly accounts, idbank `011794860` | 1949Q1 | Yes, see below |
| *Not named, category "interest rates"* | Short and long rates | — | 3-month and 10-year rates, France | OECD, `FRA.M.IR3TIB...`, `FRA.M.IRLT...` | 1970 / 1960 | Not revised |

I first found the codes on DBnomics, which mirrors the BIS, OECD, ECB and INSEE. But its BIS copy stopped at 2024Q4, so I download from each provider directly. The start dates were checked again at each source: see [`source-checks.md`](source-checks.md).

## Real-time vintages

| Series | Vintages available | Source |
|---|---|---|
| Real GDP, France | Quarterly vintages, May 1962 to Nov 1998 | Dallas Fed, Real-Time Historical Dataset for the OECD (`frarealGDP.xls`) |
| Real GDP, France | Monthly vintages, Feb 1999 to now | OECD revisions database, measure `B1GQ_Q` |
| Private credit / GDP (BIS) | Only from June 2016 | ALFRED (archive of old FRED data), `QFRPAM770A` and related |
| Household and corporate debt, credit gap | Nothing found before 2016 | — |
| Market and text-based indices | Not needed, they're not revised | — |

So for GDP (the target, and the GDP growth predictors) I can use the data as it was known at each date since 1993. For the debt ratios I can't, except after 2016. My plan before 2016 is to divide revised debt by real-time GDP. That only fixes half of the revision problem, and I'll say so in the results.

## Gaps and decisions to make

1. **Financial conditions index (ICF factors 1 and 2).** Not public for France. Decided (16 Nov): I use the CISS alone in its place, since it's already one of the note's predictors and is public. It only shows up at 20 quarters, which I only replicate in-sample anyway, so the replication will differ there and I'll say so. Rebuilding it with the Lombardi et al. two-factor method stays possible later.
2. **VSTOXX starts in 1999**, but the sample starts in 1993. It's only in Chart 1 at 20 quarters and the LASSO doesn't keep it, so either use it from 1999 or leave it out.
3. **The nine unnamed variables.** I use the categories from the text (rates, activity) and say clearly that this part is my choice.
4. **Debt vintages.** See above: revised debt / real-time GDP before 2016, real vintages after.
5. **Publication lags.** I'll measure these in step 2 instead of guessing. INSEE's first GDP estimate comes about 30 days after the quarter (45 days before 2016). BIS release dates can be read from the ALFRED vintage dates. Market data is available the same day.

## Recession dates

The CDCEF dates are in [`data/reference/cdcef_recessions.csv`](../data/reference/cdcef_recessions.csv), from the committee's press release of 10 June 2021. The committee's peak is the last quarter of the expansion, so the recession starts the quarter after. The Covid recession has a provisional peak in 2019Q4 and no trough in that release. There may be a newer update on the AFSE website, which I need to check before using the dates.
