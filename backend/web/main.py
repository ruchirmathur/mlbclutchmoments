import requests
import json
from flask import Flask, jsonify, request
import vertexai
import os
from flask_cors import CORS
from vertexai.generative_models import (
    FunctionDeclaration, GenerationConfig, GenerativeModel, Part, Tool
)
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Vertex AI
PROJECT_ID = ""  # @param {type:"string"}
LOCATION = ""  # @param {type:"string"}
vertexai.init(project=PROJECT_ID, location=LOCATION)

app = Flask(__name__)
CORS(app, origins=[""])

# Function Declarations
get_mlb_leagues = FunctionDeclaration(
    name="get_mlb_leagues",
    description="Provides detailed information about all the Major League Baseball leagues that are playing in a given season and those leagues where division is still in use. This API can provide details about the number of leagues in MLB. It provides details on the number of games played in the league for a season, number of teams that are part of the league, number of wild card teams,preSeasonStartDate,preSeasonEndDate,seasonStartDate,springStartDate,springEndDate,regularSeasonStartDate,allStarDate,regularSeasonEndDate,postSeasonStartDate,postSeasonEndDate,seasonEndDate,offseasonStartDate,offSeasonEndDate,qualifierPlateAppearances",
    parameters={
        "type": "object",
        "properties": {
            "season": {
                "type": "string",
                "description": "season that the team is playing in",
            }
        },
    },
)
get_mlb_seasons = FunctionDeclaration(
    name="get_mlb_seasons",
    description="Provides detailed information about all the Major League Baseball seasons. This includes springStartDate,springEndDate,preSeasonStartDate,seasonStartDate,regularSeasonStartDate,regularSeasonEndDate,seasonEndDate,offseasonStartDate,offSeasonEndDate,qualifierPlateAppearances,qualifierOutsPitched,allStarDate",
    parameters={
        "type": "object",
        "properties": {
            "sportId": {
                "type": "string",
                "description": "MLB sport id",
            },
             "season": {
                "type": "string",
                "description": "Season",
            }

        },
    },
)
get_mlb_teams = FunctionDeclaration(
    name="get_mlb_teams",
    description="Retrieves all the Major League Baseball teams and not players. It retrieves team id or the id of all the teams, springLeague information, venue and stadium information, first year of play for that team, location of the team, which league does the team play in, which division does the team play in. Any query about a team without season information can be addressed using this API call.",
    parameters={
        "type": "object",
        "properties": {
            "sportID": {
                "type": "string",
                "description": "Sport id for MLB",
            }
        },
    },
)

get_mlb_teams_by_season = FunctionDeclaration(
    name="get_mlb_teams_by_season",
    description="Provides details about all the Major Leaguee Baseball teams playing in a given season. It retrieves team id or the id of all the teams, springLeague information, venue information, stadium information, first year of play for that team, location of the team, which league does the team play in, which division does the team play in. Any query about a team can be addressed using this API call.",
    parameters={
        "type": "object",
        "properties": {
            "season": {
                "type": "string",
                "description": "season that the team is playing in",
            }
        },
    },
)

get_mlb_teams_by_teamname_season = FunctionDeclaration(
    name="get_mlb_teams_by_teamname_season",
    description="Provides details about the particular Major Leaguee Baseball team playing in a given season and by team id. It retrieves team id or the id for a particular team, springLeague information, venue information, stadium information, first year of play for that team, location of the team, which league does the team play in, which division does the team play in. Any query about a team can be addressed using this API call.",
    parameters={
        "type": "object",
        "properties": {
            "season": {
                "type": "string",
                "description": "season that the team is playing in",
            },
            "team_id": {
                "type": "string",
                "description": "Id of the team",
            }
        },
    },
)

