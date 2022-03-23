from history_ohlc import all_in_range
import pytz
import pandas as pd
from datetime import datetime, timedelta
pd.set_option('display.max_columns', 1000)
import time

timezone = pytz.timezone("Etc/UTC")


while True:
    """
    OHLC data downloader (from MT5).
    Saves data to MySQL DB.
    
    Triggers download every XX minutes (=loop_time)
    (download itself takes around 2-4 minutes)
    then wait up to loop_range time and go again.
    """
    loop_time = timedelta(minutes=6)

    started = datetime.now()
    all_in_range(datetime.now() - loop_time - timedelta(minutes=1), datetime.now() - timedelta(minutes=1))
    ended = datetime.now()
    worked_for = ended - started
    print('worked for: ', worked_for)

    # have_to_wait = loop_time + timedelta(minutes=1) - worked_for
    have_to_wait = loop_time - worked_for
    print('have_to_wait: ', have_to_wait)
    time.sleep(have_to_wait.total_seconds())





######     CHOOSE RANGE BY DATEs
# utc_date_from = datetime(2022, 3, 14, 1, 40, 0, tzinfo=timezone)
# utc_date_to = datetime(2022, 3, 8, tzinfo=timezone)