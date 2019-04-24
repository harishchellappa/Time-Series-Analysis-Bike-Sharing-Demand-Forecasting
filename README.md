# Time-Series-Analysis

# Arconic demand forecasting
To begin with, we performed some exploratory data analysis on Arconic demand. We used Market A
data for basic exploration and understanding. We investigated the significance of each column and how
can we use them in forecasting. We plotted demand by months (After rolling up at month level) at
product family level and item level using excel. It gave us an idea that lot of product families/items are
not having orders in all of the months. Also, it gave us an idea what should be the appropriate level of
aggregation to forecast demand. We chose important columns based on the analysis and performed
some pre-processing on data before applying any forecasting technique. Below are some observations
and decisions based on exploratory analysis –

1. For Market A, there was 41227 rows of data in historical data sheet and 6850 rows in open data
sheet. As historical and open data both were having maximum order date of September’2018, we
decided to combine them. This gave us the actual sense of demand in the June 2014 – September
2018 period that we are developing our forecast on.

2. After looking at the data carefully, we aggregated demand at Product family level and item level. We
decided that we would go ahead with forecast on Product family-month level and item-quarter
level, as they seemed appropriate looking at the demand numbers and patterns.

3. We extracted mainly 4 columns from Arconic data – Product family, Item no., order date (to extract
months and quarters), and Demand quantity.

4. We cleaned data and removed observations wherever quantity < 0 (about 1.3% of data).
We have forecasted on two levels of demand aggregation – monthly aggregation for product families
& quarterly aggregation at SKU (item#) level. According to the textbook, monthly forecast at family
level is a short-term forecasting technique. We have used 6 techniques namely- Moving average,
Exponential smoothing, Seasonality, Regression method, Holt’s method and ARIMA. Quarterly forecasts
at item level is a long-term forecasting technique. Holt’s method has the parameter Tau that is used for
multiple step ahead forecasts for future months.

In addition to all these models, we tried to implement Holt Winter method, but we faced some
problems due to missing demand. The averaged seasonal factors were coming out to be 0 for some
missing demand months which is used as a denominator in calculation St (level) at each step of series.
So, we did not go ahead with this approach.
As of now, our models use Market A data for forecasting purpose but our analysis can easily be
replicated to Market B and C datasets as well.
Product family and Monthly level - short term forecast

# Data Preprocessing

As we wanted to get our data ready for forecasting, we applied some pre-processing touches to the
dataset. We started off with the actual data format as per the dataset. Daily and weekly aggregation of
demand did not yield good results. We found sufficient data at month level aggregation for each
product family.

• We used three columns from main dataset – Product family, Order Month (yyyymm format),
demand quantity and aggregated data at product family-month level

• we found some months with missing demand. So, we added missing months demand as 0 to resolve
inconsistency in data. This increased number of records increased to 62618.

• The aggregated version had 4680 records. There were 90 product families to be analyzed. Each
product family had 52 months of data from 201406-201809 (removed one 201404 observation)

# The details of methods applied can be found in the pdf final report!
# The SQL, Tableau, Python, R files as well
