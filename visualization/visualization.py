import streamlit_shadcn_ui as ui
from datetime import datetime
import plotly.express as px
import streamlit as st
import pandas as pd


#Stylize the app
st.set_page_config(layout="wide")
with open ('../styles/visualize.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

df = pd.read_csv("../dataset/disney_data_csv.csv")

df = df.rename(columns={'title': 'Title', 'imdb':'IMDB', 'rotten_tomatoes':'Rotten Tomatoes'})
df = df.dropna(subset=['Release date (datetime)', 'Country', 'Language'])
df['Release date (datetime)'] = pd.to_datetime(df['Release date (datetime)'], errors='coerce')
df = df.dropna(subset=['Release date (datetime)'])

#Converting years to decaded for ex:1940s
df['Decade'] = df['Release date (datetime)'].dt.year.astype(str).str[:3] + '0s' 

col1, col2, col3 = st.columns(3)

with col1:
    decades = st.multiselect(
            'Select Decades:', 
             df['Decade'].unique(),
             default=df['Decade'].unique()[:2])

with col2:
    countries = st.multiselect(
               'Select Country:', 
                df['Country'].unique(),
                default=df['Country'].unique()[:2])

with col3:
    languages = st.multiselect(
               'Select Language:', 
                df['Language'].unique(),
                default=df['Language'].unique()[:2])

filtered_df = df[
    df['Decade'].isin(decades) &
    df['Country'].isin(countries) &
    df['Language'].isin(languages)
]

fig1 = px.scatter(filtered_df, 
                 x='Budget', 
                 y='Box office', 
                 color='Country', 
                 size='IMDB', 
                 hover_name= 'Title',  
                 title='Budget vs Box Office Performance',
                 labels={'Budget': 'Budget (in USD)', 'Box office': 'Box Office (in USD)', 'IMDB': 'IMDB Rating'},
                 size_max=70)  # Control the maximum size of points

fig2 = px.scatter(filtered_df, 
                 x='IMDB', 
                 y='Rotten Tomatoes', 
                 color='Country', 
                 size='IMDB', 
                 hover_name= 'Title',  
                 title='IMDB Rating vs Rotten Tomatoes Rating',
                 labels={'IMDB': 'IMDB Rating', 'rotten_tomatoes': 'Rotten Tomatoes'},
                 size_max=70)  

top_10_movies = filtered_df.nlargest(10, 'Box office (float)')

fig3 = px.bar(top_10_movies, 
             x='Title', 
             y='Box office', 
             color='IMDB', 
             title='Top 10 Movies by Box Office Performance',
             labels={'Box office': 'Box Office (in USD)', 'IMDB': 'IMDB Rating'},
             hover_name='Title')

#Show metric card
total_budget = df['Budget (float)'].sum()
total_box_office = df['Box office (float)'].sum()
highest_imdb = df['IMDB'].max()
last_budget = df.iloc[-1]['Budget (float)']
second_last_budget = df.iloc[-2]['Budget (float)']
budget_diff = last_budget - second_last_budget
budget_change = (budget_diff/second_last_budget) * 100
last_box_office = df.iloc[-1]['Box office (float)']
second_last_box_office = df.iloc[-2]['Box office (float)']
box_office_change = ((last_box_office - second_last_box_office) / second_last_box_office) * 100

cols = st.columns(3)
with cols[0]:
    ui.metric_card(title="Total Budget (USD)", 
                   content=f"${total_budget:,.2f}", 
                   description=f"{budget_change:,.2f}% from last movie", 
                   key="card1")
with cols[1]:
    ui.metric_card(title="Total Box Office (USD)", 
                   content=f"${total_box_office:,.2f}", 
                   description=f"{box_office_change:,.2f}% from last movie", 
                   key="card2")
with cols[2]:
        ui.metric_card(title="Budget Change for Last Movie", 
                       content=f"${last_budget:,.2f}", 
                       description=f"{budget_change:,.2f}% from last movie", 
                       key="card3")

#Show recently released movies
today = pd.to_datetime(datetime.today().strftime('%Y-%m-%d'))
df['Recent releases'] = pd.to_datetime(df['Release date (datetime)'])
df = df.sort_values(by='Recent releases', ascending=False)
df['Release dates'] = df['Release date (datetime)'].apply(lambda x: x.strftime('%Y %b, %d'))
df_recent = df[df['Recent releases'] <= today].head(12)
df_recent = df_recent.reset_index(drop=True)
df_recent.index = df_recent.index + 1
st.write("### Most Recent Movie Releases")
columns_to_show = ['Title', 'Release dates', 'Budget', 'Box office', 'IMDB', 'Rotten Tomatoes', 'Country', 'Language']

cols= st.columns(2)
with cols[0]:
    st.dataframe(df_recent[columns_to_show], use_container_width=True, height=450)
with cols[1]:
    st.plotly_chart(fig3)

col1, col2 = st.columns([6,6])
with col1:
    st.plotly_chart(fig1)
with col2:
    st.plotly_chart(fig2)
