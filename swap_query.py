import requests
import json

import sqlite3

import time

# CREATE TABLE swap_transactions (
#     id TEXT,
#     amountUSD REAL,
#     timestamp TIMESTAMP,
#     wallet_address TEXT,
#     token0_abbr TEXT,
#     token0_name TEXT,
#     amount0 REAL,
#     token0_feesUSD REAL,
#     token1_abbr TEXT,
#     token1_name TEXT
#     amount1 REAL,
#     token1_feesUSD REAL,
#     UNIQUE(id)
# );

now = time.time()

con = sqlite3.connect("test.db")
cur = con.cursor()

query = """{
  factories(first: 5) {
    totalVolumeUSD
  }
}"""

url = 'https://api.thegraph.com/subgraphs/name/nick8319/uniswap-v3-harmony'
r = requests.post(url, json={'query': query})
response = r.text 
response = response[response.find('VolumeUSD":"')+12:-6]
response = int(response.split('.')[0])

insertQuery = """Insert INTO tvltest
    VALUES (?,?);"""

cur.execute(insertQuery, (response, now))
con.commit()
cur.close()
con.close()

# create table tvltest (
#    ...> TVLUSD INT,
#    ...> datetime TIMESTAMP);