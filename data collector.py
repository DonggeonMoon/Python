from connect_info import *
import json
import pymysql
import requests
import time
import traceback


def reprt_code_chk():
    quarter = str(input("보고서 종류를 입력하세요(0:사업보고서, 1:1분기보고서, 2:반기보고서, 3:3분기보고서):"))
    if quarter == '0':
        return '11011'
    elif quarter == '1':
        return '11013'
    elif quarter == '2':
        return '11012'
    elif quarter == '3':
        return '11014'
    else:
        print("잘못 입력하셨습니다.")
        return reprt_code_chk()

    
def connect_db():
    conn = pymysql.connect(host=connect_info['host'], user=connect_info['user'], password=connect_info['password'],
                           db=connect_info['db'], charset=connect_info['charset'])
    return conn


crtfc_key = connect_info['crtfc_key']  # API 인증키(openapi.dart.or.kr에서 발급)
bsns_year = str(input("연도를 입력하세요:"))  # 사업연도
reprt_code = reprt_code_chk()  # 보고서 코드

# DBMS에서 종목정보 불러오기
conn = connect_db()
cur = conn.cursor()
cur.execute("select stock_code, stock_name, corp_cls, corp_code from stock_info")

stock_info = cur.fetchall()
print('rows of data: ' + str(len(stock_info)))
conn.close()

# 기초 자료 수집
df = []
for i, j, k, l in stock_info:
    try:
        stock_code = i
        stock_name = j
        corp_cls = k
        corp_code = l
        print('stock_name:', j, 'corp_cls:', k)
        api = 'https://opendart.fss.or.kr/api/empSttus.json?crtfc_key={crtfc_key}' \
              '&corp_code={corp_code}' \
              '&bsns_year={bsns_year}' \
              '&reprt_code={reprt_code}'
        url = api.format(crtfc_key=crtfc_key, corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code)
        print(url)
        data = json.loads(requests.get(url).text)
        
        num_total = 0
        for num in data['list']:
            if '합계' in num.get('fo_bbm') or '총계' in num.get('fo_bbm'):
                continue
            num = num.get('sm')
            num = int(num.replace(',', '')) if num != '-' else 0
            num_total += num
            print(num_total)
            
        df.append([stock_code, stock_name, corp_cls, num_total])
        print(stock_code, stock_name, corp_cls, num_total, '\n')
        
        time.sleep(0.61)  # 크롤링 속도 제한
        
    except:
        traceback.print_stack()
        traceback.print_exc()
        continue
    
# DBMS에 저장
conn = connect_db()
cur = conn.cursor()

for row in df:
    try:
        cur.execute(
            "insert into hrr(stock_code, stock_name, corp_cls, bsns_year, reprt_code, total_emp) values('" +
            str(row[0]) + "', '" + str(row[1]) + "', '" + str(row[2]) + "', '" + bsns_year + "', '" +
            reprt_code + "', '" + str(row[3]) + "')")
        
    except:
        traceback.print_stack()
        traceback.print_exc()
        continue
    
conn.commit()
conn.close()
