# Sales Forecasting Project
## Overview
This project focuses on building a Credit Scoring Model using transactional and behavioral data provided by an eCommerce platform. The goal is to enable a buy-now-pay-later service, allowing customers to purchase products on credit if they qualify.

Credit scoring is the process of assigning a numerical score to represent a borrower's creditworthiness. Traditionally, credit scoring models have relied on statistical techniques to analyze borrower behavior and loan performance. The objective of this project is to leverage machine learning techniques to enhance traditional credit scoring methods.

## Objectives
- Define a Default Proxy Variable: Identify and define a proxy variable that categorizes users as either high-risk (likely to default) or low-risk (unlikely to default).

- Feature Selection: Select observable features from the data that serve as strong predictors (i.e., those with high correlation) of the default variable.

- Risk Probability Model: Build a machine learning model that assigns a risk probability to new customers, estimating the likelihood of default.

- Credit Scoring Model: Develop a model that converts the risk probability estimates into a credit score for each user.


## Getting Started
### Prerequisites
Make sure you have the following installed:
  * Python 3.x
  * Pip (Python package manager)

### Installation
Clone the repository:
```
git clone https://github.com/Yosef-ft/Credit_Risk_Model.git
cd Credit_Risk_Model
```
Create a virtual environment and activate it:
```
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
Install the required packages:
```
pip install -r requirements.txt
```
