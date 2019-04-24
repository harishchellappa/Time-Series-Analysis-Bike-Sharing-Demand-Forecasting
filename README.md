# Time-Series-Analysis

# Supply chain demand forecasting
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

# 2nd project - Demand forecasting using Prophet

# Executive summary of the problem
We analyzed the Los Angles Metro Bike Share data provided to us from Q3 of 2016 till Q4 of 2018. Our forecast was at the overall level and also at the individual region level since the metro serves 4 stations. Our forecast ultimately supports the proposal to expand into newer regions in LA. We came up with the potential candidates for expansion based on our analysis. Our models predict the number of trips for the last quarter of 2018 and Q1 of 2019, thereby predicting the number of bikes at a station level. We also give quantitative and qualitative recommendations for possible pricing changes by forecasting income from ticket sales and expanding the network. We evaluate characteristics for the region to be successful

# General Approach

We used some descriptive statistics to examine the data. We followed this with a replace impute encode procedure to get rid of the outliers. Then, we trained and tested the model to make predictions until Q1 of 2019. We used an open source package by facebook – called prophet. The recommendations are visually shown in tableau.

# Estimated Benefits
1. The revenue is sure to increase with the expansion.
2. Bike utilization is also a key parameter that we focused on, which is bound to increase at all regions.
3. The pricing recommendations we suggest in sure to increase the activity in winter months.

# The problem and data collection
We were given with two data files – the bicycle trip data and the station data. Descriptive statistics for each feature was analyzed. Bike IDs were used as a feature to forecast the bike staging part of the problem. Start station was an important feature as that forms the base of our forecast number of trips. Start times were used to pivot as index values. Lat – long details were used to geo code and get the correlation from weather data. Passholder type and plan duration are related to each other. Also, using station ID as the key both tables were left-joined

# Data Preprocessing
In Station Table - Updated the missing values in Region, go_live_date, status column
In Trip Table - Updated trip information.
The following steps were followed for data preprocessing:
• Created a new column ‘trip_duration’ (unit=minutes)
• Removed all trips which have a length less than a minute or more than 24 hours (outliers as mention in the competition website)
• Removed station ID 3000 as it’s a virtual station (has majority of the rows amongst removed data)
• Used the fact that Start_station=end_station for all Round Trips, and encoded missing values
• Updated null values of end_station using bike id – on where the bike was next used and previously used.
• Updated null/0 values in start_lat,start_lon,end_lat,end_lon
Initial data had 639786 rows. New data table has 629416 rows. So, removed 10,370 rows (1.6% data)
Few stations were removed from the analysis - 43 start stations are inactive right now + 3 stations (4110,4118,4276) which had station table rows blank - 4110 4118 were never in start_station.

# Forecasting Trips and Bicycle Demand
The initial step was to create a pivot between the start-time and bike stations. We created a column of date-time indices. From a date-time index, we rolled it at a daily level to start our proceedings. We removed the few dates that were from Q1 of 2019.
There were huge spikes in demand on certain dates. We figured out that this was due to a regular cycling competition happening in LA. https://www.ciclavia.org/events_history . These dates were also removed from the model.
We used the facebook’s prophet library in python to do our forecasting. We did 80-20 train-test split and also predicted for Q1 of 2019. This was done at a bike station level by running a loop over all stations.
We built dashboards in tableau that gave us the trend, seasonality, variation and spikes in demand. We were able to get it at quarterly level, monthly level, weekly level and hourly level. We noticed similar patterns in quarterly, monthly levels with demand increasing in summer and spring and the least during winter and rainy seasons. We correlated this with the weather data by getting data from the API. We also noticed there were no significant pattern at a weekly level. The demand is stationary irrespective of the day of the week. And, as expected at hourly level, there were peaks in demand at school hours. We incorporated this into the model and got our predictions. Used MSE as the loss function to evaluate the performance of the models. We then aggregated this for visualizing at all levels to present our forecast in tableau.

