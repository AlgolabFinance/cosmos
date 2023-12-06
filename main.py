import os
from datetime import datetime
os.chdir('D:/Computis/CLIENT/NP1/blockchain data/Cosmos') #to replace with local directory
from src.cosmosRPC import RPC

def main():
    
    # to choose a node provider below
    
    # rpcNode = 'https://cosmos-rpc.polkachu.com/'
    # rpcNode = 'https://cosmos-rpc.tienthuattoan.ventures'
    rpcNode = 'https://rpc-cosmoshub.mms.team/'
    # rpcNode = 'https://rpc-cosmoshub.ecostake.com/'
    # rpcNode = 'https://rpc.cosmos.directory/cosmoshub/'
    # rpcNode = 'https://v1.cosmos.network/rpc/'

    walletList = {
        'cosmos14tcxx9z6gtdslajzz5qjlxu3vl3v23djyl6tgh': 'Cosmos 0-0 BOOTDISK',
        'cosmos1ahannsepkam057pkelu69mar3gkjcnvdedkz6k': 'Cosmos 0-1 PERSONAL',
        'cosmos1j8t96quyejfwx3rm8emzy23t5j2e4r0dy8uxm0': 'Cosmos NoL1 PERSONAL',
        }
    reportTime = datetime.now().strftime("%b%dT%H%M")  
    client = 'NP1'
    txHistory = RPC(rpcNode,walletList)
    filename = f'{client}-CosmosTxns-{reportTime}.xlsx'
    txHistory.to_excel(filename)


if __name__ == "__main__":
    main()
