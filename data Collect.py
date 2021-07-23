from connect_info import *
import pymysql
import requests
from xml.etree import ElementTree
import json
import time

def reprt_code_chk():
    
    year = str(input("보고서 종류를 입력하세요(0:사업보고서, 1:1분기보고서, 2:반기보고서, 3:3분기보고서):"))
    if year == "0":
        return "11011"
    elif year == "1":
        return "11013"
    elif year == "2":
        return "11012"
    elif year == "3":
        return "11014"
    else:
        print("잘못 입력하셨습니다.")
        return reprt_code_chk()
    
def connect_db():
    
    conn = pymysql.connect(host=connect_info["host"], user=connect_info["user"], password=connect_info["password"], db=connect_info["db"], charset=connect_info["charset"])
    return conn
    
crtfc_key = connect_info["crtfc_key"] #API 인증키(openapi.dart.or.kr에서 발급)
bsns_year = str(input("연도를 입력하세요:")) #사업연도
reprt_code = reprt_code_chk() #보고서 코드

#종목정보 DBMS에서 불러오기
conn = connect_db()
cur = conn.cursor()
cur.execute("select * from stock_info")

corp_code_dic = {}
while True:
    row = cur.fetchone()
    
    if row == None:
        break
    
    stock_code = row[0]
    corp_code_dic[stock_code] = [row[1], row[2], row[3]]
    print(stock_code, ": ", corp_code_dic[stock_code])
    
conn.close()

#HRR 기초 자료 수집
df=[]
for k, v in corp_code_dic.items():
    try:
        stock_code = k
        stock_name = v[0]
        corp_cls = v[1]
        corp_code = v[2]
        print("corp_code:", v[0], "corp_cls",v[1])
        api = "https://opendart.fss.or.kr/api/empSttus.json?crtfc_key={crtfc_key}&corp_code={corp_code}&bsns_year={bsns_year}&reprt_code={reprt_code}"
        url = api.format(crtfc_key=crtfc_key, corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code)
        print(url)
        data = json.loads(requests.get(url).text)
        
        num_total = 0
        for num in data["list"]:
            if "합계" in num.get("fo_bbm") or "총계" in num.get("fo_bbm"):
                continue
            num_total += int(num.get("sm").replace(',', ''))
            print(num_total)
            
        df.append([stock_code, stock_name, corp_cls, num_total])
        print(stock_code, stock_name, corp_cls, num_total)
        
        time.sleep(0.61) #크롤링 속도 제한
        
    except:
        continue
    
#DBMS에 저장
conn = connect_db()
cur = conn.cursor()

for row in df:
    cur.execute("insert into hrr(stock_code, stock_name, corp_cls, bsns_year, total_emp) values('"+str(row[0])+"', '"+str(row[1])+"', '"+(row[2])+"', '"+bsns_year+"', '"+str(row[3])+"')")

conn.commit()
conn.close()
