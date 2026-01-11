# GOG Games Data Analysis

This repository contains a data analysis coursework project focused on exploring how price, genre, and discount campaigns relate to game popularity on the GOG.com platform.

The project follows a simple data pipeline approach:

1. Clean and prepare raw data
2. Analyze the cleaned dataset
3. Generate insights and visualizations

## Project Overview

Research topic: <br>
**The relationship between price, genre, and discount campaigns and game popularity on GOG.com.**

The analysis is based on a publicly available GOG games dataset and focuses on understanding:

- Common price points

- Popular genres

- Release year trends

- The relationship between price, discounts, and popularity (user review count)

The full analysis and conclusions are documented in the accompanying PDF report.

## Repository Structure
├── gog_games_dataset.csv        <br>
├── cleaned_gog_dataset.csv      <br>
├── data_cleaning.py              <br>
├── analysis.py                  <br>
└── report.pdf                    <br>

## Data Pipeline
### 1. Data Cleaning (data_cleaning.py)

This script prepares the raw dataset for analysis.

**Key steps:**

- Removes columns not relevant to the analysis (e.g. image and video links)

- Keeps variables related to pricing, genres, discounts, popularity, and release year

- Outputs a cleaned dataset used in the analysis phase

**Input:**
gog_games_dataset.csv

**Output:**
cleaned_gog_dataset.csv

### 2. Data Analysis (analysis.py)

This script performs the actual analysis using the cleaned dataset.

**The analysis includes:**

1. Most common game prices

2. Most common genres

3. Number of games by release year

4. Price compared to popularity (number of user reviews)

5. Effect of discounts on popularity (cross-tabulation)

6. Most popular genres

7. (Extra) Popularity trends by release year

The script produces visualizations and summary statistics to support the findings presented in the report.

## How to Run the Project
### Requirements

- Python 3.x

- pandas

- matplotlib

- numpy

- scipy

### Steps

1. Run the data cleaning script:

python data_cleaning.py


2. Run the analysis script:

python analysis.py


Make sure both scripts are run in the same directory as the CSV files.

## Tools & Technologies

Python

pandas

matplotlib

numpy

CSV data processing

## Notes

This project was completed as part of a data analytics coursework assignment.

The focus is on data cleaning, exploratory analysis, and visualization.