get_roster = FunctionDeclaration(
    name="get_roster",
    description="This provides MLB team roster information and its summary. It provides all information about all players playing for MLB in a season. Basic information about the MLB player name, player birthDate, name, player jersey number, player height, player weight,player number, player birth date,current player age, player birth city,player birth state, player birth country,player height, player weight, player position, draft year, education,awards name,award date,award season, award team,award date,mlb debut date,bat side code,pitch hand code,strike zone top, stroke zone bottom,draft pick round, draft pick number,signing bonus, trades or transactions, trade or transaction teams, trade or transactions dates,trade description,player type, player active or inactive",
    parameters={
        "type": "object",
        "properties": {
            "team_id": {
                "type": "string",
                "description": "Determines the ID of the MLB team",
            },
            "season": {
                "type": "string",
                "description": "MLB season",
            }
        },
    },
)


get_find_game = FunctionDeclaration(
    name="get_find_game",
    description="Get detailed information about the MLB match schedules and game information, provides winner information,if the game was a tie, if it was a doubleHeader,if it was a tiebreaker, if it was a dayNight game,gamePk,gameGuid,gameDate, team information, score of the game,venue of the game, teams away record, teams home record",
    parameters={
        "type": "object",
        "properties": {
            "season": {
                "type": "string",
                "description": "Determines the season or the year the game was played",
            },
            "gamedate": {
                "type": "string",
                "description": "Date the game was played",
            },
            "team_id": {
                "type": "string",
                "description": "Id of the team",
            }

        },
    },
)

get_current_play = FunctionDeclaration(
    name="get_current_play",
    description="Get current play information about a game",
    parameters={
        "type": "object",
        "properties": {
            "season": {
                "type": "string",
                "description": "Determines the season or the year the game was played",
            },
            "gamedate": {
                "type": "string",
                "description": "Date the game was played",
            },
            "team_id": {
                "type": "string",
                "description": "Id of the team",
            }

        },
    },
)


get_mlb_clutch_moments = FunctionDeclaration(
    name="get_mlb_clutch_moments",
    description="Get detailed information about the MLB match or game data with game_pk or gamePk.That game data feed has a lot of detailed information about the game itself, the teams, the players, and what happened on every pitch. Below, we extract all the information on the current play from the game chosen above, to show all the information available for every pitch. This gives information about game type, doubleHeader,gamedayType,tiebreaker,calendarEventID,season,officialDate,dayNight,detailedState,team information,team records, player information,pitch data,startSpeed,endSpeed,strikeZoneBottom,strikeZoneTop,breaks,plateTime,ballColor,breakAngle,breakLength,breakVertical,breakVerticalInduced,breakHorizontal,spinRate,spinDirection",
    parameters={
        "type": "object",
        "properties": {
            "season": {
                "type": "string",
                "description": "Determines the season or the year the game was played",
            },
            "gamedate": {
                "type": "string",
                "description": "Date the game was played",
            },
            "team_id": {
                "type": "string",
                "description": "Id of the team",
            }

        },
     },

)
get_mlb_most_followed_teams = FunctionDeclaration(
    name="get_mlb_most_followed_teams",
    description="Retrieve information about most followed and most favorite teams in MLB or Major League Baseball. Summarise the response of the API and it gives the favorite team id for a user and favorite team ids for the user. Team ids can be found in the get_mlb_teams function call and name of the team will be retrieved from the get_mlb_teams API call ",
    parameters={
        "type": "object",
        "properties": {
            "season": {
                "type": "string",
                "description": "Season when the information is collected",
            }
        },
    },
)

