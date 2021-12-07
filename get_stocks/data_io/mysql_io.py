import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import datetime
from get_data_from_net.get_history_data import get_single_stack_history_data, get_append_data
from utils.logger import logger


class MysqlIO:
    def __init__(self, params=None):

        self.params = params
        # 连接数据库
        self.engine = create_engine(self.params.mysql_connect_info)
        # 创建数据库
        if not database_exists(self.engine.url):
            create_database(self.engine.url)

    def mysql_input_single_table(self, data_df=None, table_name=None, method='replace'):
        """
        将单个表输入到mysql
        :param data_df: 需要输入mysql的表格
        :param table_name: 表的名字
        :param method: 是否通过替换或者追加的方式加入到表中
        :return:
        """
        logger.info(f'start input table {table_name} to mysql!')
        data_df.to_sql(name=table_name, con=self.engine, if_exists=method, index=None)
        logger.info(f'{table_name} input mysql done')

    def mysql_input_all_stock_data(self, stocks_code_df, method):
        """
        获得所有股票的数据
        :param stocks_code_df: 所有股票的代码和名字
        :param method: replace 代表替换表中所有的数据，append 代表追加，一般获得实时数据是append， 所有历史数据是 replace
        :return:
        """
        # 获得当前数据库所有表名
        table_names = set(self.engine.table_names())
        ###
        if method == 'replace':
            logger.info(f'start get all stocks history data!')
            for i in range(len(stocks_code_df)):
                code, name = tuple(stocks_code_df.iloc[i].tolist())
                logger.info(f'start get {i} rd stock history data')
                # 当前表名已经存在则不再进行爬取
                if code in table_names:
                    logger.info(f'the stock :{name} is in the dbase, dont need get from net again')
                    continue
                # 获得所有历史数据
                global_url = self.params.stock_data_url
                if code[0] == '6':
                    url = global_url[0] + f'1.{code}' + global_url[1]
                else:
                    url = global_url[0] + f'0.{code}' + global_url[1]
                # 获得 股票代码code 的股票的所有历史数据
                data_df = get_single_stack_history_data(url, name)
                # 将此数据输入到数据库,表名以股票代码命名
                if data_df is not None:
                    self.mysql_input_single_table(data_df=data_df, table_name=code, method=method)
        elif method == 'append':
            logger.info(f'start get all stocks today data!')
            data_df = get_append_data(self.params.stock_today_url)
            for i in range(len(data_df)):
                # 检查是否今天的数据已经录入
                tmp_data = data_df.loc[[i]]
                # 是否开市
                if tmp_data['开盘'].values[0] == '-':
                    continue
                code = tmp_data['代码'].values[0]
                tmp_data.drop(columns=['代码'], inplace=True)
                today = datetime.datetime.today()
                # 如果今天是非交易日的处理
                if today.isoweekday() == 6:
                    today += datetime.timedelta(days=-1)
                elif today.isoweekday() == 7:
                    today += datetime.timedelta(days=-2)
                last_transaction_day = today.strftime('%Y-%m-%d')
                # 检查是否今天的数据已经录入
                if code in table_names:
                    # 在表存在的情况下检查是否存在今天的数据
                    sql_code = f"select `日期` from `{code}` order by `日期` desc limit 0,1"
                    last_day = pd.read_sql_query(sql_code, con=self.engine, index_col=None)
                    last_day = last_day.values[0]
                    # 检查今天的数据是否已经被录入
                    if last_transaction_day == last_day:
                        logger.info(f"stock {code} today's data already input database, dont neet input again!")
                        continue
                tmp_data.insert(0, '日期', last_transaction_day)
                self.mysql_input_single_table(data_df=tmp_data, table_name=code, method=method)
        else:
            logger.error(f'method {method} is not defined')

    def mysql_output_all(self, table_name=None):
        pass

    def mysql_output_some(self, sql_code=''):
        return pd.read_sql_query(sql_code, self.engine)








