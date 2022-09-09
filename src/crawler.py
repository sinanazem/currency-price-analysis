
import pandas as pd

import requests
from loguru import logger



class RequestAPI:

    def __init__(self,api):

        self.api = api
        try:
            # request for getting api
            response = requests.get(self.api)
            logger.info(f'Response {response}')
            self.data= response.json()
            logger.info(f'Change format to json!')


        except:
            print(f'{self.api} dose not exist!')

    def get_dataframe(self,columns=None):

        df = pd.DataFrame(self.data['data'],columns=columns)

        return df




































