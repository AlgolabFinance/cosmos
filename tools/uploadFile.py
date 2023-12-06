import streamlit as st 
import pandas as pd


def uploadFile(message,key,sourceCol,findsheet = None):
    file = st.file_uploader(message, type=['csv','xlsx'],accept_multiple_files=False, key = key+1)
    st.set_option("deprecation.showfileUploaderEncoding", False)

    if file is not None:
        skiprow = st.number_input('Skip rows:', 0, key = key+400)
        try:
            data = pd.read_csv(file, index_col=False,dtype=str, skiprows=int(skiprow))
        except Exception as e:
            if findsheet == None:
                selected_sheet = st.selectbox('Select sheet:',pd.ExcelFile(file).sheet_names, key = key+100)
            else:
                allsheet = pd.ExcelFile(file).sheet_names
                for index, item in enumerate(pd.ExcelFile(file).sheet_names):
                    if findsheet in item.lower():
                        allsheet.insert(0, allsheet.pop(index))
                selected_sheet = st.selectbox('Select sheet:',allsheet, key = key+100)

            data = pd.read_excel(file, dtype=str, sheet_name= selected_sheet,skiprows=int(skiprow), index_col=False)
        
        data['Source'] = file.name
        if sourceCol == True:
            source = data.pop('Source')
            data.insert(0,'Source',source)
    else:
        data = pd.DataFrame()
    return data