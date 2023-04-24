import pandas as pd
import streamlit as st
import re
import string
from textblob import TextBlob
#from plotly.offline import iplot
import altair as alt
from wordcloud import WordCloud, STOPWORDS
from collections import defaultdict
#import plotly
import matplotlib.pyplot as plt
#from matplotlib import rcParams
#import seaborn as sns
#from plotly import tools

st.set_page_config(layout='wide')
st.set_option('deprecation.showPyplotGlobalUse', False)

reviews = {" ":" ","Playstation5":"files/PS5_Reviews_upd.csv","Xbox SeriesX":"files/SERIESX_Reviews_upd.csv","Nintendo Switch":"files/NS_Reviews_upd.csv"}
console = st.sidebar.selectbox("Choose a console",reviews.keys())
n_gram = {" ":" ","Unigram":1,"Bigram":2,"Trigram":3}


def create_wordcloud(review):
    value=review["Cleaned Review"]
    wordcloud = WordCloud(
            width=3000,
            height=2000,
            background_color='black',
            stopwords=STOPWORDS
    ).generate(str(value))

    fig=plt.figure(
            figsize=(2,4),
            facecolor='k',
            edgecolor='k'
    )
    fig=plt.imshow(wordcloud)
    fig=plt.axis('off')
    fig=plt.tight_layout(pad=0)
    fig=plt.show()
    return fig 

def generate_ngrams(words, n_gram=1):
    token = [token for token in words.lower().split(" ") if token != "" if token not in STOPWORDS]
    ngrams = zip(*[token[i:] for i in range(n_gram)])
    return[" ".join(ngram) for ngram in ngrams]

def horizontal_bar_chart(df,color):
    trace = alt.Chart(df).mark_bar(color='orange').encode(
        y=df["word"],
        x=df["wordcount"]
    )
    return trace

def create_bar_chart(review, bar_color):
    freq_dict = defaultdict(int)
    for sent in review["Cleaned Review"]:
        for word in generate_ngrams(sent):
            freq_dict[word] += 1
            fd_sorted = pd.DataFrame(sorted(freq_dict.items(), key=lambda x: x[1])[::-1])
            fd_sorted.columns = ["word", "wordcount"]
            fd_sorted_head = fd_sorted.head(25)
            

    bar_chart = alt.Chart(fd_sorted_head).mark_bar(color=bar_color).encode(
                        x=alt.X("wordcount"),
                        y=alt.Y("word",sort=alt.EncodingSortField(field="word", op='count'))
    )
    return bar_chart 


def create_console_sales_chart(chosen_console):
    sales = pd.read_csv("files/console_sales.csv")
    console_sales = sales[sales["Console"]==chosen_console]
    new_console_sales = pd.melt(console_sales, id_vars =['Console'], value_vars =['North America','Europe','Japan','Rest of the World','Global'])
    new_console_sales = new_console_sales.sort_values(by=['value'],ascending=False)
        
    console_sales_chart = alt.Chart(new_console_sales).mark_bar().encode(
        x=alt.X('variable', sort=alt.EncodingSortField(field="variable", op='count')),
        y=alt.Y('value'),
        color=alt.Color('value', scale=alt.Scale(scheme='redyellowgreen'))
        ).properties(
             width=800,
             height=400
        )
    return console_sales_chart    


tab1, tab2, tab3, tab4 = st.tabs(["History", "Ratings", "Reviews", "Console Sales"])

with tab1:
    if reviews.get(console) == " ":
        st.write("Please make a selection to see further")

    if console == 'Playstation5':
        ps = 'files/playstation.md'
        ps_text = open(ps,"r").read()
        st.markdown(ps_text)
    
    elif console == 'Xbox SeriesX':
        xbox = 'files/xbox.md'
        xbox_text = open(xbox,"r").read()
        st.markdown(xbox_text)
    
    elif console == 'Nintendo Switch':
        ns = 'files/nintendo.md'
        ns_text = open(ns,"r").read()
        st.markdown(ns_text)

with tab2:
    if reviews.get(console) == " ":
       st.write("Please make a selection to see further")

    if reviews.get(console) != " ":
        st.write(reviews.get(console))
        df = pd.read_csv(reviews.get(console))
        df['Review Year'] = df['Review Year'].astype(str) 
        new_df = df.groupby(['Ratings','Review Year'])['Review Year'].count().reset_index(name='counts')

        ratings_line_chart=alt.Chart(new_df).mark_line().encode(
            x='Ratings',
            y='counts',
            color='Review Year'
        ).properties(
        width=800,
        height=400
    )
        st.write(ratings_line_chart)
    
