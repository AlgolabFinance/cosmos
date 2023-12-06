from urllib.parse import urlencode
import requests
import pandas as pd
import os
os.chdir('D:\\Computis\\CLIENT\\NP1')

def main():
    walletList = ['cosmos14tcxx9z6gtdslajzz5qjlxu3vl3v23djyl6tgh','cosmos1ahannsepkam057pkelu69mar3gkjcnvdedkz6k','cosmos1j8t96quyejfwx3rm8emzy23t5j2e4r0dy8uxm0']
    txHistory = cosmostation(walletList)
    txHistory.to_excel('cosmosTxns.xlsx')



def cosmostation(walletList):
    #visit https://v1.cosmos.network/rpc/v0.41.4
    txHistory = pd.DataFrame() 
    for wallet_address in walletList:
        query_params = {
            "limit": 10,
            # "from": '0',
        }

        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
        }
        url = f"https://api-cosmos.cosmostation.io/v1/account/new_txs/{wallet_address}"

        print("Requesting url=%s?%s", url, urlencode(query_params))
        response = requests.get(url, query_params, headers=headers)
        data = response.json()


        # txid = 'B3E831C8AC8075EBD37032A669773F1E036284C273125E93595F2D590355CB7E'
        # url = f"https://api-cosmos.cosmostation.io/v1/tx/hash/{txid}"

        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()

        if "timestamp" not in data["data"]:
            data["data"]["timestamp"] = data["header"]["timestamp"]
        
        if len(data)>0:
            data = pd.DataFrame(data)
            data['wallet'] = wallet_address

    txHistory = pd.concat([txHistory,pd.DataFrame(data)])

    return data
    


def mintscan(walletList):

    # visit https://docs.cosmostation.io/apis, currently in beta, can't get apikey yet
    network = 'cosmos'  
    apikey = ''
    txHistory = pd.DataFrame() 
    for wallet_address in walletList:
        url = f"https://apis.mintscan.io/v1/{network}/accounts/{wallet_address}/transactions"

        headers = {"x-api-key": apikey}
        params = {
            # 'take'              : 20,
            # 'searchAfter'       :'MTY4NjkxMzUyOTAwMHwxMDExMzc3M3w5MjY2RjQ1MENFNDVFM0NDMEIwMEM5OTgzQzZEM0Q1QzZCRkUxOTZENzFGODNFMEZFQThFQ0MwOTk4QUNBMTlD',
            # 'messageTypes[0]'   : '/cosmos.gov.v1beta1.MsgVote',
            # 'messageTypes[1]'   : '/cosmos.bank.v1beta1.MsgSend',
            # 'messageTypes[2]'   : '/cosmos.staking.v1beta1.MsgDelegate',
            # 'fromDateTime'      : 'YYYY-MM-DD OR YYYY-MM-DD HH:mm:ii',
            # 'toDateTime'        : 'YYYY-MM-DD OR YYYY-MM-DD HH:mm:ii',
        }
        response = requests.get(url, params= params, headers = headers)

        if response.status_code == 200:
            data = response.json()

        if len(data)>0:
            data = pd.DataFrame(data)
            data['wallet'] = wallet_address

    txHistory = pd.concat([txHistory,data])
    return txHistory


if __name__ == "__main__":
    main()
