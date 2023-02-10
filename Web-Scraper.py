import streamlit as st
import pandas as pd
from pandas import json_normalize 
import json
import io
import requests
import base64
from io import BytesIO
import io

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter') # pylint: disable=abstract-class-instantiated
    df.to_excel(writer, sheet_name='Sheet1',index=False)
    writer.save()
    processed_data = output.getvalue()
    return processed_data

def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    val = to_excel(df)
    b64 = base64.b64encode(val)
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download='+keyword.replace(" ", "")+".xlsx"'>Download Excel file</a>' # decode b'abc' => abc
 
st.title(":male-detective: Pete's Google Scraper")

keyword = st.text_input("Enter keyword here: ")

headers = { 
  "apikey": "05884cd0-a918-11ed-ae21-659aaec240ea"}
 
params = (
   ("q",keyword),
   ("search_engine","google.co.za"),
   ("tbm","shop"),
   ("gl","ZA"),
   ("hl","en"),
);

url = 'https://app.zenserp.com/api/v2/search'
 


displayResult = st.button("Display Result")
if displayResult:
    response = requests.get(url, headers=headers, params=params);
    json = response.json()
    df = pd.DataFrame(json["shopping_results"])
    df_price_num = df["price_parsed"].apply(pd.Series)
    df_final = pd.merge(df, df_price_num, left_index=True,right_index=True)
    df_final = df_final[['source','currency','value','price','stars','link']]
    df_final
    # Output to .xlsx
    st.write('Download:')
    st.markdown(get_table_download_link(df_final), unsafe_allow_html=True)

