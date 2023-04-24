import pandas as pd
import streamlit as st
import altair as alt

st.set_page_config(layout='wide')

def create_freq_chart(variable):
    new_games_df = games_df[['Game', variable]].groupby([variable]).count().sort_values('Game',ascending=False).reset_index()
    freq_chart = alt.Chart(new_games_df).mark_bar().encode(
            x=alt.X(variable, sort=alt.EncodingSortField(field=variable, op='count')),
            y=alt.Y('Game')
    )
    return freq_chart

def create_scatter_plot(sales_selection, score_selection):
    # Drop N/A for columns
    new_games_df = games_df[[score_selection, sales_selection]]
    result_games_df = new_games_df.dropna(subset=[score_selection]).reset_index(drop=True)
    result_games_df = new_games_df.dropna(subset=[sales_selection]).reset_index(drop=True)
    final_games_df = result_games_df.dropna(subset=[score_selection]).reset_index(drop=True)
    
    scatter = alt.Chart(final_games_df).mark_circle(size=60).encode(
            x=score_selection,
            y=sales_selection,
            tooltip=[score_selection, sales_selection]
    ).interactive()
    # correlation_coeff = final_games_df.corr()
    # st.write('We can obtain the correlation coefficient using the scatter plot and the matrix is below:')
    # st.write(correlation_coeff)

    return scatter

tab1, tab2, tab3 = st.tabs(["Games Stats", "Scatter Plots", "Top Rated Games"])

with tab1:
    games_df=pd.read_csv("files/final_app_data.csv", encoding='latin-1')
    st.write('We can look at Game statistics and see what attributes effect the number of games released.')
    selection=st.selectbox("Choose your variable",['','Console','Genre','Publisher','Developer'])

    if selection == 'Console':
        console_freq_chart = create_freq_chart('Console')
        st.write(console_freq_chart)
    elif selection == 'Genre':
        genre_freq_chart = create_freq_chart('Genre')
        st.write(genre_freq_chart)
    elif selection == 'Publisher':
        publisher_freq_chart = create_freq_chart('Publisher')
        st.write(publisher_freq_chart)
    elif selection == 'Developer':
        developer_freq_chart = create_freq_chart('Developer')
        st.write(developer_freq_chart)

with tab2:
    sales_choice = st.selectbox("What sales would you like to see:",
                 ('', 'Total Sales','NA Sales', 'PAL Sales' ,'Japan Sales' ,'Other Sales' ))
    st.write('*PAL Sales are sales in Europe')
    st.write('**Please note all sales values are in millions')
    score_choice = st.selectbox('Please choose what ratings you would like to see',
                 ('', 'VGChartz Score', 'Critic Score', 'User Score'))
    if sales_choice != '' and score_choice != '':
        scatter_plot = create_scatter_plot(sales_choice, score_choice)
        st.write(scatter_plot)

with tab3:
    st.write("Let's take a look at the Top Rated Games")
    rating_system = st.selectbox("Choose the rating system:",
                 ('', 'VGChartz Score', 'Critic Score', 'User Score'))
    top_count = st.slider('How many of the Top rated games would you like to view:',
                          min_value=1,max_value=200,value=50,step=10)
    if rating_system != '':
        new_games_df = games_df[['Game', rating_system]]
        result_games_df = new_games_df.dropna(subset=[rating_system]).reset_index(drop=True)
        final_df = result_games_df.drop_duplicates(subset=['Game'])
        final_df = final_df.sort_values(by=rating_system, ascending=False)
        bar_chart = alt.Chart(final_df.head(top_count)).mark_bar().encode(
                    x=alt.X('Game',sort=alt.EncodingSortField(field="Game", op='count')),
                    y=alt.Y(rating_system),
                    color=alt.Color(rating_system, scale=alt.Scale(scheme='redyellowgreen'))
                    )
        st.write(bar_chart)    


    
    


# bar_chart = alt.Chart(df).mark_bar().encode(
#             x=alt.X('frequency'),
#             y=alt.Y('word',sort=alt.EncodingSortField(field="word", op='count')),
#             color=alt.Color('frequency', scale=alt.Scale(scheme='redyellowgreen'))
#             )    






