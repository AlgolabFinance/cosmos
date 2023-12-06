import streamlit as st
import os
from pathlib import Path
import base64
from io import BytesIO
# from pyxlsb import open_workbook as open_xlsb
import pandas as pd
from datetime import datetime
import xlsxwriter
import os

def download_csv(data):
  # IMPORTANT: Cache the conversion to prevent computation on every rerun
  return data.to_csv(index = False).encode('utf-8')

def download_excel(data):
  # IMPORTANT: Cache the conversion to prevent computation on every rerun
  output = BytesIO()
  with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
    data.to_excel(writer,index = False)
  return output.getvalue()

def queueUp(filename, clientCode, clientID, data):

  reportTime = datetime.now().strftime("%b%dT%H%M")  
  filename = f'{clientCode}-{filename}-{clientID}-{reportTime}'
  st.session_state["download"].append(filename)
  st.session_state[filename] = data.astype(str)


def download(data,filename):
  try: 
    st.download_button(
            label=f"Download '{filename}'",
            data = download_excel(data),
            file_name=f'{filename}',
            mime="application/vnd.ms-excel"
            )
  except Exception as e: 
      st.error(e)
      st.stop()
