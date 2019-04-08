library(readxl)
library(dplyr)
data <- read_excel("D:/Himanshu/Acads/03. Fall 2018 Sem/03. ISEN 615/Project/item_level_inputdata.xlsx")

### Seasonality method
data$quarter <- substr(data$year_quarter, 6, 6)
# calculate mean of demand for each family-item combo and seasonal factor of each line 
meandmd <- data %>% group_by(product_family, item_no) %>% summarise(mean_demand = mean(Demand))

data <- inner_join(data, meandmd, by=c("product_family", "item_no"))

data$seasonal_factor <- data$Demand/data$mean_demand

### calculate seasonal factor at prod_family, item,  quarter level

mean_seasonal_factor <-aggregate(x=data$seasonal_factor, by=list(data$product_family, data$item_no, data$quarter), FUN=mean)

colnames(mean_seasonal_factor) <- c("product_family","item_no", "quarter", "mean_seasonal_factor")

data <- inner_join(data, mean_seasonal_factor, by=c("product_family","item_no", "quarter"))

data$forecasted_demand <- data$mean_demand*data$mean_seasonal_factor

write.csv(data, 'itemlevel_seasonality_output.csv')