# Forecasting income and pricing recommendations
The revenue of the LA Bike Share program can be divided into two components, the cost of subscribing to a pass and the cost of each ride when the duration exceeds standard unit of thirty minutes.
We calculate the revenue obtained in the bike share program when a ride exceeds thirty minutes by finding the no of standard units of duration that the bike as been rented and we adjust this quantity based on the passholder type. We then obtain cost of each ride obtained by using the appropriate price (the price changes on July 12, 2018, the cost of a standard unit is reduced from 3.5 to 1.75).
Once the revenue obtained from each ride is calculated we create a pivot table that aggregates the revenue earned for each date. We then use this data to estimate the future revenue obtained from every ride by using fakebook’s prophet library. We use a 80-20 train test split and predict the revenue for Q1 of 2019. We used the weather data to identify the dips in demand. We use the events data to identify dips or peaks in the data. We use MSE as the loss function to evaluate the model.
A slightly higher test MSE is obtained for the training MSE due to the removal of service from Pasadena. An RMSE of lesser than one percent of the forecast is obtained.
To estimate the trend to subscription of the pass we forecast the number of rides each passholder type will undertake in the quarter 1 of 2019 we first create a pivot table from the data that aggregates the number of rides that passholder of each type has undertaken. We then use prophet to forecast the demand for quarter 1 in 2019.
We make the pricing recommendation based on the assumption that the number of trips for each passholder type is proportion to the actual number of users in the category. The following observations were made , the number of flex pass holders showed a decreasing a trend which suggests the presence of an alternative service which is a more feasible and hence we need to reduce the price to increase the usage of the number of flex pass holders. The forecast of the number of monthly pass rides changes around a mean and remains constant and hence we do not make changes to the price of monthly pass. One day pass show a similar trend in its forecast. The forecast for the number of people having walk-up prices increases which suggests the absence of alternative services. The price of this service can be increased.

# Network Management
ANALYSIS FOR AVERAGE NUMBER OF RIDES PER BIKE:
Key Points:
• Although the bike prices changed on 12th July 2018, Pasadena continued to go down in terms of average no. of rides per bike and hence service was discontinued in that area.
• DTLA is fairly consistent in all quarters throughout the 3 years and service must be continued with the same trips per bike ratio.
• During the Q4 of each year, Port of LA and Venice may perform badly due to unsuitable weather conditions for biking. Hence, keep the ratio of number of rides to bikes at around 15 for Port of LA and 55 for Venice.
• Now to predict the number of bikes, we use the method of Moving Averages of past 4 periods:
𝑁𝑢𝑚𝑏𝑒𝑟 𝑜𝑓 𝐵𝑖𝑘𝑒𝑠= 𝑁𝑢𝑚𝑏𝑒𝑟 𝑜𝑓 𝑇𝑟𝑖𝑝𝑠𝐴𝑣𝑔(𝐴𝑣𝑒𝑟𝑎𝑔𝑒 𝑁𝑢𝑚𝑏𝑒𝑟 𝑜𝑓 𝑅𝑖𝑑𝑒𝑠 𝑝𝑒𝑟 𝑏𝑖𝑘𝑒 𝑖𝑛 2018)
• Accordingly, DTLA will require 717, Port of LA will require 212 and Venice will require 485 bikes in Q1 of 2019

# Summary
1. The Bike Share metro is doing good business overall which is evident from the trend.
2. With expansion comes along the cost of capital and purchasing more bikes. This may or may not be done due to the bike utilization statistics explained earlier. Bike staging is taken care under this.
3. Pricing according to pass type also demands a chance as discussed.
4. From the analysis, it was clear that places close to coast or beach and major downtowns expand quickly. Cities away from major business capitals decline after a point of time and shouldn’t be considered for future expansion.
5. In Port of LA, all the stations are along the coast or near the beach. Our recommendation is to expand into the interiors so that people and tourists can travel from their houses/hotels to the coast.
6. Expand the company by installing stations at Long Beach and its interiors as it is the 39th most populous city in the United States of America.

# The details of methods applied can be found in the pdf final report!
# The SQL, Tableau, Python, R files as well
