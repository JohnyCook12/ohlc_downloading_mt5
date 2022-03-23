import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime, timedelta
pd.set_option('display.max_columns', 1000)
import numpy as np
import pytz
from sqlalchemy import create_engine
from db_con import exec_query
from db_credentials import db_creds


# open platform + login
mt5.initialize()
login = 3333
password = 'Abc12345'
server = 'FTMO-Server'


symbols=mt5.symbols_get()


symbols_names = [symbol.name for symbol in symbols]
timezone = pytz.timezone("Etc/UTC")

def get_ohlc(symbol, date_from, date_to, timeframe):
    """
    get ohlc data from mt5 then insert to DB ohlc_history
    per every symbol create table symbolname_timeframe (eg. EURUSD_D1)
    :param symbol: EURUSD
    :param date_from: datetime(2020, 8, 1, tzinfo=timezone)
    :param date_to:
    :param timeframe: string: D1, W1, M1 .... then call mt5.TIMEFRAME_D1
    :return:
    """

    db_connection_str = db_creds['computing_test']
    table_name = symbol + '_' + timeframe


    mt5.login(login, password, server)
    timeframe_dict = {
        'M1': mt5.TIMEFRAME_M1,
        'M5': mt5.TIMEFRAME_M5,
        'M15': mt5.TIMEFRAME_M15,
        'M30': mt5.TIMEFRAME_M30,
        'H1': mt5.TIMEFRAME_H1,
        'H4': mt5.TIMEFRAME_H4,
        'D1': mt5.TIMEFRAME_D1,
        'W1': mt5.TIMEFRAME_W1,
        'MN1': mt5.TIMEFRAME_MN1}

    df = pd.DataFrame(mt5.copy_rates_range(symbol, timeframe_dict[timeframe], date_from, date_to))
    if df.empty:
        return "No data"
    else:
        df['time'] = df['time'].apply(lambda x: datetime.fromtimestamp(x))
        df['symbol'] = symbol
        df.drop(columns=['tick_volume', 'real_volume'], inplace=True)
        df = df[['symbol', 'time', 'open', 'high', 'low', 'close', 'spread']]

        engine = create_engine(db_connection_str)
        df.to_sql(table_name,con=engine, if_exists='append')
        # df.to_sql(table_name,con=engine, if_exists='replace')     # when need to replace data


## main ##
def all_in_range(utc_from_d, utc_to_d):
    """ download OHLC of all symbols in selected datetime RANGE and write it to DB """
    tfs= ['M1','M5','M15','M30','H1','H4','D1','W1', 'MN1']

    print(len(symbols))
    print(symbols_names)
    for s in symbols:
        print(s.name, '  ', utc_from_d, '  ->  ', utc_to_d)
        for tf in tfs:
            print(tf)
            get_ohlc(s.name, utc_from_d, utc_to_d, tf)
    print('===========   finished   ==========')




    ######     CHOOSE RANGE BY DATEs (for PREFIL data)      ######
    """
    By this you can prefil the DB by data from selected range.
    Dont forget to choose 'replace' instead of 'append' in to_sql method.
    """

    # utc_date_from = datetime(2022, 3, 14, 1, 40, 0, tzinfo=timezone)
    # utc_date_to = datetime(2022, 3, 8, tzinfo=timezone)
    # all_in_range(utc_date_from, utc_date_to)