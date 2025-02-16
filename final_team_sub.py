import streamlit as st
from pymongo import MongoClient

# MongoDB Connection
mongo_uri = st.secrets["mongo_uri"]["mongo_uri"]
client = MongoClient(mongo_uri)
db = client['players']  # Database name
bids_collection = db['players_bid']  # Collection for bids
final_teams_collection = db['finalteams']  # Collection for final teams

# IPL Teams
ipl_teams = [
    "Chennai Super Kings", "Mumbai Indians", "Royal Challengers Bangalore", 
    "Kolkata Knight Riders", "Sunrisers Hyderabad", "Delhi Capitals", 
    "Rajasthan Royals", "Punjab Kings", "Lucknow Super Giants", "Gujarat Titans"
]

# Streamlit App
st.title("IPL Final Team Submission")

# Team Authentication
st.sidebar.header("Team Authentication")
selected_team = st.sidebar.selectbox("Select Your IPL Team", ipl_teams)
team_password = st.sidebar.text_input("Enter Team Password", type="password")

# Dummy authentication for now (replace with secure method)
team_passwords = {
    "Chennai Super Kings": "csk123",
    "Mumbai Indians": "mi123",
    "Royal Challengers Bangalore": "rcb123",
    "Kolkata Knight Riders": "kkr123",
    "Sunrisers Hyderabad": "srh123",
    "Delhi Capitals": "dc123",
    "Rajasthan Royals": "rr123",
    "Punjab Kings": "pbks123",
    "Lucknow Super Giants": "lsg123",
    "Gujarat Titans": "gt123"
}

if team_password != team_passwords.get(selected_team, ""):
    st.error("Incorrect password!")
    st.stop()

# Fetch players already bid on for the selected team
team_players = bids_collection.find({"ipl_team": selected_team}, {"_id": 0, "player_name": 1, "bid_amount": 1, "Role": 1, "Points": 1})
player_data = [{
    "player_name": player['player_name'], 
    "bid_amount": player['bid_amount'], 
    "Role": player['Role'], 
    "Points": player.get('Points', player.get(' Points ', 0))  # Handle inconsistent field names
} for player in team_players]

player_names = [player['player_name'] for player in player_data]

if len(player_names) < 11:
    st.warning(f"{selected_team} currently has {len(player_names)} players. Select 11 players to finalize the team.")

st.header(f"Select Final 11 for {selected_team}")

# Dropdowns for 11 players
final_team = []
for i in range(11):
    player = st.selectbox(f"Player {i + 1}", player_names, key=f"player_{i + 1}")
    final_team.append(player)

# Final Team Submission
if st.button("Submit Final Team"):
    if len(set(final_team)) < 11:
        st.error("Please select 11 unique players!")
    else:
        final_team_data = [player for player in player_data if player['player_name'] in final_team]
        final_teams_collection.update_one(
            {"team_name": selected_team},
            {"$set": {"players": final_team_data}},
            upsert=True
        )
        st.success(f"Final team for {selected_team} submitted successfully!")

        # Display the final team details in a table
        st.header(f"{selected_team} Final Team Details")
        st.dataframe(final_team_data)
        average_points = sum(player['Points'] for player in final_team_data) / len(final_team_data)
        st.write(f"Average Points: {average_points:.2f}")
