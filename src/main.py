from src.crawler import RequestAPI
from utils import DataBaseClass
from src.plots import CreatePlots



if __name__ == "__main__":

    # Request for API
    api = "https://api.accessban.com/v1/market/indicator/summary-table-data/price_dollar_rl?lang=fa"
    obj_request_api = RequestAPI(api=api)
    currency_df = obj_request_api.get_dataframe(columns=['open',
                                        'lowest',
                                        'highest',
                                        'close',
                                        'diff_balance',
                                        'pct_change',
                                        'g_date',
                                        'j_date'])

    # Store data

    obj_data_base_class = DataBaseClass('postgres','ss','0.0.0.0',5432,'currency_db')
    obj_data_base_class.store_data(currency_df,sql_table_name='currency_data')


    # Create Plots
    obj_create_plots = CreatePlots()
    sql = """ SELECT * FROM currency_data """
    raw_df = obj_create_plots.read_data(username='postgres',password='ss',host='0.0.0.0',port=5432,db_name='currency_db',command=sql,table_name='currency_data')
    df = obj_create_plots.data_processing(raw_df)
    df = df[df['g_date'] > '2021-05-11']
    obj_create_plots.create_plot(df)
