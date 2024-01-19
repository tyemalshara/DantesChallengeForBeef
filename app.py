import streamlit as st
import requests
import pandas as pd
import os 
from dotenv import load_dotenv
from deta import Deta  # Import Deta
load_dotenv()
st.set_page_config(layout="wide")
import urllib.request



def login():
    st.sidebar.title("Login to add player participants")

    password = st.sidebar.text_input("Password", type='password')

    if st.sidebar.button("Login") or password:
        # Authentication goes here
        # You can add a function to check the validity of the username and password
        b9ula_admin_password = os.getenv("B9ULA_ADMIN_PASSWORD")
        if password == b9ula_admin_password:    # or username == 'sharatye' and password == 'beefb9ula'
            st.session_state['login'] = True
            # print(st.session_state['login'])
            return st.session_state['login']
        else:
            st.sidebar.error("Invalid username or password")
    return False

# def get_data(added_playernames_byuser, deleted_playernames_byuser):
#     playernames = ["timoschka17", "BeefQ8i"]
#     # append added_playernames_byuser to playernames list. In case of duplicates, skip the duplicate
#     for playername in added_playernames_byuser:
#         if playername not in playernames:
#             playernames.append(playername)
#         else:
#             continue
#     print("playernames after adding",playernames)
#     # remove deleted_playernames_byuser from playernames list. In case of non-existence, skip the name. 
#     for playername in deleted_playernames_byuser:
#         if playername in playernames:
#             playernames.remove(playername)
#         else:
#             continue
#     # get api key from .env file 
#     riot_api_key = os.getenv("RIOT_API_KEY")
#     list_of_players = []
#     for playername in playernames:
#         api_url = f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{playername}" + '?api_key=' + riot_api_key
#         player_info = requests.get(api_url).json()
#         player_id = player_info['id']
#         entries_url = f"https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/{player_id}" + '?api_key=' + riot_api_key
#         player_entries = requests.get(entries_url).json()
#         leaguePoints = player_entries[0]['leaguePoints']
#         # add playername and leaguePoints as key-value pair to list_of_players
#         list_of_players.append({playername: leaguePoints})
#     print(list_of_players)
#     return list_of_players

# def get_data_test(added_playernames_byuser, deleted_playernames_byuser):
#     # playernames = ["timoschka17", "BeefQ8i"]
#     st.session_state["playernames"]
#     # append added_playernames_byuser to playernames list. In case of duplicates, skip the duplicate
#     for playername in added_playernames_byuser:
#         if playername not in st.session_state["playernames"]:
#             st.session_state["playernames"].append(playername)
#         else:
#             continue
#     print("playernames after adding",st.session_state["playernames"])
#     # remove deleted_playernames_byuser from playernames list. In case of non-existence, skip the name. 
#     for playername in deleted_playernames_byuser:
#         if playername in st.session_state["playernames"]:
#             st.session_state["playernames"].remove(playername)
#         else:
#             continue
#     print("playernames after deleting",st.session_state["playernames"])

def get_data_from_db(added_playernames_byuser, deleted_playernames_byuser):
    PLAYER_PARTICIPANTS_KEY = os.getenv("PLAYER_PARTICIPANTS_KEY")
    # Initialize
    deta = Deta(PLAYER_PARTICIPANTS_KEY)
    # This how to connect to or create a database.
    db = deta.Base("beef")

    def insert_player(playernames_tobe_added):
        '''Inserts a player into the database
        e.g. insert_player("timoschka17")
        Returns the player on a successful player creation, otherwise raises an error'''
        try:
            return db.insert({"playername": playernames_tobe_added}, playernames_tobe_added)
        except urllib.error.HTTPError as e:
            if e.code == 409:  # Conflict error
                print(f"A player with the name {playernames_tobe_added} already exists.")
            else:
                raise  # Re-raise the exception if it's not a conflict error
        # return db.insert({"playername": playernames_tobe_added}, playernames_tobe_added)

    def delete_player(playernames_tobe_deleted):
        '''Deletes a player from the database
        e.g. delete_player("timoschka17")
        Returns the player on a successful player deletion, otherwise raises an error'''
        # Delete a player
        return db.delete(playernames_tobe_deleted)

    def fetch_all_players():
        '''Retruns a list of dicts with all the players in the database
        e.g. [{'playername': 'timoschka17'}, {'playername': 'BeefQ8i'}]'''
        # Fetch all the items in the database
        res = db.fetch()
        return res.items
    
    # playernames = ["timoschka17", "BeefQ8i"]
    # st.session_state["playernames"]
    # append added_playernames_byuser to playernames list. In case of duplicates, skip the duplicate
    # for playername in added_playernames_byuser:
        # if playername not in st.session_state["playernames"]:
    if len(added_playernames_byuser) > 0:
        # st.session_state["playernames"].append(added_playernames_byuser[0])
        print("added_playernames_byuser[0]: ",added_playernames_byuser[0])
        insert_player(added_playernames_byuser[0])
        # remove elment from added_playernames_byuser
        added_playernames_byuser.pop(0)
        # else:
            # continue
    # print("playernames after adding",st.session_state["playernames"])
    # remove deleted_playernames_byuser from playernames list. In case of non-existence, skip the name. 
    # for playername in deleted_playernames_byuser:
        # if playername in st.session_state["playernames"]:   # should prevent calling the api more than needed
    if len(deleted_playernames_byuser) > 0:
        # st.session_state["playernames"].remove(deleted_playernames_byuser[0])
        print("deleted_playernames_byuser[0]: ",deleted_playernames_byuser[0])
        delete_player(deleted_playernames_byuser[0])
        # remove elment from deleted_playernames_byuser
        deleted_playernames_byuser.pop(0)
        # else:
        #     continue
    # print("playernames after deleting",st.session_state["playernames"])
    
    player_not_found = str()
    # get api key from .env file 
    riot_api_key = os.getenv("RIOT_API_KEY")
    list_of_players = []
    for playername in fetch_all_players():
        try:
            api_url = f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{playername['playername']}" + '?api_key=' + riot_api_key
            player_info = requests.get(api_url).json()
            player_id = player_info['id']
            entries_url = f"https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/{player_id}" + '?api_key=' + riot_api_key
            player_entries = requests.get(entries_url).json()
            leaguePoints = player_entries[0]['leaguePoints']
            # add playername and leaguePoints as key-value pair to list_of_players
            list_of_players.append({playername['playername']: leaguePoints})
        except:
            # st.error(player_info["status"]["message"], icon="🚨")
            print(f"Player {playername['playername']} was not found")
            player_not_found = f"Player {playername['playername']} was not found"
            delete_player(playername['playername'])
            continue       
    print(list_of_players)
    return list_of_players, player_not_found

