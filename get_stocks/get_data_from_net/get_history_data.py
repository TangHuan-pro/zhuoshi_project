## utils
## 获取股票代码
import re
import pandas as pd
from urllib import request
from utils.do_again_decorator import do_again_decorator
from utils.logger import logger


def get_stack_code(url):
    """
    :param url: 所有A股股票的页面的url
    :return: a dataframe with all A stocks code and name
    """
    headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36',
    'Host':"96.push2.eastmoney.com"
    }
    # 这个url需要抓包实现
    # 由url 获得网站 html 文件
    logger.info('start get all stock codes of A Market')
    req = request.Request(url=url, headers=headers)
    resp = request.urlopen(req)
    html = resp.read().decode('utf-8')
    p = re.compile('"f12":(.*?),.*?"f14":(.*?),')
    stock_codes = p.findall(html)
    for s in range(len(stock_codes)):
        stock_codes[s] = [eval(i) for i in stock_codes[s]]
    stock_codes_df = pd.DataFrame(stock_codes)
    stock_codes_df.columns = ['代码', '名称']
    logger.info(f'There are {len(stock_codes_df)} A shares in total')
    logger.info(f'get stock codes done!')
    return stock_codes_df


@do_again_decorator
def get_single_stack_history_data(stock_url, stock_name):
    """
    根据一支股票的url得到股票历史数据
    :param stock_url: 网页url
    :param stock_name: 股票名称
    :param stock_code: 股票代码
    :return: 此股票所有历史的数据,只包括'日期', '开盘', '收盘', '最高', '最低', '成交量', '成交额', '振幅', '涨跌幅', '涨跌额','换手率'
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36',
    }

    # 这个url需要抓包实现
    req = request.Request(url=stock_url, headers=headers)
    resp = request.urlopen(req)
    html = resp.read().decode('utf-8')
    p = re.compile(r'"klines":(\[.*?\])')

    all_data = eval(p.findall(html)[0])
    all_data = [all_data[i].split(',') for i in range(len(all_data))]
    df_data = pd.DataFrame(all_data, columns=['日期', '开盘', '收盘', '最高', '最低', '成交量', '成交额', '振幅', '涨跌幅', '涨跌额', '换手率'])
    df_data.loc[:, '开盘':'换手率'] = df_data.loc[:, '开盘':'换手率'].applymap(lambda x: float(x))
    # 去掉最后一天的数据
    df_data = df_data[:-1]
    if len(df_data) == 0:
        logger.info(f"The stock {stock_name} launch today, there aren't history data")
        return None
    logger.info(f'There are {len(df_data)} days in total in stock {stock_name}')
    logger.info(f'the share start on {df_data.loc[0, "日期"]}, the last day is {df_data.loc[len(df_data)-1, "日期"]}')
    return df_data

@do_again_decorator
def get_append_data(url):

    """
    # 根据股票代码获得今天的数据
    :param stock_url: 股票url
    :param stock_name: 股票的名字
    :param stock_code: 股票的代码
    :return: 返回单条数据的dataframe
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36',
    }
    # 这个url需要抓包实现
    # 由url 获得网站 html 文件
    req = request.Request(url, headers=headers)
    resp = request.urlopen(req)
    html = resp.read().decode('utf-8')
    p = re.compile(r'"diff":(\{.*?\}\})')
    append_data = eval(p.findall(html)[0])
    df_data = pd.DataFrame(append_data.values())
    df_data.columns = ['收盘', '涨跌幅', '涨跌额', '成交量', '成交额', '振幅', '换手率', '代码', '最高', '最低', '开盘']
    df_data = df_data[['代码', '开盘', '收盘', '最高', '最低', '成交量', '成交额', '振幅', '涨跌幅', '涨跌额', '换手率']]
    return df_data