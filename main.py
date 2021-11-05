import requests, json,datetime,csv,time,schedule
from ftplib import FTP

from os import environ
from flask import Flask



url = "https://api.nomics.com/v1/prices?key=a9275858e9280ae020cc52fd9b6fdad1103d651e&format=json"
csv_url = "https://mohamad-awad.info/scripts/crypto/prices.csv"

def StoreCurrentPrices():
    
    def GetPrice(Currencies):
        r = requests.get(url)
        data=json.loads(r.text)
        price=[]
        #print(data)
        for currency in Currencies:
            for i in data:
                if(i["currency"]==currency):
                    price.append(i["price"])
        return price
    
    DateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    prices=GetPrice(["BTC","SHIB","XRP","AUDIO","SOL","DOGE","BNB","LUNA","DENT","WIN","ADA","ETH"])
    prices.insert(0, DateTime)
    print(prices)
    
    req = requests.get(csv_url)
    url_content = req.content
    csv_file = open('prices.csv', 'wb')
    csv_file.write(url_content)
    csv_file.close()

    
    with open('prices.csv', 'a',newline="") as DateFile:
        writer = csv.writer(DateFile)
        writer.writerow(prices)
    
    # upload data to my host
    FTP.maxline = 163840
    ftp = FTP('ftpupload.net')
    ftp.login(user="epiz_26155908",passwd="CziCHHeOvM3jNLJ")
    ftp.cwd("/mohamad-awad.info/htdocs/scripts/crypto/")
    filename = 'prices.csv'
    ftp.storlines('STOR ' + filename, open(filename, 'rb'))
    ftp.quit()
    
    port = int(os.environ.get('PORT', 5000))
    app = Flask(__name__)
    app.run(environ.get(port))


    
    # upload the file to a we

schedule.every(20).seconds.do(StoreCurrentPrices)

while True:
    schedule.run_pending()
    time.sleep(1)
