import math

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import missingno as msno
from Utils import logger
from statsmodels.distributions.empirical_distribution import ECDF

class Plots:
    # def __init__(self, data):
    #     self.data = data


    def visualize_missing_values(self, data):
        '''
        This method generates a heatmap to visually represent the missing values in the dataset.
        '''
        logger.debug("Plotting missing values...")
        try:
            missing_cols = data.columns[data.isna().any()]

            missing_data = data[missing_cols]

            msno.bar(missing_data)    
        except Exception as e:
            logger.error(f"Error in plotting missing values: {e}")

    
    
    def visualize_outliers(self, data):
        '''
        This funcions helps in visualizing outliers using boxplot
        '''
        logger.debug("Plotting Outliers...")

        try:
            numerical_cols = data.select_dtypes(include=['float64', 'int64']).columns
            num_columns = len(numerical_cols) # length of numerical columns
            n_cols = int(math.sqrt(num_columns))

            nrows = num_columns // n_cols + num_columns % n_cols

            fig, axes = plt.subplots(nrows=nrows, ncols=n_cols, figsize=(20,12))
            axes = axes.flatten()

            for i, col in enumerate(numerical_cols):
                sns.boxplot(y=data[col], ax=axes[i])
                axes[i].set_title(col)

            for j in range(i + 1, len(axes)):
                fig.delaxes(axes[j])            

            plt.tight_layout()
            plt.show()

        except Exception as e:
            logger.error(f"Error in plotting Outliers: {e}")    


    def visualize_correlations(self, data: pd.DataFrame, num_cols: list):
        '''
        This function is used to find the correaltion for numerical columns

        Parameters:
        -----------
            data(pd.DataFrame)
            num_cols(list): List of numerical columns for analysis
        
        Returns:
            sns.plot
        '''
        logger.debug('Plotting Heatmap for numerical columns')
        plt.figure(figsize=(10, 8))
        try: 
            correlation = data[num_cols].corr()
            sns.heatmap(correlation, annot=True, cbar=True, cmap='Blues', annot_kws={"weight": "bold"})
            plt.title('Correlation between numerical columns')
            plt.plot()
        except Exception as e:
            logger.error(f'Error ploting the heatmap: {e}')


    def plot_ecdf (self, column, title= 'ECDF Plot', xlabel = 'Sales', ylabel = 'Percentage'):
        '''
        Funtion to plot ecdf taking a column of data as input

        Parameters:
            column(pd.Series)
        '''
        cdf = ECDF(column)

        plt.plot(cdf.x, cdf.y, marker = '.', linestyle='none')
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.margins(0.02)                 


    def trend_col(self, data, col):
        '''
        This function plots a line plot for a given column
        '''

        plt.figure(figsize=(10,6))
        sns.lineplot(data[col], linewidth=2.5, color='royalblue')

        plt.title(f'Trend of {col}', fontweight='bold')
        plt.ylabel(f"{col}")

        plt.xticks(rotation=45)

        plt.grid(True, linestyle='--')
        plt.tight_layout()
        plt.show()



    def cat_distribution(self, data: pd.DataFrame, col: str, value_count: bool = True):
        '''
        This function plots a distrubution for a bar plot for a given column

        Parameters:
        ----------
            data(pd.DataFrmame)
            col: the column to plot
            value_count(bool): whether to plot by counting values or not

        '''

        plt.figure(figsize=(10,6))
        logger.debug("plotting categorical distribution...")
        try:
            if value_count:
                sns.barplot(x=data[col].value_counts().index,
                            y=data[col].value_counts().values,
                            palette='pastel', hue=data[col].value_counts().index)
                
            else:
                sns.barplot(x=data.index,
                            y=data[col],
                            palette='pastel', hue=data.index)                

            plt.xticks(rotation=45)

            plt.ylabel(f'{col}', fontweight='bold')
            plt.title(f'Distribution for {col}')
            plt.grid(True, linestyle='--')
            plt.tight_layout()
            plt.show()

        except Exception as e:
            logger.error(f"Can't plot the distribution: {e}")


    def bivariant_distribution(self, data:pd.DataFrame, col: str, hue: str):
        '''
        This function plots columns in respect to another column (plots countplot for two columns)


        Parameter:
        ----------
            col(str): The column to plot
            hue(str): The column to compare each col with

        Retruns:
        --------
            plt.show()
        '''

        fig = plt.figure(figsize=(10,6))

        sns.countplot(x=col, data=data, hue=hue, palette = 'pastel')
        
        plt.xticks(rotation=45)
        plt.title(f'Comparing {col} in respect to {hue}')
        plt.show()


    def RFM_Space_visualization(self, RFM_data):
        '''
        This function plots a 3d scatter plot to visualize RFM space:

        Parameter:
        ----------
            RFM_data(pd.DataFrame): dataframe containing R_rank_norm, F_rank_norm, M_rank_norm, RFM_Score
        '''
        fig = plt.figure(figsize=(10,6))
        ax = fig.add_subplot(projection='3d')

        ax.scatter(RFM_data['R_rank_norm'], RFM_data['F_rank_norm'], RFM_data['M_rank_norm'], c=RFM_data['RFM_Score'], cmap='viridis')

        ax.set_xlabel('Recency Rank')
        ax.set_ylabel('Frequency Rank')
        ax.set_zlabel('Monetary Rank')
        ax.set_title('RFMS Space Visualization')

        plt.colorbar(ax.scatter(RFM_data['R_rank_norm'], RFM_data['F_rank_norm'], RFM_data['M_rank_norm'], c=RFM_data['RFM_Score'], cmap='viridis'), label='RFM Score')
        plt.show()