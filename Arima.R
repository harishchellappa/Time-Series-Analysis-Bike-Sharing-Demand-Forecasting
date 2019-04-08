## ARIMA Model

df = t(ES)
df <- data.frame(df)
time_stamp <- rownames(df)

rownames(df) <- NULL
df['time_stamp'] <- time_stamp
colnames(df) <- df[1,]
df <- df[-1,]
colnames(df)[ncol(df)] <- 'time_stamp'

df['time_stamp'] <- c(1:nrow(df))
df <- df[-53,]

library(forecast)

pred_matrix <- matrix(0,16,91)
df_pred_matrix <- data.frame(pred_matrix)
train <- df[1:36,]
test<- df[37:52,]

for (i in (1:ncol(df_pred_matrix))){
model <- auto.arima(train[,i])
#summary(model)
df_pred_matrix[,i] <- predict(model,16)$pred
}

write.csv(df_pred_matrix, file = "Arima1.csv",row.names=FALSE)

model2 <- auto.arima(train[,1])
#summary(model)
x <- predict(model2,16)
z