get_mlb_user_video_watch = FunctionDeclaration(
    name="get_mlb_user_video_watch",
    description="Gets information about what users are watching on 2024-08-27 in the MLB season and what the most watched videos and headlines in an MLB game. It provides information about watched videos of a team, player and it provides headlines. This provides the source or the medium on which users were watching the games, this medium can be iOS, Android and Web",
    parameters={
        "type": "object",
        "properties": {
            "season": {
                "type": "string",
                "description": "Season when the information is collected",
            }
        },
    },
)
get_mlb_user_video_watch_sept15 = FunctionDeclaration(
    name="get_mlb_user_video_watch_sept15",
    description="Gets information about what users are watching on 2024-09-15 in the MLB season and what the most watched videos and headlines in an MLB game. It provides information about watched videos of a team, most watched player and it provides headlines. This provides the source or the medium on which users were watching the games, this medium can be iOS, Android and Web",
    parameters={
        "type": "object",
        "properties": {
            "season": {
                "type": "string",
                "description": "Season when the information is collected",
            }
        },
    },
)
get_standings = FunctionDeclaration(
    name="get_standings",
    description="This provides MLB team standings or the team records for a season. Details on league Record/wins,league Record/losses,league Record/ties,league Record/points,streakNumber,streak,divisionRank,leagueRank,leagueRecord,wins,losses,ties,home wins, home losses, away wins, away losses,division records wins,division records losses,division records ties,division records points,overall Records wins, overall Records losses, overall Records ties, overall Records points,league Records wins, league Records losses, league Records ties,league Records points,runs allowed,runs Scored,division Champ,split Records wins, split Records losses, split Records ties, split Records types, split Records points",
    parameters={
        "type": "object",
        "properties": {
            "leagueId": {
                "type": "string",
                "description": "Determines the league ID",
            },
            "season": {
                "type": "string",
                "description": "MLB season",
            }
        },
    },
)
get_mlb_attendance = FunctionDeclaration(
    name="get_mlb_attendance",
    description="This provides MLB game attendance, attendance year, openingsTotal,openingsTotalAway,openingsTotalHome,openingsTotalLost,gamesTotal,gamesAwayTotal,gamesHomeTotal,year,attendanceAverageAway,attendanceAverageHome,attendanceAverageYtd,attendanceHigh,attendance was highest,attendanceHighDate,attendanceLow,attendanceOpeningAverage,attendanceTotal,attendanceTotal,attendanceTotalAway,attendanceTotalHome",
    parameters={
        "type": "object",
        "properties": {
            "team_id": {
                "type": "string",
                "description": "Determines the league ID",
            },
            "season": {
                "type": "string",
                "description": "MLB season",
            }
        },
    },
)
get_player_image = FunctionDeclaration(
    name="get_player_image",
    description="This provides MLB players image based on the id of the player ",
    parameters={
        "type": "object",
        "properties": {
            "id": {
                "type": "string",
                "description": "This is the person id of the player",
            }
        },
    },
)


mlb_insights_tool = Tool(
    function_declarations=[
        get_mlb_leagues,
        get_mlb_seasons,
        get_mlb_teams,
        get_mlb_teams_by_season,
        get_mlb_teams_by_teamname_season,
        get_roster,
        get_find_game,
        get_mlb_clutch_moments,
        get_mlb_most_followed_teams,
        get_mlb_user_video_watch,
        get_standings,
        get_mlb_attendance,
        get_mlb_user_video_watch_sept15,
        get_player_image,
        get_current_play,
    ],
)

# API Functions with improved error handling
def fetch_mlb_data(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"API request failed: {str(e)}")
        return {"error": str(e)}

def get_mlb_leagues_from_api(content):
    url = f"https://statsapi.mlb.com/api/v1/league?sportId=1&season={content['season']}"
    return fetch_mlb_data(url)

def get_mlb_seasons_from_api(content):
    url = f"https://statsapi.mlb.com/api/v1/seasons/?sportId=1&season={content['season']}"
    return fetch_mlb_data(url)

def get_mlb_teams_from_api(content):
    url = f"https://statsapi.mlb.com/api/v1/teams?sportId=1"
    response = fetch_mlb_data(url)
    if 'teams' in response:
        for team in response['teams']:
            team_id = team["id"]
            team["teamurl"] = f"https://www.mlbstatic.com/team-logos/{team_id}.svg"
    return response

def get_mlb_teams_by_season_from_api(content):
    url = f"https://statsapi.mlb.com/api/v1/teams?sportId=1&season={content['season']}"
    response = fetch_mlb_data(url)
    if 'teams' in response:
        for team in response['teams']:
            team_id = team["id"]
            team["teamurl"] = f"https://www.mlbstatic.com/team-logos/{team_id}.svg"
    return response

def get_mlb_teams_by_teamname_season_from_api(content):
    url = f"https://statsapi.mlb.com/api/v1/teams/{content['team_id']}?sportId=1&season={content['season']}"
    return fetch_mlb_data(url)

