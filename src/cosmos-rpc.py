
from urllib.parse import urlencode
import requests
import os
os.chdir('D:\\Computis\\CLIENT\\NP1')
import pandas as pd

def main():

    walletList = ['cosmos14tcxx9z6gtdslajzz5qjlxu3vl3v23djyl6tgh','cosmos1ahannsepkam057pkelu69mar3gkjcnvdedkz6k','cosmos1j8t96quyejfwx3rm8emzy23t5j2e4r0dy8uxm0']

    txHistory = queryRPC(walletList)
    txHistory.to_excel('cosmosTxns.xlsx')


def RPC(walletList):
    # to choose a node provider below
    base_url = 'https://cosmos-rpc.polkachu.com/'
    # base_url = 'https://cosmos-rpc.tienthuattoan.ventures'
    # base_url = 'https://rpc-cosmoshub.mms.team/'
    # base_url = 'https://rpc-cosmoshub.ecostake.com/'
    # base_url = 'https://rpc.cosmos.directory/cosmoshub/'
    # base_url = 'https://v1.cosmos.network/rpc/'
    
    endpoint = 'tx_search'
    url = base_url + endpoint
    page= 1
    per_page = 100
    offset = 30
    query_params = {"page": page, 
                "per_page": per_page,
                # "pagination.offset": offset,
                # 'message.action':'getreward',
                # 'message.sender':'cosmos16xyempempp92x9hyzz9wrgf94r6j9h5f06pxxv'
                }
    
    ledger = pd.DataFrame()
    for wallet_address in walletList:
        
        #query different event types
        queries = [
            "\"message.sender='{}'\"".format(wallet_address),
            "\"message.action='getreward' AND message.sender='{}'\"".format(wallet_address),
            "\"tx.maxheight=18000000 AND message.sender='{}'\"".format(wallet_address),
            "\"transfer.recipient='{}'\"".format(wallet_address),
            "\"message.signer='{}'\"".format(wallet_address),
            ]
        for query in queries:
            ledger = queryRPC(ledger,url, query_params,query,wallet_address)

    ledger.to_excel('cosmos2.xlsx')

def queryRPC(ledger,url, params,query,wallet_address):
    params["query"] = query
    response = requests.get(url, params = params)
    if response.status_code == 200:
        data = response.json()
        total_count_txs = int(data["result"]["total_count"])
        print(total_count_txs)
        try:
            data = pd.DataFrame(data['result']['txs'])
            data['query'] = query
            data['wallet'] = wallet_address
            ledger = pd.concat([ledger,data],ignore_index=True)
        except Exception as e:
            print(e)
'''
to add other event types
    Send From - Send
    Send To  - Receive
    Multi Send From
    Multi Send To
    Redelegate - Redelegate
    Delegate
    Undelegate
    Ibc Send - IBCSend
    Ibc Receive
    GetReward
    Get Commission

'''

if __name__ == "__main__":
    main()
