install.packages("RPostgres")

library(RPostgreSQL)
library(RPostgres)

# connect to database
conn <- dbConnect(Postgres(),
                  host = "ep-small-limit-18518205.ap-southeast-1.aws.neon.tech",
                  port = 5432,
                  dbname = "christget",
                  user = "christgett",
                  password = "MAO3Zl7NsWTe",
                  sslmode = "require")

# import csv file
review <- read.csv("Datasets/review.csv")
restaurant <- read.csv("Datasets/restaurant.csv")
location <- read.csv("Datasets/location.csv")
category <- read.csv("Datasets/category.csv")
cluster <- read.csv("Datasets/cluster.csv")
price_level <- read.csv("Datasets/price_level.csv")
chain <- read.csv("Datasets/chain.csv")

# add table into the database
dbWriteTable(conn, "review", review)
dbWriteTable(conn, "restaurant", restaurant)
dbWriteTable(conn, "location", location)
dbWriteTable(conn, "category", category)
dbWriteTable(conn, "cluster", cluster)
dbWriteTable(conn, "price_level", price_level)
dbWriteTable(conn, "chain", chain)

# List table
dbListTables(conn)

# disconnect from database
dbDisconnect(conn)