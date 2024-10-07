import os
import logging

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import missingno as msno


# ANSI Escape code to make the printing more appealing
ANSI_ESC = {
    "PURPLE": "\033[95m",
    "BLUE": "\033[94m",
    "GREEN": "\033[92m",
    "RED": "\033[91m",
    "ENDC": "\033[0m",
    "BOLD": "\033[1m",
    "ITALICS" :"\033[3m"
}



log_dir = os.path.join(os.path.split(os.getcwd())[0], 'logs')

if not os.path.exists(log_dir):
    os.mkdir(log_dir)



log_file_info = os.path.join(log_dir, 'Info.log')
log_file_error = os.path.join(log_dir, 'Error.log')


info_handler = logging.FileHandler(log_file_info)
info_handler.setLevel(logging.INFO)

error_handler = logging.FileHandler(log_file_error)
error_handler.setLevel(logging.ERROR)

formatter = logging.Formatter('%(asctime)s - %(levelname)s :: %(message)s',
                              datefmt="%Y-%m-%d %H:%M")

info_handler.setFormatter(formatter)
error_handler.setFormatter(formatter)


console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.DEBUG)
console_handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(info_handler)
logger.addHandler(error_handler)
logger.addHandler(console_handler)


class DataUtils:
    # def __init__(self, data):
    #     self.data = data


    def load_data(self, file_name: str)->pd.DataFrame:
        '''
        Load the file name from the data directory

        Parameters:
            file_name(str): name of the file

        Returns:
            pd.DataFrame
        '''
        logger.debug("Loading data from file...")
        try:
            data = pd.read_csv(f"../data/{file_name}", low_memory=False)
            return data

        except Exception as e:
            logger.error(f"Error loading data: {e}")
            return None
        


    def data_info(self, data) -> pd.DataFrame:
        '''
        Provides detailed information about the data, including:
            - Percentage of missing values per column
            - Number of missing values per column
            - Data types of the columns
        It also highlights:
            - The total number of rows and columns in the dataset
            - Columns with the most missing values
            - Columns with more than 50% missing values

        Parameters:
            data(pd.DataFrame): The dataset 
        
        Returns:
            info_df(pd.DataFrame)
        '''
        
        missing_values = data.isna().sum()
        missing_percent = round(data.isna().mean() * 100, 2)
        data_types = data.dtypes
        
        info_df = pd.DataFrame({
            "Missing Values": missing_values,
            "Missing Percentage": missing_percent,
            "Data Types": data_types
        })


        info_df = info_df[missing_percent > 0]
        info_df = info_df.sort_values(by='Missing Percentage', ascending=False)

        max_na_col = list(info_df.loc[info_df['Missing Values'] == info_df['Missing Values'].max()].index)
        more_than_half_na = list(info_df.loc[info_df['Missing Percentage'] > 50].index)
        

        print(f"\n{ANSI_ESC['BOLD']}Dataset Overview{ANSI_ESC['ENDC']}")
        print(f"---------------------")
        print(f"- {ANSI_ESC['ITALICS']}Total rows{ANSI_ESC['ENDC']}: {data.shape[0]}")
        print(f"- {ANSI_ESC['ITALICS']}Total columns{ANSI_ESC['ENDC']}: {data.shape[1]}\n")

        duplicated_rows = int(data.duplicated().sum())
        if duplicated_rows == 0:
            print(f"{ANSI_ESC['GREEN']}No Duplicated data found in the dataset.{ANSI_ESC['ENDC']}\n")
        else:
             print(f"- {ANSI_ESC['RED']}Number of duplicated rows are{ANSI_ESC['ENDC']}: {duplicated_rows}")
        
        if info_df.shape[0] > 0:
            print(f"{ANSI_ESC['BOLD']}Missing Data Summary{ANSI_ESC['ENDC']}")
            print(f"------------------------")
            print(f"- {ANSI_ESC['ITALICS']}Columns with missing values{ANSI_ESC['ENDC']}: {info_df.shape[0]}\n")
            
            print(f"- {ANSI_ESC['ITALICS']}Column(s) with the most missing values{ANSI_ESC['ENDC']}: `{', '.join(max_na_col)}`")
            print(f"- {ANSI_ESC['RED']}Number of columns with more than 50% missing values{ANSI_ESC['ENDC']}: `{len(more_than_half_na)}`\n")


            if more_than_half_na:
                print(f"{ANSI_ESC['BOLD']}Columns with more than 50% missing values:{ANSI_ESC['ENDC']}")
                for column in more_than_half_na:
                    print(f"   - `{column}`")
            else:
                print(f"{ANSI_ESC['GREEN']}No columns with more than 50% missing values.{ANSI_ESC['ENDC']}")
        else:
            print(f"{ANSI_ESC['GREEN']}No missing data found in the dataset.{ANSI_ESC['ENDC']}")

        print(f"\n{ANSI_ESC['BOLD']}Detailed Missing Data Information{ANSI_ESC['ENDC']}")
        print(info_df)

        return info_df



class WoE:

    # Function to compute Weight of Evidence

    def calculate_woe_iv(self,dataset, feature, target):
        lst = []
        for i in range(dataset[feature].nunique()):
            val = list(dataset[feature].unique())[i]
            lst.append({
                'Bin Values': val,
                'All': dataset[dataset[feature] == val].count()[feature],
                'Good': dataset[(dataset[feature] == val) & (dataset[target] == 0)].count()[feature],
                'Bad': dataset[(dataset[feature] == val) & (dataset[target] == 1)].count()[feature]
            }) 
        dset = pd.DataFrame(lst)
        dset['Distr_Good'] = dset['Good'] / dset['Good'].sum()
        dset['Distr_Bad'] = dset['Bad'] / dset['Bad'].sum()
        dset['WoE'] = np.log(dset['Distr_Good'] / dset['Distr_Bad'])
        dset = dset.replace({'WoE': {np.inf: 0, -np.inf: 0}})
        dset['IV'] = (dset['Distr_Good'] - dset['Distr_Bad']) * dset['WoE']
        iv = dset['IV'].sum()
        dset = dset.sort_values(by='WoE')
        return dset, iv
    


    # Computing WoEs and IVs
    def compute_iv(self, train_bins):
        lst = [] 
        IV_df = pd.DataFrame(columns=['Variable','IV']) 
        for col in train_bins.columns:
            if col == 'RiskResult': continue 
            else:
                df, iv = self.calculate_woe_iv(train_bins, col, 'RiskResult')
                    
            lst.append(df)
            
            new_row = pd.DataFrame({
                "Variable": [col],
                "IV": [iv]
            })    

            IV_df = pd.concat([IV_df, new_row], ignore_index=True)

        return IV_df
        

        