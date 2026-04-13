---
source_type: web
title: "TimeSeries Analysis 📈A Complete Guide 📚"
author:
  - 
  - "[[andreshg]]"
created_at: 2026-04-06
status: inbox
created: 2026-04-06
description: "Explore and run machine learning code with Kaggle Notebooks | Using data from Acea Smart Water Analytics"
tags:
  - 
  - "clippings"
source_url: "https://www.kaggle.com/code/andreshg/timeseries-analysis-a-complete-guide/notebook"
published_at: 2021-03-06
related_concepts: []
topics:
  - timeseries-analysis
  - 时间序列分析
---

AndresHG · 5y ago · 178,793 views

## TimeSeries Analysis 📈A Complete Guide 📚

[Notebook](https://www.kaggle.com/code/andreshg/timeseries-analysis-a-complete-guide/notebook) [Input](https://www.kaggle.com/code/andreshg/timeseries-analysis-a-complete-guide/input) [Output](https://www.kaggle.com/code/andreshg/timeseries-analysis-a-complete-guide/output) [Logs](https://www.kaggle.com/code/andreshg/timeseries-analysis-a-complete-guide/log) [Comments (209)](https://www.kaggle.com/code/andreshg/timeseries-analysis-a-complete-guide/comments)

## Runtime

1m 48s

## Input

COMPETITIONS

Acea Smart Water Analytics

## Tags

[Matplotlib](https://www.kaggle.com/code?tagIds=16607-Matplotlib) [NumPy](https://www.kaggle.com/code?tagIds=16609-NumPy) [pandas](https://www.kaggle.com/code?tagIds=16611-pandas) [Seaborn](https://www.kaggle.com/code?tagIds=16623-Seaborn)

## Language

Python

## Table of Contents

[TimeSeries 📈 ARIMA, Prophet, ADF, PACF... 📚 Beginner to Pro](https://www.kaggle.com/code/andreshg/timeseries-analysis-a-complete-guide/notebook#TimeSeries-%F0%9F%93%88-ARIMA,-Prophet,-ADF,-PACF...-%F0%9F%93%9A-Beginner-to-Pro) [Table of Content](https://www.kaggle.com/code/andreshg/timeseries-analysis-a-complete-guide/notebook#Table-of-Content) [1\. Data visualization 📊](https://www.kaggle.com/code/andreshg/timeseries-analysis-a-complete-guide/notebook#1.-Data-visualization-%F0%9F%93%8A) [2\. Data Preprocessing ⚙️](https://www.kaggle.com/code/andreshg/timeseries-analysis-a-complete-guide/notebook#2.-Data-Preprocessing-%E2%9A%99%EF%B8%8F) [Chronological Order and Equidistant Timestamps](https://www.kaggle.com/code/andreshg/timeseries-analysis-a-complete-guide/notebook#Chronological-Order-and-Equidistant-Timestamps) [2.1 Handle Missings](https://www.kaggle.com/code/andreshg/timeseries-analysis-a-complete-guide/notebook#2.1-Handle-Missings) [2.2 Smoothing data / Resampling](https://www.kaggle.com/code/andreshg/timeseries-analysis-a-complete-guide/notebook#2.2-Smoothing-data-/-Resampling) [2.3 Stationarity](https://www.kaggle.com/code/andreshg/timeseries-analysis-a-complete-guide/notebook#2.3-Stationarity) [2.3.1 Augmented Dickey-Fuller (ADF)](https://www.kaggle.com/code/andreshg/timeseries-analysis-a-complete-guide/notebook#2.3.1-Augmented-Dickey-Fuller-\(ADF\)) [2.3.2 Transforming](https://www.kaggle.com/code/andreshg/timeseries-analysis-a-complete-guide/notebook#2.3.2-Transforming) [2.3.3 Differencing](https://www.kaggle.com/code/andreshg/timeseries-analysis-a-complete-guide/notebook#2.3.3-Differencing) [3\. Feature engineering 🔧](https://www.kaggle.com/code/andreshg/timeseries-analysis-a-complete-guide/notebook#3.-Feature-engineering-%F0%9F%94%A7) [3.1 Encoding Cyclical Features](https://www.kaggle.com/code/andreshg/timeseries-analysis-a-complete-guide/notebook#3.1-Encoding-Cyclical-Features) [3.2 TimeSeries Decomposition](https://www.kaggle.com/code/andreshg/timeseries-analysis-a-complete-guide/notebook#3.2-TimeSeries-Decomposition) [3.3 Lag](https://www.kaggle.com/code/andreshg/timeseries-analysis-a-complete-guide/notebook#3.3-Lag) [4\. Exploratory Data Analysis 📊](https://www.kaggle.com/code/andreshg/timeseries-analysis-a-complete-guide/notebook#4.-Exploratory-Data-Analysis-%F0%9F%93%8A) [4.1 Autocorrelation Analysis](https://www.kaggle.com/code/andreshg/timeseries-analysis-a-complete-guide/notebook#4.1-Autocorrelation-Analysis) [5\. Modeling 🧩](https://www.kaggle.com/code/andreshg/timeseries-analysis-a-complete-guide/notebook#5.-Modeling-%F0%9F%A7%A9) [5.1 Models for Univariate Time Series](https://www.kaggle.com/code/andreshg/timeseries-analysis-a-complete-guide/notebook#5.1-Models-for-Univariate-Time-Series) [5.1.1 Prophet](https://www.kaggle.com/code/andreshg/timeseries-analysis-a-complete-guide/notebook#5.1.1-Prophet) [5.1.2 ARIMA](https://www.kaggle.com/code/andreshg/timeseries-analysis-a-complete-guide/notebook#5.1.2-ARIMA) [5.1.3 Auto-ARIMA](https://www.kaggle.com/code/andreshg/timeseries-analysis-a-complete-guide/notebook#5.1.3-Auto-ARIMA) [5.1.4 LSTM](https://www.kaggle.com/code/andreshg/timeseries-analysis-a-complete-guide/notebook#5.1.4-LSTM) [5.2 Models for Multivariate Time Series](https://www.kaggle.com/code/andreshg/timeseries-analysis-a-complete-guide/notebook#5.2-Models-for-Multivariate-Time-Series) [5.2.1 Multivariate Prophet](https://www.kaggle.com/code/andreshg/timeseries-analysis-a-complete-guide/notebook#5.2.1-Multivariate-Prophet) [6\. Conclusions 💎](https://www.kaggle.com/code/andreshg/timeseries-analysis-a-complete-guide/notebook#6.-Conclusions-%F0%9F%92%8E) [7\. References 📝](https://www.kaggle.com/code/andreshg/timeseries-analysis-a-complete-guide/notebook#7.-References-%F0%9F%93%9D)

![[thumb76_76.png|Profile picture for undefined]]

Competition Notebook

[Acea Smart Water Analytics](https://www.kaggle.com/competitions/acea-water-prediction)

<iframe src="https://www.kaggleusercontent.com/kf/55927590/eyJhbGciOiJkaXIiLCJlbmMiOiJBMTI4Q0JDLUhTMjU2In0..HF2f-SuEoz0RDM4bB5DF3g.jEwxv1W1ZcH-YDxpc-m_arKjoBcdJdQJU9dwWRx2NSY5fbcFNJ02qQ7XIwPdMToW3sXjewQl6ibEtWOqz-tXbFGV3KZFB5kKoWAvtMChbBEITK9byt9yM4uB-DXg-JQ6hZKFsC8WzA25YthsfqzIJm70itpkLggVV5mUDI4zb69n-JRlegO1BYaJCTa2MopSxAWYEXIiyeSobU7i2kNr5MQUCzuSGolgzDvWfyoYgVjYnj0ra4v9RvwlOJ_YmM5mTpr0rboKVLUdwpz3IHriZsaXBnwr8pJjZDkQdZog5-xFXAvl_kr4o-x5oDB3GIg1gdBfIzPX6PrF_drN9Ho5dpfXn6VYgsKTWqjYldc-UebCyXowPS-utoy5XZTSn2VfLM3HBFIx9AjWRntuWiap3GbdQOWfLVx0czp8JZaDyIQm6jHJhCYLRLNNPud1MckgTYyq8yw7Ag9kQRiKcJaufztY9rr_H0pzjrIsJwaMnjBmMJO5s0M3XDsOsrJFHYcGcRtw3Q-ETzVKIY9QareVmuPJjPYY9S4KShLHYhUGpIjDV2Cr2q2GUfJBhNV3GK2RJOE3RHIriz2CqjgFHTKA-YqAZmk-KRyDMK6SkfoYzuf4Eni3xPkGd-BV007F8HpViTAQNMajTCOTE-tkcJo3wA.wNAhk82l-zsu_ea-8JCBQw/__results__.html?sharingControls=true" title="Main Notebook Content"></iframe>

## License

This Notebook has been released under the [Apache 2.0](http://www.apache.org/licenses/LICENSE-2.0) open source license.

## Continue exploring

- ![[raw/assets/attachments/timeseries/input_light.svg]]
	Input
	1 file
- ![[raw/assets/attachments/timeseries/output_light.svg]]
	Output
	0 files
- ![[raw/assets/attachments/timeseries/logs_light.svg]]
	Logs
	107.9 second run - successful
- ![[raw/assets/attachments/timeseries/comments_light.svg]]
	Comments
	209 comments