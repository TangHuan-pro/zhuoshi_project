"""
参数解析
"""


class Params:
    def __init__(self):
        self.stock_codes_url = None
        self.stock_data_url = None
        self.mysql_connect_info = None
        self.stock_today_url = None

    def parse_params(self, original_params):
        self.stock_codes_url = original_params['url']['stock_codes_url']
        self.stock_data_url = original_params['url']['stock_data_url']
        self.stock_today_url = original_params['url']['stock_today_url']
        self.mysql_connect_info = original_params['mysql_url']