def get_roster_from_api(content):
    url = f"https://statsapi.mlb.com/api/v1/teams/{content['team_id']}/roster/active?season={content['season']}"
    response = fetch_mlb_data(url)
    if 'roster' in response:
        for player in response['roster']:
            player_id = player["person"]["id"]
            player["playerurl"] = f"https://securea.mlb.com/mlb/images/players/head_shot/{player_id}.jpg"
    return response


def extract_season(gamedate):
    """
    Extract the season (year) from the game date
    Handles multiple date formats
    """
    date_formats = [
        '%Y-%m-%d',  # YYYY-MM-DD
        '%d-%m-%Y',  # DD-MM-YYYY
        '%m-%d-%Y',  # MM-DD-YYYY
        '%Y/%m/%d',  # YYYY/MM/DD
        '%d/%m/%Y',  # DD/MM/YYYY
        '%m/%d/%Y'   # MM/DD/YYYY
    ]
    
    for fmt in date_formats:
        try:
            date_obj = datetime.strptime(gamedate, fmt)
            return date_obj.year
        except ValueError:
            continue
    
    # If no format matches, try to extract year directly
    try:
        # Try extracting 4-digit year
        year = int(''.join(filter(str.isdigit, gamedate))[:4])
        if 1900 <= year <= datetime.now().year + 1:
            return year
    except (ValueError, TypeError):
        pass
    print(datetime.now().year)
    # If all else fails, return current year
    return datetime.now().year

def get_game_data(content):

    try:
        # Extract season and format date

        season = extract_season(content['gamedate'])
        
        url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&season={season}&types=regular&date={content['gamedate']}&teamIds={content['team_id']}"
        
        api_response = requests.get(url)
        api_response.raise_for_status()
        
        data = api_response.json()
        
        if 'totalGames' not in data or data['totalGames'] is None:
            return json.dumps({"error": "Invalid or missing 'totalGames' in API response."}, indent=2)
        
        if data['totalGames'] == 0:
            return json.dumps({"error": "No games found for the specified date and team."}, indent=2)
        
        if 'dates' not in data or not data['dates']:
            return json.dumps({"error": "Invalid or missing 'dates' in API response."}, indent=2)
        
        games = data['dates'][0]['games']
        if not games:
            return json.dumps({"error": "No games data found in API response."}, indent=2)
        
        gamePk = games[0]['gamePk']
        
        gameurl = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&season={season}&types=regular&date={content['gamedate']}&gamePk={gamePk}&hydrate=game(content(highlights(highlights)))"
        
        response = requests.get(gameurl)
        response.raise_for_status()
        data = response.json()
        
        if 'dates' not in data or not data['dates'] or 'games' not in data['dates'][0] or not data['dates'][0]['games']:
            return json.dumps({"error": "Invalid or missing game data in API response."}, indent=2)
        
        game_data = data['dates'][0]['games'][0]
        
        output = {
            "game_date": game_data.get('gameDate', 'Unknown'),
            "status": game_data.get('status', {}).get('detailedState', 'Unknown'),
            "teams": {
                "away": {
                    "name": game_data.get('teams', {}).get('away', {}).get('team', {}).get('name', 'Unknown'),
                    "score": game_data.get('teams', {}).get('away', {}).get('score', 'Unknown')
                },
                "home": {
                    "name": game_data.get('teams', {}).get('home', {}).get('team', {}).get('name', 'Unknown'),
                    "score": game_data.get('teams', {}).get('home', {}).get('score', 'Unknown')
                }
            },
            "highlights": []
        }
        
        if 'content' in game_data and 'highlights' in game_data['content']:
            highlights = game_data['content']['highlights']['highlights'].get('items', [])
            for highlight in highlights:
                highlight_data = {
                    "title": highlight.get('headline', 'Unknown'),
                    "id": highlight.get('id', 'Unknown'),
                    "video_url": next((p['url'] for p in highlight.get('playbacks', []) if p.get('name') == 'mp4Avc'), None)
                }
                output['highlights'].append(highlight_data)
        
        return json.dumps(output, indent=2)
    
    except ValueError as e:
        return json.dumps({"error": f"Date parsing error: {str(e)}"}, indent=2)
    except requests.exceptions.RequestException as e:
        return json.dumps({"error": f"An error occurred while fetching data: {str(e)}"}, indent=2)
    except KeyError as e:
        return json.dumps({"error": f"Missing expected data in API response: {str(e)}"}, indent=2)
    except Exception as e:
        return json.dumps({"error": f"An unexpected error occurred: {str(e)}"}, indent=2)

