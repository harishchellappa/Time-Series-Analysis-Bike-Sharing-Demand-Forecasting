library(dplyr)
data <- read_excel("D:/Himanshu/Acads/03. Fall 2018 Sem/03. ISEN 615/Project/item_level forecasts/Regression_item_level_inputdata.xlsx")

a <- 0.2
b <- 0.2

# Run it after first manual run for data1 from loop below
#new_df <- data1[FALSE,]

prod_fam_items <- data %>% distinct(product_family, item_no)
prod_fam_items <- as.data.frame(prod_fam_items)

# For long term forecast
next_year_quarter <- c('2018_4', '2019_1', '2019_2', '2019_3')
next_quarter <- seq(18, 21, 1)


for (i in 1:nrow(prod_fam_items)) {
  
  data1 <- data[data$product_family == prod_fam_items[i, 1] & data$item_no == prod_fam_items[i, 2], ]
  
  # Find initial values of S0 and G0
  S0 <- mean(data1$Demand)
  
  lm.fit <- lm(Demand~ quarter_num, data = data1) 
  
  G0 <- lm.fit$coefficients[2]
  
  ## 
  data1$level[1] <- S0
  data1$trend[1] <- G0
  
  for (j in 2:nrow(data1)){
    data1$level[j] <- a*data1$Demand[j] + (1-a)*(data1$level[j-1]+data1$trend[j-1])
    data1$trend[j] <- b*(data1$Demand[j] - data1$Demand[j-1]) + (1-b)*data1$trend[j-1]
  }
  
  data1$forecast <- data1$level+data1$trend
  
  # For long term forecast of next year
  
  k=1
  
  for (j in 18:21){
    data1[nrow(data1)+1,] <- NA
    data1$product_family[j] = prod_fam_items[i, 1]
    data1$item_no[j] = prod_fam_items[i, 2]
    
    data1$year_quarter[j] = next_year_quarter[k]
    data1$quarter_num[j] = next_quarter[k]
    data1$forecast[j] = data1$level[17] + (k+1)*data1$trend[17]
    k=k+1
  }
  
  
  new_df <- rbind(new_df, data1)
}

write.csv(new_df, 'longterm_item_level_Holt_forecast_output.csv')