with tab3:
    if reviews.get(console) == " ":
       st.write("Please make a selection to see further")

    if reviews.get(console) != " ":
        df = pd.read_csv(reviews.get(console))
        #st.write(df.isna().sum())
        df.dropna(inplace=True)
        #st.write(df.isna().sum())
        df.reset_index(inplace=True)
        #st.write(df.tail())
        df.drop('index', axis=1, inplace=True)
        #st.write(df.tail())

        def deEmojify(x):
            regress_pattern =re.compile(pattern = "["
                                        u"\U0001F600-\U0001F64F" #emoticons
                                        u"\U0001F300-\U0001F5FF" #symbols and pictographs
                                        u"\U0001F680-\U0001F6FF" #transport and map symbols
                                        u"\U0001F1E0-\U0001F1FF" #flags
                                        "]+", flags = re.UNICODE)
            return regress_pattern.sub(r'', x)
        
        def review_cleaning(text):
            '''Make text lower case, remove text in square brackets, remove links, remove punctuation and remove words containg numbers.'''
            text = str(text).lower()
            text = re.sub('\[.*?\]', '', text)
            text = re.sub('https?://\S+|www\.\S+', '', text)
            text = re.sub('<.*?>+', '', text)
            text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
            text = re.sub('\n', '', text)
            text = re.sub('\w*\d\w*', '', text)
            text = deEmojify(text)
            text = text.strip()
            return text
        
        def f(row):
            '''This function returns sentiment value based on the overall ratings from user'''
            if row['Ratings'] == 3.0:
                val = 'Neutral'
            elif row['Ratings'] == 1.0 or row['Ratings'] == 2.0:
                val = 'Negative'
            elif row['Ratings'] == 4.0 or row['Ratings'] == 5.0:
                val = 'Positive'
            else:
                val = -1
            return val
        
        df['Cleaned Review'] = df['Review'].apply(review_cleaning)
        df['Sentiment'] = df.apply(f, axis=1)
        df['Polarity'] = df['Cleaned Review'].map(lambda text: TextBlob(text).sentiment.polarity)
        df['review_len'] = df['Cleaned Review'].astype(str).apply(len)
        df['word_count'] = df['Cleaned Review'].apply(lambda x:len(str(x).split()))

        sentiments = ["Positive","Negative"]
        sentiment_choice=st.multiselect("Choose the sentiment",sentiments)
        viz_selection=st.radio("Select your viz",['Wordcloud','Bar Chart'])
        
        if viz_selection=='Wordcloud':

            #st.write(df)
            # sentiments = ["Positive","Negative"]
            # sentiment_choice=st.multiselect("Choose a sentiment",sentiments)
            
            if sentiment_choice == ["Positive"]:
                review_pos = df[df["Sentiment"]=='Positive'].dropna()
                fig_pos = create_wordcloud(review_pos)
                st.pyplot(fig_pos,use_container_width=False)
                # st.image(,width=2)

            
            elif sentiment_choice == ["Negative"]:
                review_neg = df[df["Sentiment"]=='Negative'].dropna()
                fig_neg = create_wordcloud(review_neg)
                st.pyplot(fig_neg,use_container_width=False)
            
            elif set(sentiment_choice) == set(sentiments):
                review_pos = df[df["Sentiment"]=='Positive'].dropna()
                review_neg = df[df["Sentiment"]=='Negative'].dropna()
                fig_pos = create_wordcloud(review_pos)
                st.pyplot(fig_pos,use_container_width=False)
                fig_neg = create_wordcloud(review_neg)
                st.pyplot(fig_neg,use_container_width=False)
            
            
            else:
                pass
        
        else:
            review_pos = df[df["Sentiment"] == 'Positive'].dropna()
            review_neu = df[df["Sentiment"] == 'Neutral'].dropna()
            review_neg = df[df["Sentiment"] == 'Negative'].dropna()

            if sentiment_choice == ["Positive"]:
                bar_chart_pos = create_bar_chart(review_pos, 'blue')
                st.write(bar_chart_pos)

            elif sentiment_choice == ["Negative"]:
                bar_chart_neg = create_bar_chart(review_neg, 'orange')
                st.write(bar_chart_neg)

            elif set(sentiment_choice) == set(sentiments):
                bar_chart_pos = create_bar_chart(review_pos, 'blue')
                st.write(bar_chart_pos)
                bar_chart_neg = create_bar_chart(review_neg, 'orange')
                st.write(bar_chart_neg)
            
            else:
                pass

with tab4:
    if reviews.get(console) == " ":
       st.write("Please make a selection to see further")

    if console == 'Playstation5':
        ps5_sales_chart = create_console_sales_chart("PlayStation 5 (PS5)")
        st.write(ps5_sales_chart)
    elif console == 'Xbox SeriesX':
        xbox_sales_chart = create_console_sales_chart("Xbox Series X/S (XS)")
        st.write(xbox_sales_chart)
    elif console == "Nintendo Switch":
        ns_sales_chart = create_console_sales_chart("Nintendo Switch (NS)")
        st.write(ns_sales_chart)
    else:
        pass
