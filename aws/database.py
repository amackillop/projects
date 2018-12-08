# -*- coding: utf-8 -*-
"""
Created on Sun Nov 11 14:26:26 2018

@author: Austin
"""

import sqlalchemy as sa
import getpass
import creds
#import logging
#
#logging.basicConfig()
#logger = logging.getLogger('sqlalchemy.engine')
#log.setLevel(logging.DEBUG)
#conn = psycopg2.connect(**creds.CREDS)
#curs = conn.cursor()

class Database():
    
    def __init__(self, rdbms, host, port, user, password):
        self.conn_vars = {arg: value for arg, value in locals().items()}
        self.conn_vars.pop('self')
        self.conn_str = '{rdbms}://{user}:{password}@{host}:{port}/{database}'
        self.engine = None
        self.meta = None
        self._tables = {}
        pass
    
    @property
    def tables(self):
        if self.engine:
            return self.engine.table_names()
        raise AttributeError('Connect to a database first to get the tables.')
    
    @property
    def databases(self):
        if self.engine:
            insp = sa.inspect(self.engine)
            return insp.get_schema_names()
    
    def init_tables(self):
        for name in self.tables:
            table = sa.Table(name, self.meta, 
                          autoload=True, autoload_with=self.engine)
            self._tables.update({name, table})
            
    def connect(self, database):
        self.conn_vars.update({'database': database})
        self.conn_str = self.conn_str.format_map(self.conn_vars)
        self.engine = sa.create_engine(self.conn_str, client_encoding='utf8', echo=True)
        self.meta = sa.MetaData(bind=self.engine, reflect=True)
        
    def create_table(self, name, column_map, pkey=None):
        table_args = [name, self.meta]
        for col, dtype in column_map.items():
            if pkey and col == pkey:
                table_args.append(sa.Column(col, dtype, primary_key=True))
            else:
                table_args.append(sa.Column(col, dtype))
            
        table = sa.Table(*table_args)
        self._tables.update({name: table})
        self.meta.create_all(self.engine)
    
    def drop_table(self, name):
        if name not in self.tables:
            tables = ', '.join(self.tables)
            msg = 'Table {} not found. Current tables are: {}.'
            print(msg.format(name, tables))
        self._tables[name].drop()
        

if __name__ == '__main__':
    info = creds.CREDS
    rds = Database(**info)
#    rds.connect('crypto')
    