import streamlit as st
import os
from datetime import datetime
from src.cosmosRPC import RPC
from tools.uploadFile import uploadFile
from tools.saveFile import download

st.set_page_config(
    page_title = "Cosmos app",
    page_icon = "🚀"
)

st.session_state["hide_menu"] = """
<style>
#MainMenu {visibility: visible;}

footer {visibility: visible;}
footer:before{
    content: "Copyright ©2022 by Computis. All Rights Reserved. Permission to use, copy, modify, and distribute this software and its documentation is granted for internal uses only. Contact Computis representative at contact@computis.io, http://computis.io for commercial licensing opportunities.";
    display: block;
    position: relative;
    color: tomato;
    padding: 0px;
    bottom: 5px;
}
</style>
"""
st.markdown(st.session_state["hide_menu"], unsafe_allow_html=True)

def main():
    
    # to choose a node provider below
    
    rpcNodes = [
        'https://rpc-cosmoshub.mms.team/',
        'https://cosmos-rpc.polkachu.com/',
        'https://cosmos-rpc.tienthuattoan.ventures',
        'https://rpc-cosmoshub.ecostake.com/',
        'https://rpc.cosmos.directory/cosmoshub/',
        'https://v1.cosmos.network/rpc/',
    ]

    manual = st.checkbox('Input another node', key='manual_checkbox')
    if manual:
        rpcNode = st.text_input('Input a node', key='input_node')
    else:
        rpcNode = st.selectbox('Select a node:',rpcNodes,key='select_node')

    walletList = {
        'cosmos14tcxx9z6gtdslajzz5qjlxu3vl3v23djyl6tgh': 'Cosmos 0-0 BOOTDISK',
        'cosmos1ahannsepkam057pkelu69mar3gkjcnvdedkz6k': 'Cosmos 0-1 PERSONAL',
        'cosmos1j8t96quyejfwx3rm8emzy23t5j2e4r0dy8uxm0': 'Cosmos NoL1 PERSONAL',
        }
    
    with st.sidebar:
        try:
            walletList = uploadFile("Upload a Wallet Directory file:", key = 1000,sourceCol = False,findsheet = 'wallet directory')
        except Exception as e:
            st.error(e)
    reportTime = datetime.now().strftime("%b%dT%H%M")  
    client = 'NP1'
    txHistory = RPC(rpcNode, walletList, host = True)
    filename = f'{client}-CosmosTxns-{reportTime}.xlsx'
    download(txHistory,filename)


if __name__ == "__main__":
    main()

if __name__ == "__main__":
        try:
            main()
        except Exception as e:
            st.exception(e)
