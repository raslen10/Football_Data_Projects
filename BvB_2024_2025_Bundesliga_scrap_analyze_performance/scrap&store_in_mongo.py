import pandas as pd
import understatapi
from pymongo import MongoClient

# Initialize the Understat client
client = understatapi.UnderstatClient()

# MongoDB setup
mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client["bvb_2024_2025"]

# Constants
BVB_TEAM_ID = '129'
SEASON = '2024'
LEAGUE = 'Bundesliga'

def fetch_league_matches():
    """Fetch all matches from the specified league and season."""
    league_data = client.league(league=LEAGUE).get_match_data(season=SEASON)
    return league_data

def extract_bvb_match_data(league_data):
    """Extract match data for Borussia Dortmund (BVB) from the league data."""
    matches = []
    for match in league_data:
        if match['h']['id'] == BVB_TEAM_ID or match['a']['id'] == BVB_TEAM_ID:
            match_info = {
                'match_id': match['id'],
                'date': match['datetime'],
                'home_team': match['h']['title'],
                'away_team': match['a']['title'],
                'home_score': match['goals']['h'],
                'away_score': match['goals']['a'],
                'home_xG': match['xG']['h'],
                'away_xG': match['xG']['a'],
                'forecast_win': match.get('forecast', {}).get('w', None),
                'forecast_draw': match.get('forecast', {}).get('d', None),
                'forecast_loss': match.get('forecast', {}).get('l', None),
            }
            matches.append(match_info)
    return matches

def get_player_stats_for_bvb(league_data):
    """Extract player stats for Borussia Dortmund (BVB) from the league data."""
    player_stats = []
    for match in league_data:
        match_id = match["id"]
        try:
            shot_data = client.match(match=match_id).get_roster_data()
        except Exception as e:
            print(f"Error fetching data for match ID {match_id}: {e}")
            continue

        home_players = shot_data.get('h', {})
        away_players = shot_data.get('a', {})

        for players, team in [(home_players, 'h'), (away_players, 'a')]:
            for player_id, player_info in players.items():
                if player_info['team_id'] == BVB_TEAM_ID:
                    player_stats.append({
                        'player_id': player_info['player_id'],
                        'match_id': match_id,
                        'player': player_info['player'],
                        'goals': player_info['goals'],
                        'shots': player_info['shots'],
                        'xG': player_info['xG'],
                        'yellow_cards': player_info['yellow_card'],
                        'red_cards': player_info['red_card'],
                        'key_passes': player_info['key_passes'],
                        'assists': player_info['assists'],
                        'xA': player_info['xA'],
                        'h_a': player_info['h_a'],
                        'minutes_played': player_info['time'],
                        'position': player_info['position'],
                        'position_order': player_info['positionOrder']
                    })
    return player_stats

def get_shot_data_for_players(df_player_stats):
    """Fetch shot data for each unique player from the player stats dataframe."""
    all_shot_data = []
    unique_player_ids = df_player_stats['player_id'].unique()

    for player_id in unique_player_ids:
        try:
            player_data = client.player(player=player_id).get_shot_data()
            for shot in player_data:
                shot['player_id'] = player_id
                all_shot_data.append(shot)
        except Exception as e:
            print(f"Error fetching shot data for player ID {player_id}: {e}")

    return all_shot_data

def main():
    # Fetch data
    league_data = fetch_league_matches()

    # Extract match, player, and shot data for Borussia Dortmund (BVB)
    bvb_matches = extract_bvb_match_data(league_data)
    bvb_player_stats = get_player_stats_for_bvb(league_data)
    bvb_shot_data = get_shot_data_for_players(pd.DataFrame(bvb_player_stats))

    # Insert data into MongoDB
    db.matches_bvb_2024.insert_many(bvb_matches)
    db.player_stats_bvb_2024.insert_many(bvb_player_stats)
    db.shots_bvb_2024.insert_many(bvb_shot_data)

    # Output DataFrames (for debugging)
    print(f"Inserted {len(bvb_matches)} matches")
    print(f"Inserted {len(bvb_player_stats)} player stats")
    print(f"Inserted {len(bvb_shot_data)} shot data")

if __name__ == "__main__":
    main()