def get_game_highlights(content):

    season = extract_season(content['gamedate'])
    base_url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&season={season}&types=regular&date={content['gamedate']}&teamIds={content['team_id']}&hydrate=game(content(highlights(highlights)))"
    
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        data = response.json()
        
        games = data['dates'][0]['games']
        if not games:
            return json.dumps({"error": "No games data found in API response."}, indent=2)
        
        gamePk = games[0]['gamePk']

    except requests.RequestException as e:
        print(f"Error fetching game data: {e}")
        return None

    base_url = f"https://statsapi.mlb.com/api/v1.1/game/{gamePk}/feed/live"
    
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        print(f"Error fetching game data: {e}")
        return None

    highlights = {
        "game_info": {
            "gamePk": gamePk,
            "home_team": data["gameData"]["teams"]["home"]["name"],
            "away_team": data["gameData"]["teams"]["away"]["name"],
            "home_score": data["liveData"]["linescore"]["teams"]["home"]["runs"],
            "away_score": data["liveData"]["linescore"]["teams"]["away"]["runs"],
        },
        "key_plays": []
    }

    all_plays = data["liveData"]["plays"]["allPlays"]

    for play in all_plays:
        if is_key_play(play):
            play_data = extract_play_data(play)
            highlights["key_plays"].append(play_data)

    return highlights

def is_key_play(play):
    event = play["result"]["event"]
    return (event in ["Home Run", "Strikeout"] or
            play["about"]["isScoringPlay"] or
            "out" in event.lower())

def extract_play_data(play):
    result = play["result"]
    about = play["about"]
    matchup = play["matchup"]

    play_data = {
        "play_id": play["playEvents"][-1].get("playId", ""),
        "inning": about["inning"],
        "is_top_inning": about["isTopInning"],
        "event": result["event"],
        "description": result["description"],
        "is_scoring_play": about["isScoringPlay"],
        "batter": matchup["batter"]["fullName"],
        "pitcher": matchup["pitcher"]["fullName"],
        "pitch_data": extract_pitch_data(play["playEvents"][-1])
    }

    return play_data

def extract_pitch_data(pitch_event):
    if "pitchData" not in pitch_event:
        return {}

    pitch_data = pitch_event["pitchData"]
    return {
        "start_speed": pitch_data.get("startSpeed"),
        "end_speed": pitch_data.get("endSpeed"),
        "spin_rate": pitch_data.get("breaks", {}).get("spinRate"),
        "pitch_type": pitch_event.get("details", {}).get("type", {}).get("description")
    }

def get_video_highlights(game_id):
    url = f"https://statsapi.mlb.com/api/v1/game/{game_id}/content"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        print(f"Error fetching video highlights: {e}")
        return {}

    video_urls = {}
    for highlight in data.get("highlights", {}).get("highlights", {}).get("items", []):
        play_id = highlight.get("guid", "")
        video_url = next((p["url"] for p in highlight.get("playbacks", []) if p.get("name") == "mp4Avc"), None)
        if play_id and video_url:
            video_urls[play_id] = video_url

    return video_urls

def get_mlb_clutch_plays(content):
    highlights = get_game_highlights(content)
    if not highlights:
        return
    print(highlights)
    gamesPk = highlights['game_info']
    print(gamesPk['gamePk'])
    video_urls = get_video_highlights(gamesPk['gamePk'])

    for play in highlights["key_plays"]:
        play["video_url"] = video_urls.get(play["play_id"], "")

    print(highlights)
    return json.dumps(highlights, indent=2)



