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
    #upload data to guthub
    token = "02bf29c25181460ec263b9"+"fcde985fecb5cc264f"
    repo = 'MohNabilAwad/GetCryptoPrices'
    path = 'prices.csv'
    data = open("prices.csv", "r").read()
    
    # to get the key for github
    response = requests.get('https://raw.githubusercontent.com/MohNabilAwad/GetCryptoPrices/main/prices.csv')
    GitHubText = json.loads(response.text)
    r = requests.put(
        f'https://api.github.com/repos/{repo}/contents/{path}',
        headers = {
            'Authorization': f'Token {token}'
        },
        json = {
            "message": "add new file",
            "content": base64.b64encode(data.encode()).decode(),
            "branch": "master",
            "sha":GitHubText["sha"]
        }
    )

schedule.every(3).seconds.do(StoreCurrentPrices)

while True:
    schedule.run_pending()
    time.sleep(1)

