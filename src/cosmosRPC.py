
import requests
import pandas as pd
import streamlit as st
'''
todo: add other event types
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

def RPC(rpcNode,walletList,host = False):
    walletAddresses = list(walletList.keys())
    
    endpoint = 'tx_search'
    url = rpcNode + endpoint
    page= 1
    per_page = 100
    offset = 100
    query_params = {"page": page, 
                "per_page": per_page,
                # "pagination.offset": offset,
                # 'message.action':'getreward',
                # 'message.sender':'cosmos16xyempempp92x9hyzz9wrgf94r6j9h5f06pxxv'
                }
    
    txHistory = pd.DataFrame()
    for walletAddress in walletAddresses:
        walletNickname = walletList.get(walletAddress,'')
        #query different event types
        queries = [
            "\"message.sender='{}'\"".format(walletAddress),
            "\"message.action='getreward' AND message.sender='{}'\"".format(walletAddress),
            "\"message.action='redelegate' AND message.sender='{}'\"".format(walletAddress),
            "\"message.action='IBCSend' AND message.sender='{}'\"".format(walletAddress),
            "\"message.action='IBCReceive' AND message.sender='{}'\"".format(walletAddress),
            "\"message.action='getreward' AND transfer.recipient='{}'\"".format(walletAddress),
            "\"message.action='redelegate' AND transfer.recipient='{}'\"".format(walletAddress),
            "\"message.action='IBCSend' AND transfer.recipient='{}'\"".format(walletAddress),
            "\"message.action='IBCReceive' AND transfer.recipient='{}'\"".format(walletAddress),
            "\"tx.maxheight=18000000 AND message.sender='{}'\"".format(walletAddress),
            "\"transfer.recipient='{}'\"".format(walletAddress),
            "\"message.signer='{}'\"".format(walletAddress),
            ]
        for query in queries:
            txHistory = queryRPC(txHistory,url, query_params,query,walletAddress,walletNickname,host)
    if host == True:
        st.write(f'Total of {len(txHistory)} txns')
    else:
        print(f'Total of {len(txHistory)} txns')

    return txHistory

def queryRPC(txHistory,url, params,query,walletAddress,walletNickname, host):
    params["query"] = query
    response = requests.get(url, params = params)
    if response.status_code == 200:
        data = response.json()
        total_count_txs = int(data["result"]["total_count"])
        try:
            data = pd.DataFrame(data['result']['txs'])
            data['query'] = query
            data['wallet'] = walletAddress
            txHistory = pd.concat([txHistory,data],ignore_index=True)
            print(f'Fetching {len(data)} / {total_count_txs} txns for {walletNickname}')
            if host == True:
                st.write(f'Fetching {len(data)} / {total_count_txs} txns for {walletNickname}')

        except Exception as e:
            print(e)
            if host == True:
                st.write(e)

    return txHistory
