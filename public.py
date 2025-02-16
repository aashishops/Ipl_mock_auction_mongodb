import streamlit as st
from pymongo import MongoClient

# MongoDB connection
mongo_uri = st.secrets["mongo_uri"]["mongo_uri"]
client = MongoClient(mongo_uri)
db = client['players']
bids_collection = db['players_bid']

# Streamlit App
st.title("IPL Mock Auction - Team Bids View")

# Dropdown to select IPL team
teams = [
    "Chennai Super Kings", "Mumbai Indians", "Royal Challengers Bangalore", 
    "Kolkata Knight Riders", "Sunrisers Hyderabad", "Delhi Capitals", 
    "Rajasthan Royals", "Punjab Kings", "Lucknow Super Giants", "Gujarat Titans", "Unsold"
]

selected_team = st.selectbox("Select IPL Team", teams)

# Refresh button
if st.button("Refresh"):
    st.rerun()

# Fetch bids data from MongoDB
data = list(bids_collection.find({}, {"_id": 0}))

# Display bids for the selected team
st.header(selected_team)
team_bids = [entry for entry in data if entry['ipl_team'] == selected_team]
if team_bids:
    st.table(team_bids)
else:
    st.write(f"No bids for {selected_team} yet!")
