# Video Game Sales Data Analysis

## Project Overview
The Video Game Sales Data Analysis project aims to explore and analyze a dataset containing sales information for video games across different platforms. Utilizing Databricks, the analysis leverages the power of Apache Spark for large-scale data processing and visualization. The primary goal is to provide insights into trends, performance across platforms, genres, and sales over time.

## Objectives
- Perform Exploratory Data Analysis (EDA) on the video game sales dataset.
- Identify the top-selling games, platforms, and genres.
- Visualize sales trends over time.
- Understand regional sales distribution.

## Dataset Description
The dataset consists of several attributes, including:
- `Name`: Title of the video game.
- `Platform`: Console/Platform on which the game is available.
- `Year`: Year of release.
- `Genre`: Genre of the game (Action, Sports, Adventure, etc.).
- `Publisher`: Publisher of the game.
- `NA_Sales`: Sales in North America (in millions).
- `EU_Sales`: Sales in Europe (in millions).
- `JP_Sales`: Sales in Japan (in millions).
- `Other_Sales`: Sales in other regions (in millions).
- `Global_Sales`: Total worldwide sales (in millions).

## Requirements
- Databricks account and workspace.
- Spark environment (included in Databricks).
- Libraries: PySpark, Pandas, Matplotlib/Seaborn (installed via Databricks notebook).

## Implementation Steps
1. **Set up Databricks Workspace**
   - Create a new notebook in Databricks.
   - Configure the notebook for Python.

2. **Load the Dataset**
   - Upload the dataset to Databricks and load it into a Spark DataFrame.

3. **Data Cleaning**
   - Inspect the DataFrame for missing values and data inconsistencies.
   - Clean the dataset by handling missing values appropriately.

4. **Exploratory Data Analysis**
   - Calculate summary statistics.
   - Analyze trends over time for game sales.
   - Visualize the sales distribution by genre and platform.

5. **Visualization**
   - Create plots to visualize relationships and trends, such as:
     - Top games by sales.
     - Sales comparisons across platforms.
     - Yearly sales trends.

6. **Insights and Conclusions**
   - Summarize the key findings from the analysis.
   - Discuss implications for stakeholders in the video game industry.

## How to Run the Analysis
1. **Access Databricks**
   - Log into your Databricks account and go to your workspace.

2. **Create a New Notebook**
   - Create a new notebook and select the Python language.

3. **Upload the Dataset**
   - Upload the video game sales dataset into Databricks.

4. **Run the Analysis Cells**
   - Run the cells in the notebook step by step to perform the analysis.

## Results
The results will include various visualizations and a summary of insights regarding video game sales, highlighting patterns and significant findings from the dataset.


