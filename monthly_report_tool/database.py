# AccessDBに接続し、データの登録(insert_report)と指定月のデータ取得(get_monthly_report)を行う
import pyodbc
import pandas as pd

# AccessDBのパス
DB_PATH = "monthly_report.accdb"

# DB接続関数
def get_connection():
    conn_str = (
        r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
        fr"DBQ={DB_PATH};"
    )
    return pyodbc.connect(conn_str)

# データ登録関数
def insert_report(date, start_time, end_time, content):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO reports (date, start_time, end_time, content) VALUES (?, ?, ?, ?)"
    cursor.execute(sql, (date, start_time, end_time, content))
    conn.commit()
    conn.close()

# 月報データ取得関数
def get_monthly_report(month):
    conn = get_connection()
    query = "SELECT * FROM reports WHERE FORMAT(date, 'yyyy-mm') = ?"
    df = pd.read_sql(query, conn, params=[month])
    conn.close()
    return df
