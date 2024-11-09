import pandas as pd
import understatapi

# Initialize the Understat client
client = understatapi.UnderstatClient()

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

def get_match_stats_for_bvb(league_data):
    """Extract match statistics for Borussia Dortmund (BVB)."""
    match_stats = []
    for match in league_data:
        match_id = match["id"]
        try:
            match_info = client.match(match=match_id).get_match_info()
        except Exception as e:
            print(f"Error fetching data for match ID {match_id}: {e}")
            continue

        if match_info['h'] == BVB_TEAM_ID or match_info['a'] == BVB_TEAM_ID:
            stats = {
                'match_id': match_info['id'],
                'date': match_info['date'],
                'league': match_info['league'],
                'team_h': match_info['team_h'],
                'team_a': match_info['team_a'],
                'h_goals': match_info['h_goals'],
                'a_goals': match_info['a_goals'],
                'h_xg': match_info['h_xg'],
                'a_xg': match_info['a_xg'],
                'h_shot': match_info['h_shot'],
                'a_shot': match_info['a_shot'],
                'h_shotOnTarget': match_info['h_shotOnTarget'],
                'a_shotOnTarget': match_info['a_shotOnTarget'],
                'h_ppda': match_info['h_ppda'],
                'a_ppda': match_info['a_ppda'],
                'h_deep': match_info['h_deep'],
                'a_deep': match_info['a_deep'],
                'venue': 'Home' if match_info['h'] == BVB_TEAM_ID else 'Away',
                'team': match_info['team_h'] if match_info['h'] == BVB_TEAM_ID else match_info['team_a'],
                'opponent': match_info['team_a'] if match_info['h'] == BVB_TEAM_ID else match_info['team_h']
            }
            match_stats.append(stats)
    return match_stats

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
    bvb_match_stats = get_match_stats_for_bvb(league_data)
    bvb_shot_data = get_shot_data_for_players(pd.DataFrame(bvb_player_stats))

    # Create DataFrames
    df_bvb_matches = pd.DataFrame(bvb_matches).head(34)
    df_bvb_player_stats = pd.DataFrame(bvb_player_stats)
    df_bvb_match_stats = pd.DataFrame(bvb_match_stats)
    df_bvb_shot_data = pd.DataFrame(bvb_shot_data)

    # Filter for the 2024 season and reset index
    df_bvb_shot_data = df_bvb_shot_data[df_bvb_shot_data['season'] == SEASON].reset_index(drop=True)

    # Output DataFrames
    print(df_bvb_matches)
    print(df_bvb_player_stats)
    print(df_bvb_match_stats)
    print(df_bvb_shot_data)

    # Save data to CSV
    df_bvb_matches.to_csv('matches_bvb_2024.csv', index=False)
    df_bvb_player_stats.to_csv('player_stats_bvb_2024.csv', index=False)
    df_bvb_shot_data.to_csv('shots_bvb_2024.csv', index=False)

if __name__ == "__main__":
    main()
