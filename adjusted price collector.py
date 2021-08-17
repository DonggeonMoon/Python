from connect_info import *
from functools import partial
from multiprocessing import Pool
import os
import pymysql
import re
import time
import traceback
import urllib.request


def connect_db():
    conn = pymysql.connect(host=connect_info['host'], user=connect_info['user'], password=connect_info['password'],
                           db=connect_info['db'], charset=connect_info['charset'])
    return conn


def adjustedStockPrice(number, date):
    # DBMS에서 종목정보 불러오기
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("select stock_code, stock_name, corp_cls from stock_info")
    df = []
    
    while True:
        row = cur.fetchone()
        if row is None:
            break
        df.append([row[0], row[1], row[2]])
        
    conn.close()
    
    total_number = len(df)
    start_number = int(total_number / 4 * (number - 1))
    end_number = int(total_number / 4 * number)
    print('Process {} ({} ~ {}) started!'.format(number, start_number, end_number))
    df = df[start_number:end_number]
    
    # 네이버 금융 주가 차트에서 수정주가 데이터 수집
    for i in range(len(df)):
        try:
            data = str(urllib.request.urlopen('https://fchart.stock.naver.com/sise.nhn?symbol=' + df[i][0]
                                              + '&timeframe=day&count=3000&requestType=0').read())
            price = re.search(r'' + date + '\|[0-9]+\|[0-9]+\|[0-9]+\|[0-9]+', data).group()
            price2 = re.search(r'\|[0-9]+$', price).group().strip('|')
            df[i].append(price2)
            print(df[i])
            
        except:
            print('error')
            continue
        
    print('Process {} ({} ~ {}) completed!'.format(number, start_number, end_number))
    return df


if __name__ == '__main__':
    start_time = time.time()
    date = input("수집할 수정주가 일자를 입력하세요(ex: 20210102):")
    pool = Pool(int(os.environ['NUMBER_OF_PROCESSORS']))
    func = partial(adjustedStockPrice, date=date)
    result = pool.map(func, list(range(1, int(os.environ['NUMBER_OF_PROCESSORS']) + 1)))

    # DBMS에 저장
    conn = connect_db()
    cur = conn.cursor()
    try:
        for i in result:
            for j in i:
                print(j)
                if len(j) == 3:
                    continue
                sql = "insert into stock_price values('{}', '{}', '{}', '{}', {})".format(j[0], j[1], j[2], date, j[3])
                cur.execute(sql)
                
    except:
        traceback.print_stack()
        traceback.print_exc()
        
    conn.commit()
    conn.close()

