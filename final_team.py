import streamlit as st
from pymongo import MongoClient

# MongoDB Connection
mongo_uri = st.secrets["mongo_uri"]["mongo_uri"]
client = MongoClient(mongo_uri)
db = client['players']  # Database name
final_teams_collection = db['finalteams']  # Collection for final teams

# IPL Teams
ipl_teams = [
    "Chennai Super Kings", "Mumbai Indians", "Royal Challengers Bangalore", 
    "Kolkata Knight Riders", "Sunrisers Hyderabad", "Delhi Capitals", 
    "Rajasthan Royals", "Punjab Kings", "Lucknow Super Giants", "Gujarat Titans"
]

# Streamlit App
st.title("IPL Final Teams Overview")

# Dropdown to select IPL team
selected_team = st.selectbox("Select IPL Team", ipl_teams)

# Fetch final team data from MongoDB
team_data = final_teams_collection.find_one({"team_name": selected_team})

if team_data and 'players' in team_data:
    players = team_data['players']

    # Display final team details
    st.header(f"{selected_team} Final Team Details")
    st.dataframe(players)

    # Calculate and display the average points
    total_points = sum(player['Points'] for player in players)
    average_points = total_points / len(players)
    st.write(f"Average Points: {average_points:.2f}")

    # Calculate and display the budget remaining
    total_budget_spent = sum(player['bid_amount'] for player in players)
    remaining_budget = (10000 - total_budget_spent)/100  # Assuming a budget cap of 10000
    st.write(f"Budget Remaining: {remaining_budget:.2f} Crores")

else:
    st.warning(f"No final team found for {selected_team}.")
