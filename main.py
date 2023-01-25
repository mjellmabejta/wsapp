import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
     

URL = "https://www.goodreads.com/list/show/79160"
page = requests.get(URL)
     

soup = BeautifulSoup(page.content, "html.parser")
     
booktitle = []
for item in soup.find_all('span', itemprop="name", role="heading"):
  booktitle.append(item.get_text())


author = []
for item in soup.find_all('a', {'class' : 'authorName'}):
  author.append(item.get_text())


avg_rating = []
for item in soup.find_all('span', {'class' : 'minirating'}):
  avg_rating.append(item.get_text())


ratings = []
for i in range (len(avg_rating)):
  num = re.sub('\D', '', avg_rating[i])[:3]
  rating = num[0] + '.' + num[1:] 
  ratings.append(rating)


data = pd.DataFrame()

data['Book Title'] = booktitle
data['Author'] = author
data['Average Rating'] = ratings


#streamlit

import streamlit as st

st.title("Most Popular Mysteries on Goodreads")
st.caption("data collected by a web scraping script written in Python")

title = st.text_input('check if author is on the list:')

if title.isspace() == False and title != '':
    st.caption('Results:')
    for i in range(len(author)):
        if title in author[i].lower():          
            st.write(author[i],' ,', booktitle[i])
        if i == (len(author)-1):
            st.caption('_end of results_')


st.dataframe(data)







@st.cache
def convert_df(data):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return data.to_csv().encode('utf-8')

csv = convert_df(data)

st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='Most_Popular_Mysteries_on_Goodreads.csv',
    mime='text/csv',
)
st.write("wtf")