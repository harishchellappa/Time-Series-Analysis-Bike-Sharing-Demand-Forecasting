library(readxl)
data <- read_excel("D:/Himanshu/Acads/03. Fall 2018 Sem/03. ISEN 615/Project/input_data.xlsx")

prod_fam_items <- unique(data$item_group_product_family)
month_list <- unique(data$month)

pred <- as.vector(NA)

for (i in 1:length(prod_family)) {
 
    data1 <- data[data$item_group_product_family == prod_family[i], ]
    
    lm.fit <- lm(Demand~ Month, data = data1) 
    pred1 <- predict(lm.fit, newdata = data1)
    
    pred1 <- as.vector(pred1)
    
    pred <- c(pred, pred1)
}

pred2 <-  pred[2:4681]

data$pred_demand <- pred2

data$ABS_error <- abs(data$Demand - data$pred_demand)
