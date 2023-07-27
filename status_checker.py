import requests
import time
import sqlite3
import socket
import os

# CREATE TABLE swap_status (
#     check_datetime DATETIME,
#     url TEXT,
#     response_code INTEGER,
#     response_time REAL,
#     req_log TEXT,
#     socket_ip TEXT,
#     socket_log TEXT,
#     ping_resp INT
# );

# 99999 is error

def check_site_status(con, cur, url, max_retries=3):
    retry = 0

    try:
        socket_ip = socket.gethostbyname("url")
        socket_log = ''
    except socket.gaierror as e:
        socket_ip = ''
        socket_log = str(e)

    try:
        ping_resp = int(os.system("ping -c 1 " + url))
    except Exception as e:
        ping_resp = str(e)

    while retry <= max_retries:
        if '://' in url:
            try:
                response = requests.get(url)
                response_code = response.status_code
                response_time = response.elapsed.total_seconds()
                
                insertQuery = """Insert INTO swap_status (check_datetime, url, response_code, response_time, socket_ip, socket_log, ping_resp)
                VALUES (?,?,?,?,?,?,?);"""

                cur.execute(insertQuery, (time.time(), url, response_code, response_time, socket_ip, socket_log, ping_resp))

                break
            except requests.exceptions.RequestException as e:
                retry += 1
                if retry <= max_retries:
                    insertQuery = """Insert INTO swap_status (check_datetime, url, response_code, req_log, socket_ip, socket_log, ping_resp)
                    VALUES (?,?,?,?,?,?,?);"""
                    cur.execute(insertQuery, (time.time(), url, 99999, str(e), socket_ip, socket_log, ping_resp))
                    time.sleep(2**retry)
                else:
                    break
        else:
            insertQuery = """Insert INTO swap_status (check_datetime, url, socket_ip, socket_log, ping_resp)
                    VALUES (?,?,?,?,?);"""
            cur.execute(insertQuery, (time.time(), url, socket_ip, socket_log, ping_resp))
            break
            

if __name__ == "__main__":
    site_url = ["https://swap.country", "swap.country"]

    db_name = 'swap_status.db'

    con = sqlite3.connect(db_name)
    cur = con.cursor()

    for url in site_url:
        check_site_status(con, cur, url)

    con.commit()
    cur.close()
    con.close()