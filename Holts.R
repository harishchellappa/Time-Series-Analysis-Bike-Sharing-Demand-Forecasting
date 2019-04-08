library(readxl)
data <- read_excel("D:/Himanshu/Acads/03. Fall 2018 Sem/03. ISEN 615/Project/input_data.xlsx")
data$Month <- rep(seq(1, 52, 1), 90)

a <- 0.2
b <- 0.2

# For long term forecast
next_year_months <- c(seq(201810, 201812, 1), seq(201901, 201909, 1))
next_months <- seq(53, 64, 1)

# Manually run it
#new_df <- data1[FALSE,]

prod_family <- unique(data$item_group_product_family)

for (i in 1:length(prod_family)) {
  
  data1 <- data[data$item_group_product_family == prod_family[i], ]
  
  # Find initial values of S0 and G0
  S0 <- mean(data1$Demand)
  
  lm.fit <- lm(Demand~ Month, data = data1) 
  
  G0 <- lm.fit$coefficients[2]
  
  ## 
  data1$level[1] <- S0
  data1$trend[1] <- G0
  data1$forecast[1] <- S0 + G0
  
  for (j in 2:52){
    data1$level[j] <- a*data1$Demand[j] + (1-a)*(data1$level[j-1]+data1$trend[j-1])
    data1$trend[j] <- b*(data1$Demand[j] - data1$Demand[j-1]) + (1-b)*data1$trend[j-1]
    data1$forecast[j] <- data1$level[j]+data1$trend[j]
  }
  
  # For long term forecast of next year
  
  k=1
  
  for (j in 53:64){
    data1[nrow(data1)+1,] <- NA
    data1$item_group_product_family[j] = prod_family[i]
    data1$year_month_order_date[j] = next_year_months[k]
    data1$Month[j] = next_months[k]
    data1$forecast[j] = data1$level[52] + (k+1)*data1$trend[52]
    k=k+1
    }
  
  
  new_df <- rbind(new_df, data1)
}

write.csv(new_df, 'Holt_forecast_output_longterm.csv')
