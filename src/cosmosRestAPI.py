from urllib.parse import urlencode
import requests
import pandas as pd


def cosmostation(walletList):
    #visit https://v1.cosmos.network/rpc/v0.41.4

    walletAddresses = list(walletList.keys())

    txHistory = pd.DataFrame() 
    for walletAddress in walletAddresses:
        query_params = {
            "limit": 10,
            # "from": '0',
        }

        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
        }
        url = f"https://api-cosmos.cosmostation.io/v1/account/new_txs/{walletAddress}"

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
            data['wallet'] = walletAddress

    txHistory = pd.concat([txHistory,pd.DataFrame(data)])

    return data
    


def mintscan(walletList):

    # visit https://docs.cosmostation.io/apis, currently in beta, can't get apikey yet

    walletAddresses = list(walletList.keys())

    network = 'cosmos'  
    apikey = ''
    txHistory = pd.DataFrame() 
    for walletAddress in walletAddresses:
        url = f"https://apis.mintscan.io/v1/{network}/accounts/{walletAddress}/transactions"

        headers = {"x-api-key": apikey}
        params = {
            # 'take'              : 20,
            # 'searchAfter'       : 'MTY4NjkxMzUyOTAwMHwxMDExMzc3M3w5MjY2RjQ1MENFNDVFM0NDMEIwMEM5OTgzQzZEM0Q1QzZCRkUxOTZENzFGODNFMEZFQThFQ0MwOTk4QUNBMTlD',
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
            data['wallet'] = walletAddress

    txHistory = pd.concat([txHistory,data])
    return txHistory
