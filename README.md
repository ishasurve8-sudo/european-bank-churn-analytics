# 🏦 European Bank — Customer Segmentation & Churn Analytics

## 📌 Project Overview
This project analyses customer churn patterns across 10,000 European banking customers from France, Germany, and Spain. Built as part of a Financial Analyst Internship project for the European Central Bank.

## 🔗 Live Dashboard
👉 [Click here to view the live dashboard](https://european-bank-churn-analytics-53hqopyektsby4wvqgjsup.streamlit.app/)

## 📊 Key Findings
- Overall churn rate: **20.4%**
- Germany has the highest churn at **32.4%** — double France and Spain
- Age group 46–60 churns at **51.1%** — highest of all segments
- Inactive members churn **88% more** than active members
- Customers with 3+ products churn at **82–100%**

## 🗂️ Project Structure
| File | Description |
|---|---|
| `app.py` | Main Streamlit dashboard code |
| `European_Bank__1_.csv` | Dataset with 10,000 customer records |
| `requirements.txt` | Python libraries needed |

## 📁 Dataset Description
| Column | Description |
|---|---|
| CustomerId | Unique customer identifier |
| Geography | France, Spain, Germany |
| Gender | Male / Female |
| Age | Customer age |
| Tenure | Years with the bank |
| Balance | Account balance |
| NumOfProducts | Number of bank products |
| IsActiveMember | Activity indicator |
| Exited | Churn indicator (1 = Churned) |

## 🔍 Dashboard Sections
- **Overview** — Overall churn summary and KPI cards
- **Geography** — Country wise churn comparison
- **Demographics** — Age, gender and tenure patterns
- **Financial Profile** — Balance, credit score and product analysis
- **High Value Customers** — Premium customer churn explorer

## 🛠️ Technologies Used
- Python
- Streamlit
- Pandas
- Plotly

## 👤 Author
- Name: Isha Rohit Surve
- Name: Your Name Here
- Role: Financial Analyst Intern
- Organisation: European Central Bank
