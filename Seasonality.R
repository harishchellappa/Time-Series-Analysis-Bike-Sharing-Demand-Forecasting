library(readxl)
library(dplyr)
data <- read_excel("D:/Himanshu/Acads/03. Fall 2018 Sem/03. ISEN 615/Project/input_data.xlsx")

### Seasonality method
data$month <- substr(data$year_month_order_date, 5, 6)
# calculate mean of demand for each family and seasonal factor of each line 
meandmd <- data %>% group_by(item_group_product_family) %>% summarise(mean_demand = mean(Demand))

data <- inner_join(data, meandmd, by=c("item_group_product_family"))

data$seasonal_factor <- data$Demand/data$mean_demand

### calculate seasonal factor at prod_family, month level

mean_seasonal_factor <-aggregate(x=data$seasonal_factor, by=list(data$item_group_product_family, data$month), FUN=mean)
colnames(mean_seasonal_factor) <- c("item_group_product_family", "month", "mean_seasonal_factor")

data <- inner_join(data, mean_seasonal_factor, by=c("item_group_product_family", "month"))

data$forecasted_demand <- data$mean_demand*data$mean_seasonal_factor

write.csv(data, 'Seasonal_method_output.csv')
