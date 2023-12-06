import os
from datetime import datetime
os.chdir('D:/Computis/CLIENT/NP1') #to replace with local directory
from src.cosmosRPC import RPC

def main():

    walletList = {
        'cosmos14tcxx9z6gtdslajzz5qjlxu3vl3v23djyl6tgh': 'Cosmos 0-0 BOOTDISK',
        'cosmos1ahannsepkam057pkelu69mar3gkjcnvdedkz6k': 'Cosmos 0-1 PERSONAL',
        'cosmos1j8t96quyejfwx3rm8emzy23t5j2e4r0dy8uxm0': 'Cosmos NoL1 PERSONAL',
        }
    reportTime = datetime.now().strftime("%b%dT%H%M")  
    client = 'NP1'
    txHistory = RPC(walletList)
    txHistory.to_excel(f'{client}-CosmosTxns-{reportTime}.xlsx')


if __name__ == "__main__":
    main()
