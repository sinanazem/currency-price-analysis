import re
from datetime import datetime
from datetime import datetime as dt

import numpy as np
import pandas as pd
import plotly
import plotly.graph_objects as go
import seaborn as sns
from loguru import logger
from matplotlib import dates as mdates
from matplotlib import pyplot as plt

from src.utils import DataBaseClass


class CreatePlots:

    def read_data(self,username,password,host,port,db_name,command,table_name):
        obj_data_base_class = DataBaseClass(username=username, password=password, host=host, port=port, db_name=db_name)
        data = obj_data_base_class.read_table(command=command)
        col_sql_query = f""" SELECT Column_name 
                            FROM INFORMATION_SCHEMA.COLUMNS
                            WHERE TABLE_NAME = '{table_name}' """

        columns = obj_data_base_class.read_table(command=col_sql_query)
        columns = [item[0] for item in columns]
        df = pd.DataFrame(data,columns=columns)


        return df

    def data_processing(self,df):

        currency_df = df
        currency_df = currency_df[1:]

        currency_df['g_date'] =  pd.to_datetime(currency_df['g_date'], format='%Y/%m/%d')

        for col in ['close','highest','lowest','open']:
            currency_df[col] = currency_df[col].str.replace(',','').astype('float')

        currency_df['diff_balance'] = currency_df['diff_balance']\
            .apply(lambda x: "-" + "".join(
                re.findall('\d+', x)) if 'low' in x else "".join(re.findall('\d+', x)))

        currency_df['pct_change'] = currency_df['pct_change']\
            .apply(lambda x: "".join(re.findall(r"\d+\.\d+", x)))

        return currency_df

    def create_plot(self,df):

        currency_df = df
               # Final daily close values (daily close prices)
        x_values = currency_df['g_date']
        y_values = currency_df['close']
        ax = plt.gca()

        formatter = mdates.DateFormatter("%Y-%m-%d")
        locator = mdates.DayLocator()
        plt.plot(x_values, y_values)
        plt.savefig("src/plots/out.jpg")

        logger.info(f'daily close prices plot stored in src/plots/out.jpg')

        # Daily candlestick chart

        fig = go.Figure(data=[go.Candlestick(x=df['g_date'],
                        open=currency_df['open'],
                        high=currency_df['highest'],
                        low=currency_df['lowest'],
                        close=currency_df['close'])])


        fig.write_image("src/plots/Candlestick.png")
        plotly.offline.plot(fig, filename='src/plots/Candlestick.html')
        logger.info(f'Daily candlestick chart stored in src/plots/Candlestick.html')

        logger.info('Plots Created!')


