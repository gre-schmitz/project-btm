# project-btm
Le Wagon Project Beat the Market

**DISCLAIMER**: We have created this repo as a graduation project for the _Le Wagon Data Science & AI_ bootcamp without any commercial purpose. That is why we have not updated the data input lately. The latest calculations are from late March 2024.

## Project description
The idea is to predict a GDP growth in real time (that is on a daily basis) rather than waiting for the official GDPs being announced once a quarter. The GDP is a powerful feature when predicting a lot of economic indices, such as the S&P 500. Thus, the repo provides two pickle files:

- an XGBoost model + pipeline to predict the GDP growth in real time
- another model to predict the S&P 500

Our S&P 500 model is trained with interpolated GDP-growth rates: Between two GDP announcements, for every day we linearly interpolated the growth rates between two announcements. This interpolated growth was used as a feature to train our XGBoost S&P-model. For the _current_ quarter we are using growth rates from our GDP-prediction model. We believe like that we have created a Fair Value Calculator. Why do we believe that? The difference of the actual and predicted S&P values are _mean reverting_. Hence, the values of our predictor and the actual S&P 500 have the strong tendency to follow each other.

We have created a Dockerfile, containing the our data and pickle files. It runs an API that we have deployed via GCP. You can get your latest Fair Values on [Beat the Market](https://project-btm-front.streamlit.app/).


## Data Sources:
GDP Now [https://www.atlantafed.org/cqer/research/gdpnow#Tab2]
The GDPNow forecast model provided by the Federal Reserve Bank of Atlanta estimates the real gross domestic product (GDP) growth in the United States for the current quarter. The GDPNow model estimate is on a quarter-over-quarter basis, meaning it forecasts the percentage change in GDP from the previous quarter to the current quarter on an annualized basis.

Quarter-over-quarter annualized growth rates are commonly used in the U.S. to provide a sense of the GDP's growth pace as if the quarterly rate continued for a full year. This approach helps smooth out the seasonal variations and provides a more consistent basis for comparison across quarters. Note that the Federal Reserve's Summary of Economic Projections typically includes forecasts for GDP on a year-over-year (YoY) basis.


From Bloomberg
Daily
GSUSFCI Index - GS Financial Conditions Index
CESIUSD Index - Citi Economic Surprise Index
SPX Index - S&P 500
NDX Index - NASDAQ
USDJPY Currncy - USDJPY Spot FX
USOSFR2 Curncy - 2y USD SWAP Rate
USOSFR10 Curncy - 10y USD SWAP Rate
CLA Comdty - Front Contract WTI
US Breakeven 2 Year Index - 2y Breakeven Inflation Rate

From FRED API[https://fred.stlouisfed.org
Weekly
MORTGAGE30US - 30-Year Fixed Rate Mortgage Average in the United States
CCLACBW027SBOG -Consumer Loans: Credit Cards and Other Revolving Plans, All Commercial Banks
WALCL - Total Assets of all Federal Reserve Banks. This series provides insight into the scale of the Federal Reserve's operations, including its asset purchases and quantitative easing measures.
NFCI - Chicago Fed National Financial Conditions Index. It measures financial conditions in money markets, debt and equity markets, and the traditional and “shadow” banking systems.
WEI - Weekly Economic Index. It provides an informative signal of the state of the U.S. economy based on high-frequency data reported daily or weekly.
ICSA: Initial Claims. It measures the number of jobless claims filed by individuals seeking to receive state jobless benefits. This is a leading indicator for the U.S. labor market.
ADPWNUSNERSA - ADP National Employment Report: Private Nonfarm Employment, Seasonally Adjusted

Monthly
FEDFUNDS - Federal Funds Rates
WTISPLC - WTI Spot Price FOB (Dollars per Barrel)
CPIAUCSL - CPI
CES0500000003 - Average Hourly Earnings of All Employees
Core Inflation - CORESTICKM159SFRBATL
PAYEMS - Non Farms Employment
EXPINF1YR - Expected Inflation Rate in 1 Year
STLPPM - St. Louis Fed Precious Metals Price: Gold
ECIWAG - Employment Cost Index: Wages and Salaries
M2REAL - Real M2 Money Stock
UNRATE - Unemployment Rate
PPIACO - Producer Price Index by Commodity
PCUOMFGOMFG - Producer Price Index by Industry: Overall Manufacturing
PCUATRANSATRANS - Producer Price Index by Industry: Transportation and Warehousing
PCUATRADEATRADE - Producer Price Index by Industry: Wholesale and Retail Trade
PCUAWHLTRAWHLTR - Producer Price Index by Industry: Wholesale Trade
CSUSHPINSA - Case-Shiller U.S. National Home Price Index, Not Seasonally Adjusted
SPCS20RSA - S&P/Case-Shiller 20-City Composite Home Price Index, Seasonally Adjusted
WALCL - Weekly Assets and Liabilities of Commercial Banks in the United States
REAINTRATREARAT10Y - Real Estate: Average Interest Rate, 10 Year Maturity
SAHMREALTIME - Sahm Rule Recession Indicator (Real-Time)
POPTHM - Total Population (in Thousands)

From S&P GLobal [https://www.spglobal.com/marketintelligence/en/mi/products/us-monthly-gdp-index.html]
Monthly
Monthly Nominal GDP Index
Monthly Real GDP Index