def get_find_game_from_api(content):
    url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&season={content['season']}&types=regular&date={content['gamedate']}&teamIds={content['team_id']}"
    data = fetch_mlb_data(url)
    
    if data.get('totalGames', 0) > 0:
        game_pk = data['dates'][0]['games'][0]['gamePk']
        game_url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&season={content['season']}&types=regular&date={content['gamedate']}&gamePk={game_pk}&hydrate=game(content(highlights(highlights)))"
        game_data = fetch_mlb_data(game_url)
        
        if 'dates' in game_data and game_data['dates']:
            game = game_data['dates'][0]['games'][0]
            output = {
                "game_date": game['gameDate'],
                "status": game['status']['detailedState'],
                "teams": {
                    "away": {
                        "name": game['teams']['away']['team']['name'],
                        "score": game['teams']['away']['score']
                    },
                    "home": {
                        "name": game['teams']['home']['team']['name'],
                        "score": game['teams']['home']['score']
                    }
                },
                "highlights": []
            }
            
            if 'content' in game and 'highlights' in game['content']:
                for highlight in game['content']['highlights']['highlights']['items']:
                    highlight_data = {
                        "title": highlight['headline'],
                        "video_url": next((p['url'] for p in highlight['playbacks'] if p['name'] == 'mp4Avc'), None)
                    }
                    output['highlights'].append(highlight_data)
            
            return output
    
    return {"error": "No game data found"}

def get_mlb_clutch_moments_from_api(content):
    url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&season={content['season']}&types=regular&date={content['gamedate']}&teamIds={content['team_id']}"
    return fetch_mlb_data(url)


def get_standings_from_api(content):
    url = f"https://statsapi.mlb.com/api/v1/standings?leagueId={content['leagueId']}&season={content['season']}"
    return fetch_mlb_data(url)

def get_current_play_from_api(content):

    url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&season={content['season']}&types=regular&date={content['gamedate']}&teamIds={content['team_id']}"

    data = fetch_mlb_data(url)
    
    if data.get('totalGames', 0) > 0:
        game_pk = data['dates'][0]['games'][0]['gamePk']

    gameurl = f"https://statsapi.mlb.com/api/v1.1/game/{game_pk}/feed/live"

    gamedata = fetch_mlb_data(gameurl)

    currentplay = gamedata['liveData']['plays']['currentPlay']

    return currentplay


api_function_map = {
    "get_mlb_leagues": get_mlb_leagues_from_api,
    "get_mlb_seasons": get_mlb_seasons_from_api,
    "get_mlb_teams": get_mlb_teams_from_api,
    "get_mlb_teams_by_season": get_mlb_teams_by_season_from_api,
    "get_roster": get_roster_from_api,
    "get_find_game": get_find_game_from_api,
    "get_current_play":get_current_play_from_api,
}

gemini_model = GenerativeModel(
    "gemini-2.0-flash-exp",
    generation_config=GenerationConfig(temperature=0),
    tools=[mlb_insights_tool],
)

chat = gemini_model.start_chat()

@app.route('/generate', methods=['GET'])
def process_mlb_query():
    user_query = request.args.get('query')
    if not user_query:
        return jsonify({"error": "No query provided"}), 400

    logger.info(f"Received query: {user_query}")
    enhanced_query = user_query + "\nProvide the API response in concise, high-level summary."

    try:
        model_response = chat.send_message(enhanced_query)
        
        function_call_in_progress = True
        while function_call_in_progress:
            function_call = model_response.candidates[0].content.parts[0].function_call
            print(function_call)
            if function_call and function_call.name in api_function_map:
                function_name = function_call.name
                function_params = {key: value for key, value in function_call.args.items()}
                
                logger.info(f"Calling function: {function_name}")
                api_response = api_function_map[function_name](function_params)
                
                model_response = chat.send_message(
                    Part.from_function_response(
                        name=function_name,
                        response={"content": json.dumps(api_response)},
                    ),
                )
            else:
                function_call_in_progress = False

        summary = model_response.text.replace("'\'", "").replace('``````', "")
        
        combined_response = {
            **api_response,
            "summary": summary
        }
        
        return jsonify(combined_response)
    
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        return jsonify({"error": "An error occurred while processing the query"}), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
