import streamlit as st
from pymongo import MongoClient

# MongoDB Connection

mongo_uri = st.secrets["mongo_uri"]["mongo_uri"]

print("URI:", mongo_uri)
client = MongoClient(mongo_uri)
db = client['players']  # Database name
players_collection = db['playerslist']  # Collection with player names
bids_collection = db['players_bid']  # Collection for bids

# Streamlit App
st.title("IPL Mock Auction")

# Fetch player names from MongoDB
all_players = players_collection.find({}, {"_id": 0, "Player Name": 1})
all_player_names = [player.get('Player Name', '') for player in all_players if 'Player Name' in player]

# Fetch players who have already been bid on
bidded_players = bids_collection.distinct("player_name")

# Filter out players who have already been bid on
available_players = [name for name in all_player_names if name not in bidded_players]

# Create IPL Mock Auction Form
st.header("Create Bid")
with st.form("create_bid_form"):
    player_name = st.selectbox("Player Name", available_players)
    ipl_team = st.selectbox("IPL Team", [
        "Chennai Super Kings", "Mumbai Indians", "Royal Challengers Bangalore", 
        "Kolkata Knight Riders", "Sunrisers Hyderabad", "Delhi Capitals", 
        "Rajasthan Royals", "Punjab Kings", "Lucknow Super Giants", "Gujarat Titans"
    ])
    bid_amount = st.number_input("Bid Amount (in Lakhs)", min_value=0, key="create_bid_amount")
    submit_button = st.form_submit_button("Create Bid")

if submit_button:
    if player_name and ipl_team and bid_amount:
        bids_collection.insert_one({"player_name": player_name, "ipl_team": ipl_team, "bid_amount": bid_amount})
        st.success("Bid created successfully!")
        st.rerun()
    else:
        st.error("Please fill in all fields.")

# Display Bids Data with Local Search
st.write("## Current Bids")
search_query = st.text_input("Search Bids")

data = list(bids_collection.find({}, {"_id": 0}))

if search_query:
    data = [entry for entry in data if search_query.lower() in entry['player_name'].lower() or search_query.lower() in entry['ipl_team'].lower()]

st.table(data)

# Edit Bid Form
st.header("Edit Bid")
with st.form("edit_bid_form"):
    edit_player_name = st.selectbox("Select Player to Edit", bidded_players)
    new_ipl_team = st.selectbox("New IPL Team", [
        "Chennai Super Kings", "Mumbai Indians", "Royal Challengers Bangalore", 
        "Kolkata Knight Riders", "Sunrisers Hyderabad", "Delhi Capitals", 
        "Rajasthan Royals", "Punjab Kings", "Lucknow Super Giants", "Gujarat Titans","Unsold"
    ])
    new_bid_amount = st.number_input("New Bid Amount (in Lakhs)", min_value=0, key="edit_bid_amount")
    edit_submit_button = st.form_submit_button("Update Bid")

if edit_submit_button:
    if edit_player_name and new_ipl_team and new_bid_amount:
        bids_collection.update_one(
            {"player_name": edit_player_name},
            {"$set": {"ipl_team": new_ipl_team, "bid_amount": new_bid_amount}}
        )
        st.success("Bid updated successfully!")
        st.rerun()
    else:
        st.error("Please fill in all fields.")
