// Databricks notebook source
val Video_Game_Sales = spark.read.option("inferSchema", "true").option("header", "true").csv("/FileStore/tables/video_game_sales.csv")



// COMMAND ----------


Video_Game_Sales.printSchema()

// COMMAND ----------

// MAGIC %md
// MAGIC Creating Temporary View

// COMMAND ----------


Video_Game_Sales.createOrReplaceTempView("Video_Game_Sales")


// COMMAND ----------

// MAGIC %sql
// MAGIC select * from Video_Game_Sales

// COMMAND ----------

// MAGIC %md
// MAGIC Exploratory Data Analysis or EDA

// COMMAND ----------

// MAGIC %md
// MAGIC Rise & Fall of Video Game Consoles

// COMMAND ----------

// MAGIC %sql
// MAGIC select year, platform, sum(global_sales) from Video_Game_Sales group by platform, year order by year asc

// COMMAND ----------

// MAGIC %md
// MAGIC Top 10 Games (by Global Sales)

// COMMAND ----------

// MAGIC %sql
// MAGIC select genre, sum(global_sales) from Video_Game_Sales group by genre order by sum(global_sales) desc limit 10;

// COMMAND ----------

// MAGIC %md
// MAGIC Top 25 Platfroms (by Global Sales)

// COMMAND ----------

// MAGIC %sql
// MAGIC select publisher, sum(global_sales) from Video_Game_Sales group by publisher order by sum(global_sales) desc limit 25;

// COMMAND ----------

// MAGIC %md
// MAGIC Top 10 Consoles (By Global Sales)
// MAGIC

// COMMAND ----------

// MAGIC %sql
// MAGIC select platform, sum(global_sales) from Video_Game_Sales group by platform order by sum(global_sales) desc limit 10;

// COMMAND ----------

// MAGIC %md
// MAGIC Popular Genres Across Platforms

// COMMAND ----------

// MAGIC %sql
// MAGIC select platform, genre, count(*) from Video_Game_Sales group by platform, genre order by count(*) desc

// COMMAND ----------

// MAGIC %md
// MAGIC Top 10 Games: Proportion of Sales in Markets

// COMMAND ----------

// MAGIC %sql
// MAGIC select name,
// MAGIC sum(na_sales) as North_America,
// MAGIC sum(eu_sales) as Europe,
// MAGIC sum(jp_sales) as Japan,
// MAGIC sum(other_sales) as Other_Sales,
// MAGIC sum(global_sales) as Global_Sales
// MAGIC from Video_Game_Sales
// MAGIC group by name
// MAGIC order by global_sales desc
// MAGIC Limit 10;

// COMMAND ----------

// MAGIC %md
// MAGIC Games per Genre

// COMMAND ----------

// MAGIC %sql
// MAGIC select genre, count(genre) from Video_Game_Sales group by genre order by count(genre) desc

// COMMAND ----------

// MAGIC %md
// MAGIC Games per Genre over time

// COMMAND ----------

// MAGIC %sql
// MAGIC select genre, count(genre), year from Video_Game_Sales group by genre, year order by year

// COMMAND ----------

// MAGIC %md
// MAGIC Total Sales per Market (Grouped by Genre)

// COMMAND ----------

// MAGIC %sql
// MAGIC select
// MAGIC   genre,
// MAGIC   sum(na_sales) as North_America,
// MAGIC   sum(eu_sales) as Europe,
// MAGIC   sum(jp_sales) as Japan,
// MAGIC   sum(other_sales) as Other_Sales,
// MAGIC   sum(global_sales) as Global_Sales
// MAGIC from
// MAGIC   Video_Game_Sales
// MAGIC group by
// MAGIC   genre
// MAGIC order by
// MAGIC   global_sales desc
