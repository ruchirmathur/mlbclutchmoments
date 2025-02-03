# MLB Clutch Moments

## Installation instructions on local

### Pre-Requisites
* Create a Google Cloud account
* Create a Google Cloud project
* Enable 

* git clone https://github.com/ruchirmathur/mlbfanexperience.git
* Two folders will be available
   * Backend
   * Frontend
 * Navigate to Backend folder
   * Navigate to mlbfanexperience\backend\audio folder and open main.py file. Update the "api_key" with the API key for using the Gemini Model.
   * Navigate to mlbfanexperience\backend\web folder and open main.py file. Update the project and location in this file.
   * Navigate to mlbfanexperience\backend\video folder and open main.py file. Update the project and location in this file
  

## What it does
This project revolutionizes MLB information access through dual search interfaces:
###Audio search: 
Users can issue voice commands to retrieve up-to-date MLB data. Gemini Flash 2.0's advanced audio processing capabilities interpret these commands accurately.
#### Supported Use Cases
* League Information
* Season Information
* Team Information
* Player Information
* Game Information

#### Web search: 
Features an auto-complete search function for quick and easy information retrieval

Both interfaces tap into the MLB Stats API, ensuring real-time, accurate data on leagues, seasons, teams, rosters, and games51. Gemini Flash 2.0's function calling capabilities seamlessly integrate this data, presenting it to users in a clear, accessible format.

The system provides:
* Live game updates, including pitch-by-pitch information5
* Comprehensive player and team statistics
* Historical data for in-depth analysis
* Real-time scores and match progress
* This innovative approach makes MLB information readily available to all fans, including those with visual impairments, enhancing the baseball experience for everyone

## How we built it ##
### Technologies used ###

* Gemini Multi Modal API
* Gemini 2.0 Flash 2.0 Exp
* Vertex Generative AI SDK
* Google Gen AI SDKs
* React
* Google Material Design
* Python
* Flask
* Websockets

## Technology Architecture ##
![image](https://ff29e3e79b2ad7794861a42b431d19ae1fb7332655782894df71b59-apidata.googleusercontent.com/download/storage/v1/b/baseballfan/o/Untitled%20Diagram.png?jk=AXN3i9p86S1sVnH7tCZYU1PL4LtmLCMqmJIXHWYvYtb0Bl02w97_IBSMlcknT9-5zD-1sP9Ta_L0TSVS8dQvUzaEE0Ab6yz8x6ea669FDmbAIcdtK8w_oTqJM3LK58lM6HFyvB14c4X_qsCy6NXHj9wDd_251e1-0WB1ElPWqHFfUaCBGV0uN_1lmEefZH2mr2AnWuA11JwEZyWv1VgPDDnSla4nm8wTUkS7S3PnTikhXKQvF-5xyiRV03EVr_yOPFVVVul5xpmwD7vHJC0cpEjUZWCR5xe7UCY5auDpn-NHN5oMxUGyqlGcKg-F0RMU-1Nmp2lavi-9IjTqF9kPA7Ge_yLDycyPJVFgl0PT6p4Q0A2UZfINIcIqy-W4n1TnbHGfqTfaGTd3BzTblN_5Qk92poUQkCCuqLMl7yo9ma2_RKdoIFlxhrTWEwNNn927Azd8qx_y7g8ByCcw6uVXt9lJYl3o4hEwsj1Fan3mu8O4eJawnDSfhMQc-9vGnZFxNzY9nw1V6rMOi_DWncCtK4uKSmFs2wDdBIeGYUV8XBHMMtQ-De-1ngG-ReqCIHbH3Td_P4vyAJcr5RUcX7BWDG-XB58C0lh8zz78M0xUmVDyHZka_KeN5ftorPt-LgfMpDsTs4LGMZsE6ybWgSloqNbEIs1mENoCMvaadVNAwQZacj_Ky00A_9KjLShDR0z_thLHTy72QiCo0785wEjk1cTrb-BXMdtMgCZ5tEb2MW3sFjPwxC1ckGju3v0lMQbRAHcTAJrD0MKEUskcFsTMw2ZsXggvYv-_yMQgsXYuwucY4z0S8ntHonvK2tLBm8CixFG5w6pr2nW3kEklTSZotb-4uH6NVxgHiuMHqVtEQhhoK0Bw7SYw4zDtaDiv3Ps1L1XSmRIfUD8W6l0nFs4gnj7ALrpy6ReeYXO5-3R0gTPwn-CTz_UEb7VLlOvzLM6BwkLfA1V7rnPR1Zoe7iuuDeItGdPWvWesWngnLgbkC9jq0WlyY41aM7Mzwj8BkqR9vqjreKfkV65e91mYGarZcyY0VE_NVN0ocRgiL06QWRrS3AQMAlwUfaDn5JoohOXhP_oQQo_0a6cGY8RsXhqpFZ6sWyFMkARg9S9FtXGT9oCtrhREhdLm2KK3Klij&isca=1)


###Frontend Architecture###

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
