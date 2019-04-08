library(readxl)
data <- read_excel("D:/Himanshu/Acads/03. Fall 2018 Sem/03. ISEN 615/Project/item_level_outputs/Regression_item_level_inputdata.xlsx")

data <- as.data.frame(data)

prod_fam_items <- data %>% distinct(product_family, item_no)
prod_fam_items <- as.data.frame(prod_fam_items)

pred <- as.vector(NA)

for (i in 1:nrow(prod_fam_items)) {
 
    data1 <- data[data$product_family == prod_fam_items[i, 1] & data$item_no == prod_fam_items[i, 2], ]
    
    lm.fit <- lm(Demand~ quarter_num, data = data1) 
    pred1 <- predict(lm.fit, newdata = data1)
    
    pred1 <- as.vector(pred1)
    
    pred <- c(pred, pred1)
}

pred2 <-  pred[2:6903]

data$pred_demand <- pred2

write.csv(data, 'regression_output.csv')

