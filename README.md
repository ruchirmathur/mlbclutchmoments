# MLB Clutch Moments

## Installation instructions on local

### Pre-Requisites
* Create a Google Cloud account
* Create a Google Cloud project for the Google Cloud Account and make sure that billing is enabled
* Enable Gemini Vertex AI API by navigating to Vertex AI on Google Cloud Console
* Install and initialize the Google Cloud CLI
* To authenticate, run command gcloud auth application-default login
* Make appropriate selections of the Google Cloud Project and other information asked by the prompt
* Go to https://aistudio.google.com/, get API keys that can be used to enable the audio use cases

### Installation  

* Download the source code, git clone https://github.com/ruchirmathur/mlbclutchmoments.git
* After the download, Two folders will be available
   * Backend
   * Frontend
 * #### Backend Local Deployment
   * Navigate to Backend folder
   * Navigate to mlbclutchmoments\backend\audio folder and open main.py file.
      * Update the "api_key" with the API key for using the Gemini Model. This API key should be available in the Google AI studio.
      * Run this by executing the command, python main.py
   * Navigate to mlbclutchmoments\backend\web folder and open main.py file. Update the project and location in this file.
      * Update the Project and location in this line, aiplatform.init(project="", location="") 
      * Update the CORS setting to point to the local host for the React application. e.g CORS(app,origins=["http://localhost:3000"])
      * Run this by executing the command, python main.py
   * Navigate to mlbclutchmoments\backend\video folder and open main.py file. Update the project and location in this file
     * Update the Project and location in the below line
            PROJECT_ID = ""  # @param {type:"string"}
            LOCATION = ""  # @param {type:"string"}
      * Update the CORS setting to point to the local host for the React application. e.g CORS(app,origins=["http://localhost:3000"])
      * Run this by executing the command, python main.py
* #### Frontend Deployment
   * Navigate to Frontend folder
     * Navigate to the mlbclutchmoments\frontend\baseballfan\src\components folder and open SearchResults.tsx file. Update the hostname as the host name of server where the video API is hosted.
     * Navigate to the mlbclutchmoments\frontend\baseballfan\src\pages folder and open Audio.js file. Update the  WS_URL as the hostname for the Audio API for Websockets. It should be in the format ws://hostname:port/ws
     * Navigate to the mlbclutchmoments\frontend\baseballfan\src\pages folder and open Web.tsx. Update the host for Web API endpoint.
     * Run npm install
     * Run npm start
     * Access the MLB Clutch Moments app by accessing http://localhost:3000
    
## Access Information
React application will be available at
  * Audio - http://localhost:3000
  * Web - http://localhost:3000/web
        

## What it does
This project revolutionizes MLB information access through dual search interfaces:
###Audio search: 
Users can issue voice commands to retrieve up-to-date MLB data in audio. Gemini Flash 2.0's advanced audio processing capabilities interpret these commands accurately and provide real time MLB data back in the form of audio to the fans.

![Audio Search](https://storage.cloud.google.com/baseballfan/audio.png)

Audio search gets its data from the MLB Stats API, ensuring real-time, accurate data on MLB leagues, seasons, teams, rosters, and games. Gemini Flash 2.0's function calling capabilities seamlessly integrate this data, presenting it to users in a clear, accessible format. 

The system provides:
* Live game data and Clutch Plays
* Comprehensive player and team data
* MLB League and Season data
* Historical data for in-depth analysis
* Team Standings
* This innovative approach makes MLB information readily available to all fans, including those with visual impairments, enhancing the baseball experience for everyone.


## How we built it
### Technologies used

* Gemini Multi Modal Live API
* Gemini 2.0 Flash 2.0 Exp
* Vertex Generative AI SDK
* Google Gen AI SDKs
* React
* Google Material Design
* Python
* Flask
* Websockets

## Technology Architecture
![Architecture](https://storage.cloud.google.com/baseballfan/Untitled%20Diagram.png)

Note - Web and Video capabilities have been added in the 2nd iteration.

### Frontend Architecture

* **Frameworks** - 
     * **React** - Frontend of the MLB clutch moments application is built using React.
     * **Google Material** - Front end design is powered by Google Material provide a rich user experience
* **Deployment** -  Google Cloud Run is used for deployment of the React application  

###Backend Architecture

* **Frameworks** - 
     * **Python** - Used Python to build the API's for the MLB Clutch App
     * **Flask** - Flask was used some of the API end points
     * **Websockets** - Used Websockets to enable Audio communication
     * **Google Gen AI SDK** - Used Gen AI SDK for enabling Audio capabilities and function calling
     * **Vertex Generative AI SDK**- Used the Gemini SDK to enable Generative AI capabilities for the Web and Video summarization

     * **Audio Websocket server** - This Websocket server is hosted on Google Cloud Run. This websocket server receives audio input. Audio input is converted into text and it is used to find out the function that needs to be called. Gemini is able to accurately identify the function and it is able to retrieve the MLB data that the user is looking for. Different functions within the websocket server connect to different MLB stats API's to get the information need to power the MLB use cases. 
         * This server sends the audio output back and supports the following MLB Data.
             * **Seasons**
              * API used - https://statsapi.mlb.com/api/v1/seasons/{season}?sportId=1
             * **Leagues**
               * API used - https://statsapi.mlb.com/api/v1/league?sportId=1&season={season}
             * **Teams**
               * API used - https://statsapi.mlb.com/api/v1/teams?sportId=1&season={season}
             * **Players**
               * API used - https://statsapi.mlb.com/api/v1/teams/{team_id}/roster/active?season={season}
             * **Games**
                - https://statsapi.mlb.com/api/v1/schedule?sportId=1&season={season}&types=regular&date={gamedate}&teamIds={team_id}
                - https://statsapi.mlb.com/api/v1/schedule?sportId=1&season={season}&types=regular&date={gamedate}&gamePk={Game ID}&hydrate=game(content(highlights(highlights)))
               * https://statsapi.mlb.com/api/v1.1/game/{Game Id}/feed/live
             * **Team Standings**
                * API used - https://statsapi.mlb.com/api/v1/standings?leagueId={League_id'}&season={Season}



     * **Video API** - This API end point is hosted as a Flask API. This API accepts a video url and provides a summary of the video. This is built in the 2nd iteration of this app.

     * **Web API** - This API end point is hosted as a flask API. This API receives text input from the web. Text is analyzed and an appropriate function to be called is identified. Based on the function identified by Gemini, MLB data is retrieved from the MLB statsapi . This is built in the 2nd iteration of this app.
         * This API supports the following MLB Data.
             * Seasons
             * Leagues
             * Teams
             * Players
             * Games

* **Deployment** - API's are deployed on Google Cloud Run.

