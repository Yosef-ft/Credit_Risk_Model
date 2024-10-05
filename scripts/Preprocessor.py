import pandas as pd


class FeatureEngineering:
    
    def __init__ (self, data):

        self.data = data


    def aggregate_features(self):
        self.data['Total_transaction_amount'] = self.data.groupby(by='CustomerId')['Amount'].transform("sum")
        self.data['Average_transaction_amount'] = self.data.groupby(by='CustomerId')['Amount'].transform("mean")
        self.data['Transaction_Count'] = self.data.groupby(by='CustomerId')['TransactionId'].transform('size')
        self.data['STD_Transaction_Amount'] = self.data.groupby(by='CustomerId')['Amount'].transform('std')


    def feature_extraction(self):
        self.data['Transaction_Hour']= self.data['TransactionStartTime'].dt.hour
        self.data['Transaction_Month'] = self.data['TransactionStartTime'].dt.month
        self.data['Transaction_year'] = self.data['TransactionStartTime'].dt.year
        self.data['Transaction_Day'] = self.data['TransactionStartTime'].dt.day


    def engineer_features(self):
        self.feature_extraction()
        self.aggregate_features()
        return self.data



