import asyncio
import json
import os
import websockets
import requests
from google import genai
import base64

# Load API key from environment
os.environ['GOOGLE_API_KEY'] = ''
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

def get_find_game(content):
   
    url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&season={content['season']}&types=regular&date={content['gamedate']}&teamIds={content['team_id']}"
     
    api_response = requests.get(url)

    data = api_response.json()

    if data['totalGames'] > 0:
      games = data['dates'][0]['games']
      for game in games:
        gamePk = game['gamePk']
    print(gamePk)
    gameurl = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&season={content['season']}&types=regular&date={content['gamedate']}&gamePk={gamePk}&hydrate=game(content(highlights(highlights)))"
    try:
        response = requests.get(gameurl)
        response.raise_for_status()
        data = response.json()
        
        game_data = data['dates'][0]['games'][0]
        
        output = {
            "game_date": game_data['gameDate'],
            "status": game_data['status']['detailedState'],
            "teams": {
                "away": {
                    "name": game_data['teams']['away']['team']['name'],
                    "score": game_data['teams']['away']['score']
                },
                "home": {
                    "name": game_data['teams']['home']['team']['name'],
                    "score": game_data['teams']['home']['score']
                }
            },
            "highlights": []
        }
        
        if 'content' in game_data and 'highlights' in game_data['content']:
            highlights = game_data['content']['highlights']['highlights']['items']
            for highlight in highlights:
                highlight_data = {
                    "title": highlight['headline'],
                    "video_url": next((p['url'] for p in highlight['playbacks'] if p['name'] == 'mp4Avc'), None)
                }
                output['highlights'].append(highlight_data)
        
        return json.dumps(output, indent=2)
    
    except requests.exceptions.RequestException as e:
        return json.dumps({"error": f"An error occurred: {str(e)}"}, indent=2)


def get_mlb_attendance(season, team_id):
    return fetch_mlb_data(f"https://statsapi.mlb.com/api/v1/attendance?teamId={team_id}&season={season}")


def get_mlb_team_roster_stats(content):
    return fetch_mlb_data(f"http://statsapi.mlb.com/api/v1/teams/{content['team']}/roster/active?hydrate=person(education,draft,stats)/")


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
        ("get_mlb_roster", "Provides MLB team roster information", {"season": {"type": "STRING", "description": "Season for MLB"}, "team_id": {"type": "STRING", "description": "Team Id for MLB"}}),
        ("get_find_game", "Retrieves information and highlights about a game", {"season": {"type": "STRING", "description": "Season for MLB"}, "team_id": {"type": "STRING", "description": "Team Id for MLB"}, "gamedate": {"type": "STRING", "description": "Game Date for MLB game"}}),
    ]
]

function_handler = {
    "get_mlb_seasons": get_mlb_seasons,
    "get_mlb_leagues": get_mlb_leagues,
    "get_mlb_teams": get_mlb_teams,
    "get_mlb_roster": get_mlb_roster,
    "get_find_game": get_find_game,
    "get_mlb_attendance": get_mlb_attendance,
}

async def gemini_session_handler(client_websocket: websockets.WebSocketServerProtocol):
    try:
        config_message = await client_websocket.recv()
        config_data = json.loads(config_message)
        config = config_data.get("setup", {})
        config["tools"] = tools

        async with client.aio.live.connect(model=MODEL, config=config) as session:
            print("Connected to Gemini API")

            async def send_to_gemini():
                try:
                    async for message in client_websocket:
                        data = json.loads(message)
                        if "realtime_input" in data:
                            for chunk in data["realtime_input"]["media_chunks"]:
                                await session.send({"mime_type": chunk["mime_type"], "data": chunk["data"]})
                except Exception as e:
                    print(f"Error sending to Gemini: {e}")

            async def receive_from_gemini():
                try:
                    while True:
                        async for response in session.receive():
                            if response.server_content is None:
                                if response.tool_call is not None:
                                    function_calls = response.tool_call.function_calls
                                    function_responses = []

                                    for function_call in function_calls:
                                        name = function_call.name
                                        args = function_call.args
                                        call_id = function_call.id
                                        params = {key: value for key, value in args.items()}

                                        if name in function_handler:
                                            try:
                                                result = function_handler[name](params)
                                                function_responses.append({
                                                    "name": name,
                                                    "response": {"result": result},
                                                    "id": call_id
                                                })
                                                await client_websocket.send(json.dumps({"text": json.dumps(function_responses)}))
                                            except Exception as e:
                                                print(f"Error executing function: {e}")
                                                continue

                                    await session.send(function_responses)
                                    continue

                            model_turn = response.server_content.model_turn
                            if model_turn:
                                for part in model_turn.parts:
                                    if hasattr(part, 'text') and part.text is not None:
                                        await client_websocket.send(json.dumps({"text": part.text}))
                                    elif hasattr(part, 'inline_data') and part.inline_data is not None:
                                        base64_audio = base64.b64encode(part.inline_data.data).decode('utf-8')
                                        await client_websocket.send(json.dumps({"audio": base64_audio}))

                            if response.server_content.turn_complete:
                                print('\n<Turn complete>')
                except Exception as e:
                    print(f"Error receiving from Gemini: {e}")

            await asyncio.gather(
                asyncio.create_task(send_to_gemini()),
                asyncio.create_task(receive_from_gemini())
            )

    except Exception as e:
        print(f"Error in Gemini session: {e}")
    finally:
        print("Gemini session closed.")

async def main():
    async with websockets.serve(gemini_session_handler, "localhost", 9082):
        print("Running websocket server localhost:9082...")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
