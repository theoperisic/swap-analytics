import requests
import json

import sqlite3

import time

# Persisting transaction data
def persist_swap_transactions(con, cur):
    # CREATE TABLE swap_transactions (
    #     id TEXT NOT NULL UNIQUE,
    #     amountUSD REAL,
    #     tx_timestamp TIMESTAMP,
    #     wallet_address TEXT,
    #     token0_abbr TEXT,
    #     token0_name TEXT,
    #     amount0 REAL,
    #     token0_feesUSD REAL,
    #     token1_abbr TEXT,
    #     token1_name TEXT,
    #     amount1 REAL,
    #     token1_feesUSD REAL
    # );

    query = """{
    swaps {
    amount0
    amount1
    amountUSD
    id
    origin
    timestamp
    token1 {
        name
        symbol
        feesUSD
    }
    token0 {
        symbol
        name
        feesUSD
    }
    }
    }"""

    url = 'https://api.thegraph.com/subgraphs/name/nick8319/uniswap-v3-harmony'
    r = requests.post(url, json={'query': query})
    response_json = r.json()['data']['swaps']
    for txn in response_json:
        id = txn['id']
        amountUSD = txn['amountUSD']
        tx_timestamp = txn['timestamp']
        wallet_address = txn['origin']

        token0_abbr = txn['token0']['symbol']
        token0_name = txn['token0']['name']
        amount0 = txn['amount0']
        token0_feesUSD = txn['token0']['feesUSD']

        token1_abbr = txn['token1']['symbol']
        token1_name = txn['token1']['name']
        amount1 = txn['amount1']
        token1_feesUSD = txn['token1']['feesUSD']

        insertQuery = """Insert INTO swap_transactions (id, amountUSD, tx_timestamp, wallet_address, token0_abbr, token0_name, amount0, token0_feesUSD, token1_abbr, token1_name, amount1, token1_feesUSD)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?);"""

        try:
            cur.execute(insertQuery, (id, amountUSD, tx_timestamp, wallet_address, token0_abbr,
                        token0_name, amount0, token0_feesUSD, token1_abbr, token1_name, amount1, token1_feesUSD))
        except:
            pass

if __name__ == "__main__":
    db_name = 'swap_data.db'

    con = sqlite3.connect(db_name)
    cur = con.cursor()

    persist_swap_transactions(con, cur)

    con.commit()
    cur.close()
    con.close()
