from initialize import *
import os, re, time
import urllib.request
from multiprocessing import Pool
from functools import partial

def adjustedStockPrice(number, date):
    df = initialize("종목정보")
    total_number = len(df)
    start_number = int(total_number / 4 * (number - 1))
    end_number = int(total_number / 4 * number)
    print("Process(" + str(start_number) + " ~ " + str(end_number) + ") started!")
    df = df[start_number:end_number]
    
    #네이버 금융 주가 차트에서 수정주가 데이터 수집
    for i in range(0, len(df)):
        try:
            data = str(urllib.request.urlopen("https://fchart.stock.naver.com/sise.nhn?symbol=" + df[i][0] + "&timeframe=day&count=3000&requestType=0").read())
            price = re.search(r'' + date + '\|[0-9]+\|[0-9]+\|[0-9]+\|[0-9]+', data).group()
            price2 = re.search(r'\|[0-9]+$', price).group().strip('|')
            df[i] = df[i][:3]
            df[i].append(price2)
            print(df[i])
            
        except:
            df[i] = df[i][:3]
            print("error")
            continue
            
    print("Process %d (%d ~ %d) completed!" % (number, start_number, end_number))
    return df

if __name__=='__main__':
    start_time = time.time()
    date = input("수집할 수정주가 일자를 입력하세요. (ex: 20200102):")
    pool = Pool(int(os.environ['NUMBER_OF_PROCESSORS']))
    func = partial(adjustedStockPrice, date=date)
    result = pool.map(func, list(range(1, int(os.environ['NUMBER_OF_PROCESSORS']) + 1)))
    
    #수정주가YYYYMMDD.txt 파일에 저장
    f = open("수정주가" + str(date) + ".txt",'w')
    length = len(result)
    for i in range(0, length):
        length2 = len(result[i])
        for j in range(0,length2):
            length3 = len(result[i][j])
            for k in range(0, length3):
                f.write(result[i][j][k])
                f.write('\t')
            f.write("\n")
    f.close()
    print("--- %s초 ---" % (time.time() - start_time))
    #os.system("shutdown -s -t 60")
