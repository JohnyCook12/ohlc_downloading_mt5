import pandas as pd
from sqlalchemy import create_engine
from db_credentials import db_creds

"""
OIDC_CONFIG can be found inside gitignore db_credentials.py. Contact Project Maintainer for more details

example of db_connection_string

from urllib.parse import quote_plus as urlquote
db_connection_str = 'mysql+pymysql://{}:{}@{}/{}'.format(user, urlquote(password),host, db_name)
"""


def exec_query(query, database, **kwargs):
    if kwargs:
        engine = create_engine(db_creds[database])
        df = pd.read_sql(query, con=engine, params=kwargs['params'])
        return df
    else:
        engine = create_engine(db_creds[database])
        df = pd.read_sql(query, con=engine)
        return df
