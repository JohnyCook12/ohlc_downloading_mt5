from urllib.parse import quote_plus as urlquote

db_creds = {'db1' : 'mysql+pymysql://{}:{}@{}/{}'.format('db_login', urlquote('some_password'),'db1.ftmo.com', 'database_name'),
'computing_test' : 'mysql+pymysql://{}:{}@{}/{}'.format('j.kuchar@ftmo.com', urlquote('Hs5.Mashj0ms,'),'35.189.96.188', 'ohlc_history')}