#import pandas as pd
import streamlit as st

st.set_page_config(layout='wide')

st.title("Introduction to the Gaming Industry")

tab1, tab2 = st.tabs(["Introduction", "About this App"])

#need to add images
with tab1:
    intro = 'files/introduction.md'
    intro_text = open(intro,"r").read()
    st.write(intro_text)

with tab2:
    st.write("This app provides us insights into the latest consoles in the market today, namely, PS5, XBox Series X and NS. We also take a closer look at the top rated games, sales and ratings across all platforms.")
    st.write("We will also look into PC gaming as a platform. However, since PC gaming itself is so vast, we will look at it separately")
    st.header("About the Data")
    st.write("For the latest console data we look at Amazon reviews")
    st.write("For the top rated games and sales data we will use vgchartz.com as our source")