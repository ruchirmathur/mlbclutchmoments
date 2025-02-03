# MLB Clutch Moments

## What it does
This project revolutionizes MLB information access through dual search interfaces:
###Audio search: 
Users can issue voice commands to retrieve up-to-date MLB data. Gemini Flash 2.0's advanced audio processing capabilities interpret these commands accurately.
#### Supported Use Cases ####
* League Information
* Season Information
* Team Information
* Player Information
* Game Information

###Web search: 
Features an auto-complete search function for quick and easy information retrieval

Both interfaces tap into the MLB Stats API, ensuring real-time, accurate data on leagues, seasons, teams, rosters, and games51. Gemini Flash 2.0's function calling capabilities seamlessly integrate this data, presenting it to users in a clear, accessible format.

The system provides:
* Live game updates, including pitch-by-pitch information5
* Comprehensive player and team statistics
* Historical data for in-depth analysis
* Real-time scores and match progress
* This innovative approach makes MLB information readily available to all fans, including those with visual impairments, enhancing the baseball experience for everyone

## How we built it
### Technologies used

* Gemini Multi Modal API
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

###Frontend Architecture

* **Frameworks** - 
     * **React** - Frontend of the MLB clutch moments application is built using React.
     * **Google Material** - Front end design is powered by Google Material provide a rich user experience
* **Deployment** -  Google Cloud Run is used for deployment of the React application  

###Backend Architecture

* **Frameworks** - 
     * **Python** - Used Python to build the API's for the MLB Clutch App
     * **Flask** - Flask was used some of the API end points
     * **Websockets** - Used Websockets to enable Audio communication
     * **Google Gen AI SDK** - Used Gen AI SDK for Audio capabilities
     * **Vertex Generative AI SDK**- Used the Gemini SDK to enable Generative AI capabilities for the Web and Video summarization

* **API** - There are 3 API end points exposed as part of the backend.

     * **Audio API** - This API end point is hosted as a websocket server. This websocket server receives audio input. Audio input is converted into text and it is used to find out the function that needs to be called.
         * This API sends the audio output back and supports the following MLB Data.
             * Seasons
             * Leagues
             * Teams
             * Players
             * Games

     * **Video API** - This API end point is hosted as a Flask API. This API accepts a video url and provides a summary of the video.

     * **Web API** - This API end point is hosted as a flask API. This API receives text input from the web. Text is analyzed and an appropriate function to be called is identified. Based on the function identified, MLB data is received.
         * This API supports the following MLB Data.
             * Seasons
             * Leagues
             * Teams
             * Players
             * Games

* **Deployment** - API's are deployed on Google Cloud Run.
