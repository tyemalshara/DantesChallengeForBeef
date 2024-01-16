import streamlit as st
import requests
import pandas as pd
import os 
from dotenv import load_dotenv
load_dotenv()
st.set_page_config(layout="wide")

def get_data():
    playernames = ["timoschka17", "BeefQ8i"]
    # get api key from .env file 
    riot_api_key = os.getenv("RIOT_API_KEY")
    list_of_players = []
    for playername in playernames:
        api_url = f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{playername}" + '?api_key=' + riot_api_key
        player_info = requests.get(api_url).json()
        player_id = player_info['id']
        entries_url = f"https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/{player_id}" + '?api_key=' + riot_api_key
        player_entries = requests.get(entries_url).json()
        leaguePoints = player_entries[0]['leaguePoints']
        # add playername and leaguePoints as key-value pair to list_of_players
        list_of_players.append({playername: leaguePoints})
    print(list_of_players)
    return list_of_players

def app():
    data = get_data()
    # data = [{'timoschka17': 23}, {'BeefQ8i': 37}, {'Beefh8i': 35}, {'BeehgfQ8i': 37}, {'BeefQjhj8i': 37}, {'BeefQds8i': 37}, {'BeeasfQ8i': 37}, {'BwqeeefQ8i': 37}]
    df = pd.DataFrame([{k: v for d in data for k, v in d.items()}])
    df = df.T.reset_index()
    df.columns = ['player_name', 'league_points']
    df['league_points'] = df['league_points'].astype(float)
    df = df.sort_values(by=['league_points'], ascending=False)
    _, col2, _ = st.columns([1, 2, 1])

    with col2:
        st.title('مسابقة الليق اوف ليجندز برعاية :grey[بــــــيــف] :meat_on_bone: ', anchor='العنوان') 
        st.header(' :facepunch:  الأقوى يفوز بـ لحمة لا مثيل لمذاقها ', anchor='التعليمات', help='التعليمات', divider='rainbow')
    st.markdown("***")
    # st.write(df)
    container = st.container()
    meat, chicken, pizza, hamburger = ":meat_on_bone:", ":poultry_leg:", ":pizza:", ":hamburger:"
    with container:    
        for i in range(len(df)):
            if i == 0:
                container.subheader(f":first_place_medal: + {meat} **" + df[['player_name', 'league_points']].values[i][0] + "** has " + str(int(df[['player_name', 'league_points']].values[i][1])) + " league points.")
            elif i == 1:
                container.subheader(f":second_place_medal: + {hamburger} **" + df[['player_name', 'league_points']].values[i][0] + "** has " + str(int(df[['player_name', 'league_points']].values[i][1])) + " league points.")
            elif i == 2:   
                container.subheader(f":third_place_medal: + {chicken} **" + df[['player_name', 'league_points']].values[i][0] + "** has " + str(int(df[['player_name', 'league_points']].values[i][1])) + " league points.")
            else:
                container.subheader(f"{pizza} **" + df[['player_name', 'league_points']].values[i][0] + "** has " + str(int(df[['player_name', 'league_points']].values[i][1])) + " league points.")
            container.divider()
    return df
if __name__ == "__main__":
    # app()
    if "external_data" not in st.session_state:
        # api_result = get_data()
        cleaned_data = app()
        # print("I've been called: ", cleaned_data)
        st.session_state["external_data"] = cleaned_data