def app():
    if login():
        # print("st.session_state['login'] ->", st.session_state['login'])
        # let the user add players to the list of participants 'playernames'
        # st.title("Add player participants")
        with st.form('player_input_form'):
            inputfield, addbuttonfield, deletebuttonfield = st.columns([0.9, 0.1, 0.1])
            with inputfield:
                playernames = st.text_input("Player names to be added/deleted", placeholder="Player names to be added/deleted e.g. BeefQ8i", label_visibility='collapsed')
            with addbuttonfield:
                # add_button = st.button("Add")
                add_button = st.form_submit_button("Add")
            with deletebuttonfield:
                # delete_button = st.button("Delete")
                delete_button = st.form_submit_button("Delete")
            if playernames:
                if add_button:
                    st.session_state["playernames"] = [playername.strip() for playername in playernames.split(", ") if playername.strip()]
                    print("playernames_tobe_added: ",st.session_state["playernames"])
                if delete_button:
            # playernames_tobe_deleted = st.text_input("Player names to be deleted")
            # if st.button("Delete") and playernames_tobe_deleted:
                    st.session_state["playernames_tobe_deleted"] = [playername.strip() for playername in playernames.split(", ") if playername.strip()]
                    print("playernames_tobe_deleted: ", st.session_state["playernames_tobe_deleted"])
        # data = get_data(st.session_state["playernames"], st.session_state["playernames_tobe_deleted"])
        # get_data_test(st.session_state["playernames"], st.session_state["playernames_tobe_deleted"])
        with st.spinner("Loading data..."):
            data, player_not_found = get_data_from_db(st.session_state["playernames"], st.session_state["playernames_tobe_deleted"])
        if player_not_found:
            st.error(player_not_found, icon="🚨")
        elif playernames and not player_not_found and add_button:
            st.success(f"Done! Player **{playernames}** has been added, icon= '👍'")
        elif playernames and not player_not_found and delete_button:
            st.success(f"Done! Player **{playernames}** has been deleted, icon= '👍'")
        # data = [{'timoschka17': 23}, {'BeefQ8i': 37}, {'Beefh8i': 35}, {'BeehgfQ8i': 37}, {'BeefQjhj8i': 37}, {'BeefQds8i': 37}, {'BeeasfQ8i': 37}, {'BwqeeefQ8i': 37}]
        df = pd.DataFrame([{k: v for d in data for k, v in d.items()}])
        df = df.T.reset_index()
        df.columns = ['player_name', 'league_points']
        df['league_points'] = df['league_points'].astype(float)
        df = df.sort_values(by=['league_points'], ascending=False)
        _, col2, _ = st.columns([1, 3, 1])

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
        # return df
    else:
        st.title("Please login to proceed")
if __name__ == "__main__":
    st.session_state['playernames_default'] = []
    if "playernames_default" not in st.session_state:   # list of current players 
        st.session_state['playernames_default'] = []
    if "playernames_tobe_deleted" not in st.session_state:
        st.session_state['playernames_tobe_deleted'] = []
    if "playernames" not in st.session_state:   # to be added
        st.session_state['playernames'] = []
    if 'login' not in st.session_state:
        st.session_state['login'] = False
    print("Program has started!")
    app()
    # if "external_data" not in st.session_state:
    #     # api_result = get_data()
    #     cleaned_data = app()
    #     # print("I've been called: ", cleaned_data)
    #     st.session_state["external_data"] = cleaned_data


