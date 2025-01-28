import requests
import json
from flask import Flask,jsonify,request
import vertexai
import io
import os
from flask_cors import CORS
from datetime import datetime

PROJECT_ID =  os.environ.get('googleproject')
LOCATION = "us-central1"  # @param {type:"string"}

vertexai.init(project=PROJECT_ID, location=LOCATION)

app = Flask(__name__)
CORS(app,origins=["http://localhost:3000"])

from IPython.display import Markdown, display
import requests
from vertexai.generative_models import (
    FunctionDeclaration,
    GenerationConfig,
    GenerativeModel,
    Part,
    Tool,
)


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

get_mlb_team_roster = FunctionDeclaration(
    name="get_mlb_team_roster",
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
get_mlb_single_game_data = FunctionDeclaration(
    name="get_mlb_single_game_data",
    description="Get detailed information about the MLB match or game data with game_pk or gamePk.That game data feed has a lot of detailed information about the game itself, the teams, the players, and what happened on every pitch. Below, we extract all the information on the current play from the game chosen above, to show all the information available for every pitch. This gives information about game type, doubleHeader,gamedayType,tiebreaker,calendarEventID,season,officialDate,dayNight,detailedState,team information,team records, player information,pitch data,startSpeed,endSpeed,strikeZoneBottom,strikeZoneTop,breaks,plateTime,ballColor,breakAngle,breakLength,breakVertical,breakVerticalInduced,breakHorizontal,spinRate,spinDirection",
    parameters={
        "type": "object",
        "properties": {
            "game_pk": {
                "type": "string",
                "description": "Determines the unique ID for a game",
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
get_mlb_team_standings = FunctionDeclaration(
    name="get_mlb_team_standings",
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
        get_mlb_team_roster,
        get_find_game,
        get_mlb_single_game_data,
        get_mlb_most_followed_teams,
        get_mlb_user_video_watch,
        get_mlb_team_standings,
        get_mlb_attendance,
        get_mlb_user_video_watch_sept15,
        get_player_image,
    ],
)

def get_mlb_leagues_from_api(content):
    url = f"https://statsapi.mlb.com/api/v1/league?sportId=1&season={content['season']}"
    api_request = requests.get(url)
    print(api_request.text)
    return api_request.text
    
def get_mlb_seasons_from_api(content):
    url = f"https://statsapi.mlb.com/api/v1/seasons/?sportId=1&season={content['season']}"
    api_request = requests.get(url)
    return api_request.text
    
def get_mlb_teams_from_api(content):
    url = f"https://statsapi.mlb.com/api/v1/teams?sportId=1"
    api_response = requests.get(url)
    response=api_response.json()
    teams = response['teams']
    for res in teams:
       team_id = res["id"]
       res["teamurl"] = f"https://www.mlbstatic.com/team-logos/{team_id}.svg"
    
    modified_json_str = json.dumps(response) 
    return modified_json_str
    
def get_mlb_teams_by_season_from_api(content):
    url = f"https://statsapi.mlb.com/api/v1/teams?sportId=1&season={content['season']}"
    api_request = requests.get(url)
    print(api_request.json())
    return api_request.text
    
def get_mlb_team_roster_from_api(content):
    url = f"https://statsapi.mlb.com/api/v1/teams/{content['team_id']}/roster/active?season={content['season']}"
    api_response = requests.get(url)
    response=api_response.json()
    roster = response['roster']
    for res in roster:
       player_id = res["person"]["id"]
       res["playerurl"] = f"https://securea.mlb.com/mlb/images/players/head_shot/{player_id}.jpg"
    
    modified_json_str = json.dumps(response) 
    return modified_json_str
    
def get_find_game_from_api(content):
   
   
    url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&season={content['season']}&types=regular&date={content['gamedate']}&teamIds={content['team_id']}"
     
    api_response = requests.get(url)

    data = api_response.json()

    if data['totalGames'] > 0:
      games = data['dates'][0]['games']
      for game in games:
        gamelink = game['link']
    print(gamelink)
    gameurl = f"https://statsapi.mlb.com{game['link']}"
    print(gameurl)
    game_response = requests.get(gameurl)
    print(game_response.json()['liveData']['plays'])
    modified_json_str = json.dumps(game_response.json()['liveData']['plays']['allPlays']) 
    return  modified_json_str
    
def get_mlb_single_game_data_from_api(content):
    url = f"https://statsapi.mlb.com/api/v1.1/game/{content['game_pk']}/feed/live"
    api_response = requests.get(url)
    return api_response.text
    
def get_mlb_most_followed_teams_from_api(content):
    url = f"https://storage.googleapis.com/gcp-mlb-hackathon-2025/datasets/mlb-fan-content-interaction-data/2025-mlb-fan-favs-follows.json?season={content['season']}"
    api_response = requests.get(url)
    print(api_response.text)
    return api_response.text
    
def get_mlb_user_video_watch_from_api(content):
    url = f"https://storage.googleapis.com/gcp-mlb-hackathon-2025/datasets/mlb-fan-content-interaction-data/mlb-fan-content-interaction-data-000000000020.json?{content['season']}"
    api_response = requests.get(url)
    return api_response.text

def get_mlb_user_video_watch_sept15_from_api(content):
    url = f"https://storage.googleapis.com/gcp-mlb-hackathon-2025/datasets/mlb-fan-content-interaction-data/mlb-fan-content-interaction-data-000000000047.json?{content['season']}"
    api_response = requests.get(url)
    return api_response.text
    
def get_mlb_team_standings_from_api(content):
    url = f"https://statsapi.mlb.com/api/v1/standings?leagueId={content['leagueId']}&season={content['season']}"
    api_response = requests.get(url)
    return api_response.text

def get_mlb_attendance_from_api(content):
    url = f"https://statsapi.mlb.com/api/v1/attendance?teamId={content['team_id']}&season={content['season']}"
    api_response = requests.get(url)
    return api_response.text

def get_player_image_from_api(content):
    url = f"https://securea.mlb.com/mlb/images/players/head_shot/season={content['id']}.jpg"
    api_response = requests.get(url)
    return api_response


function_handler = {
    "get_mlb_leagues":get_mlb_leagues_from_api,
    "get_mlb_seasons":get_mlb_seasons_from_api,
    "get_mlb_teams": get_mlb_teams_from_api,
    "get_mlb_teams_by_season": get_mlb_teams_by_season_from_api,
    "get_mlb_team_roster": get_mlb_team_roster_from_api,
    "get_find_game":get_find_game_from_api,
    "get_mlb_single_game_data":get_mlb_single_game_data_from_api,
    "get_mlb_most_followed_teams":get_mlb_most_followed_teams_from_api,
    "get_mlb_user_video_watch":get_mlb_user_video_watch_from_api,
    "get_mlb_team_standings":get_mlb_team_standings_from_api,
    "get_mlb_attendance":get_mlb_attendance,
    "get_mlb_user_video_watch_sept15":get_mlb_user_video_watch_sept15_from_api,
    "get_player_image":get_player_image_from_api,
}

gemini_model = GenerativeModel(
    "gemini-2.0-flash-exp",
    generation_config=GenerationConfig(temperature=0),
    tools=[mlb_insights_tool],
)

chat = gemini_model.start_chat()

@app.route('/generate', methods=['GET'])
def send_chat_message():
    query = request.args.get('query')
    display(Markdown("#### Prompt"))
    print(query, "\n")
    query += """
    Provide the API response in concise, high-level summary.     """

    # Send a chat message to the Gemini API
    response = chat.send_message(query)
    print(response)

    # Handle cases with multiple chained function calls
    function_calling_in_process = True
    while function_calling_in_process:
        # Extract the function call response
        function_call = response.candidates[0].content.parts[0].function_call
        # Check for a function call or a natural language response
        if function_call is not None and function_call.name in function_handler.keys():
            # Extract the function call name
           
            function_name = function_call.name
            display(Markdown("#### Predicted function name"))

            # Extract the function call parameters
            params = {key: value for key, value in function_call.args.items()}
            display(Markdown("#### Predicted function parameters"))

            # Invoke a function that calls an external API
            function_api_response = function_handler[function_name](params)[
                :30000
            ]  # Stay within the input token limit

            # Send the API response back to Gemini, which will generate a natural language summary or another function call
            response = chat.send_message(
                Part.from_function_response(
                    name=function_name,
                    response={"content": function_api_response},
                ),
            )
        else:
            function_calling_in_process = False

    # Show the final natural language summary
    display(Markdown("#### Natural language response"))
    res1=response.text.replace("'\'", "")
    res2=res1.replace('```json', "")
    res3=res2.replace('```', "")

  
    json_response2 = function_api_response

    # Load JSON responses into dictionaries
    data1 = json.loads(json_response2)
  
    data2 = {"response":res3}
     
    # Combine dictionaries
    combined_data = {**data1, **data2}

    # Convert combined dictionary back to JSON
    combined_json = json.dumps(combined_data)
    
    return  combined_json
    
if __name__ == '__main__':
    app.run(debug=True)
