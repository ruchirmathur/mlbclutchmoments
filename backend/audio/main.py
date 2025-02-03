import asyncio
import json
import os
import websockets
import requests
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from google import genai
import base64
import uvicorn
from datetime import datetime
import re


MODEL = "gemini-2.0-flash-exp"

client = genai.Client(
    api_key='',
    http_options={'api_version': 'v1alpha'}
)

def fetch_mlb_data(url):
    response = requests.get(url)
    return response.text

def get_mlb_seasons(content):
    return fetch_mlb_data(f"https://statsapi.mlb.com/api/v1/seasons/{content['season']}?sportId=1")

def get_mlb_leagues(season):
    return fetch_mlb_data(f"https://statsapi.mlb.com/api/v1/league?sportId=1&season={season['season']}")

def get_mlb_teams(season):
    return fetch_mlb_data(f"https://statsapi.mlb.com/api/v1/teams?sportId=1&season={season['season']}")

def get_mlb_roster(content):
    return fetch_mlb_data(f"https://statsapi.mlb.com/api/v1/teams/{content['team_id']}/roster/active?season={content['season']}")

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


def get_mlb_attendance(season, team_id):
    return fetch_mlb_data(f"https://statsapi.mlb.com/api/v1/attendance?teamId={team_id}&season={season}")


def get_mlb_team_roster_stats(content):
    return fetch_mlb_data(f"http://statsapi.mlb.com/api/v1/teams/{content['team']}/roster/active?hydrate=person(education,draft,stats)/")


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
    gamesPk = highlights['game_info']
    video_urls = get_video_highlights(gamesPk['gamePk'])

    for play in highlights["key_plays"]:
        play["video_url"] = video_urls.get(play["play_id"], "")

    return json.dumps(highlights, indent=2)

def get_current_play(content):
    season = extract_season(content['gamedate'])

    url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&season={season}&types=regular&date={content['gamedate']}&teamIds={content['team_id']}"

    api_response = requests.get(url)

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
        
    game_pk = games[0]['gamePk']

    gameurl = f"https://statsapi.mlb.com/api/v1.1/game/{game_pk}/feed/live"

    game_api_response = requests.get(gameurl)

    gamedata = game_api_response.json()

    currentplay = gamedata['liveData']['plays']['currentPlay']

    return json.dumps(currentplay, indent=2)


# Define tools (functions)
tools = [
    {
        "function_declarations": [
            {
                "name": func_name,
                "description": func_desc,
                "parameters": {
                    "type": "OBJECT",
                    "properties": func_props,
                    "required": list(func_props.keys())
                }
            }
        ]
    } for func_name, func_desc, func_props in [
        ("get_mlb_seasons", "Provides detailed information about MLB seasons", {"season": {"type": "STRING", "description": "Season for MLB"}}),
        ("get_mlb_leagues", "Provides detailed information about MLB leagues", {"season": {"type": "STRING", "description": "Season for MLB"}}),
        ("get_mlb_teams", "Retrieves all MLB teams for a season", {"season": {"type": "STRING", "description": "Season for MLB"}}),
        ("get_mlb_roster", "Provides MLB team roster information,Retrieve the team_id from get_mlb_teams API, please do not ask the user to provide you the team_id. If you know the get_mlb_teams API then get the data proactively", {"season": {"type": "STRING", "description": "Season for MLB"}, "team_id": {"type": "STRING", "description": "Team Id for MLB"}}),
        ("get_game_data", "Retrieves information and highlights about a game. Use game date in YYYY-MM-DD format.", {"team_id": {"type": "STRING", "description": "Team Id for MLB"}, "gamedate": {"type": "STRING", "description": "Game Date for MLB game"}}),
        ("get_mlb_clutch_plays", "Get the Clutch Plays for a MLB game. Use game date in YYYY-MM-DD format", {"team_id": {"type": "STRING", "description": "Team Id for MLB"}, "gamedate": {"type": "STRING", "description": "Game Date for MLB game"}}),
        ("get_current_play", "Get the Current Plays for a MLB game. Use game date in YYYY-MM-DD format", {"team_id": {"type": "STRING", "description": "Team Id for MLB"}, "gamedate": {"type": "STRING", "description": "Game Date for MLB game"}}),
    ]
]

function_handler = {
    "get_mlb_seasons": get_mlb_seasons,
    "get_mlb_leagues": get_mlb_leagues,
    "get_mlb_teams": get_mlb_teams,
    "get_mlb_roster": get_mlb_roster,
    "get_game_data": get_game_data,
    "get_mlb_clutch_plays": get_mlb_clutch_plays,
    "get_current_play": get_current_play,
}

app = FastAPI()

@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.websocket("/ws")
async def gemini_session_handler(websocket: WebSocket):
    await websocket.accept()
    try:
        config_message = await websocket.receive_text()
        config_data = json.loads(config_message)
        config = config_data.get("setup", {})
        
        config["tools"] = tools
        
        async with client.aio.live.connect(model=MODEL, config=config) as session:
            print("Connected to Gemini API")

            async def send_to_gemini():
                try:
                    while True:
                        message = await websocket.receive_text()
                        data = json.loads(message)
                        
                        if "realtime_input" in data:
                            for chunk in data["realtime_input"]["media_chunks"]:
                                if chunk["mime_type"] == "audio/pcm":
                                    await session.send({"mime_type": "audio/pcm", "data": chunk["data"]})
                                elif chunk["mime_type"] == "image/jpeg":
                                    await session.send({"mime_type": "image/jpeg", "data": chunk["data"]})
                except WebSocketDisconnect:
                    print("Client connection closed (send)")

            async def receive_from_gemini():
                try:
                    while True:
                        async for response in session.receive():
                            if response.server_content is None:
                                if response.tool_call is not None:
                                    print(f"Tool call received: {response.tool_call}")
                                    function_calls = response.tool_call.function_calls
                                    function_responses = []

                                    for function_call in function_calls:
                                        name = function_call.name
                                        args = function_call.args
                                        call_id = function_call.id
                                        params = {key: value for key, value in args.items()}
                                        print(params)
                                        
                                        if name in function_handler:
                                            try:
                                                result = function_handler[name](params)
                                                function_responses.append({
                                                    "name": name,
                                                    "response": {"result": result},
                                                    "id": call_id  
                                                })
                                               
                                                await websocket.send_text(json.dumps({"text": json.dumps(function_responses)}))
                                                print("Function executed")
                                            except Exception as e:
                                                print(f"Error executing function: {e}")
                                                continue

                                    await session.send(function_responses)
                                    continue

                            model_turn = response.server_content.model_turn
                            if model_turn:
                                for part in model_turn.parts:
                                    if hasattr(part, 'text') and part.text is not None:
                                        await websocket.send_text(json.dumps({"text": part.text}))
                                    elif hasattr(part, 'inline_data') and part.inline_data is not None:
                                        base64_audio = base64.b64encode(part.inline_data.data).decode('utf-8')
                                        await websocket.send_text(json.dumps({
                                            "audio": base64_audio,
                                        }))
                                        print("audio received")

                            if response.server_content.turn_complete:
                                print('\n<Turn complete>')
                except WebSocketDisconnect:
                    print("Client connection closed (receive)")

            await asyncio.gather(send_to_gemini(), receive_from_gemini())

    except WebSocketDisconnect:
        print("WebSocket disconnected")
    except Exception as e:
        print(f"Error in Gemini session: {e}")
    finally:
        print("Gemini session closed.")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)