import requests, json,datetime,schedule,csv,time

url = "https://api.nomics.com/v1/prices?key=a9275858e9280ae020cc52fd9b6fdad1103d651e&format=json"

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

    with open('prices.csv', 'a',newline="") as DateFile:
        writer = csv.writer(DateFile)
        writer.writerow(prices)

schedule.every(2).seconds.do(StoreCurrentPrices)

while True:
    schedule.run_pending()
    time.sleep(1)

