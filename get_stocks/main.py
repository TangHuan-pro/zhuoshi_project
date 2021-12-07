from utils.parse_params import Params
from get_data_from_net.get_history_data import get_stack_code, get_single_stack_history_data
from data_io.mysql_io import MysqlIO
from utils.logger import logger
import time
if __name__ == '__main__':
    # 股票代码url
    STOCK_CODES_URL = "http://96.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112408956068365762069_1638337924300&pn=1&pz=20&po=1&np=2&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23,m:0+t:81+s:2048&fields=f12,f13,f14,f15&_=1638337924301"

    # 股票数据url，只需要在中间加上下述字符串即可
    # 上证的 '1.' + 股票代码, 其他的 是 '0.' + 股票代码
    STOCK_DATA_URL = \
        ("http://4.push2his.eastmoney.com/api/qt/stock/kline/get?cb=jQuery112408332917201844157_1638357848630&secid=",
         "&ut=fa5fd1943c7b386f172d6893dbfba10b&fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5%2Cf6&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58%2Cf59%2Cf60%2Cf61&klt=101&fqt=0&end=20500101&lmt=1000000&_=1638347585498"
         )
    STOCK_TODAY_URL = "https://96.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112408956068365762069_1638337924300&pn=1&pz=20&po=1&np=2&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23,m:0+t:81+s:2048&fields=f12,f2,f3,f4,f5,f6,f7,f8,f15,f16,f17&_=1638337924301"
    original_params = {
        'url': {'stock_codes_url': STOCK_CODES_URL, 'stock_data_url': STOCK_DATA_URL, 'stock_today_url': STOCK_TODAY_URL},
        'mysql_url': 'mysql+pymysql://root:root@localhost:3306/stocks_data?charset=utf8'
    }
    params = Params()
    params.parse_params(original_params)

    # 获取股票代码
    stocks_code_df = get_stack_code(params.stock_codes_url)

    # step1: 将股票代码存到数据库
    mysql_obj = MysqlIO(params)
    mysql_obj.mysql_input_single_table(data_df=stocks_code_df, table_name='stocks_code', method='replace')

    # step2: 根据股票代码获得所有的历史数据并存到数据库
    # start = time.time()
    # mysql_obj.mysql_input_all_stock_data(stocks_code_df, method='replace')
    # duration = time.time()-start
    # logger.info(f'time to get history data is {duration//60} mins , {duration%60} s')
    # 获得今天的所有股票数据

    ## step3: 获得当天股票数据
    start_today = time.time()
    mysql_obj.mysql_input_all_stock_data(stocks_code_df, method='append')
    duration_today = time.time() - start_today
    logger.info(f'time to get tiday data is {duration_today // 60} mins , {duration_today % 60} s')










