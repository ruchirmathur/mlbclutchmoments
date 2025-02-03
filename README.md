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

* Download the source code, git clone https://github.com/ruchirmathur/mlbfanexperience.git
* After the download, Two folders will be available
   * Backend
   * Frontend
 * Backend Local Deployment
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
* Frontend Local Deployment
* Navigate to Frontend folder
   * Navigate to the mlbclutchmoments\frontend\baseballfan\src\components folder and open SearchResults.tsx file. Update the hostname as the host name of server where the video API is hosted.
   * Navigate to the mlbclutchmoments\frontend\baseballfan\src\pages folder and open Audio.js file. Update the  WS_URL as the hostname for the Audio API for Websockets. It should be in the format ws://hostname:port/ws
   * Navigate to the mlbclutchmoments\frontend\baseballfan\src\pages folder and open Web.tsx. Update the host for Web API endpoint.
   * Run npm install
   * Run npm start
   * Access the MLB Clutch Moments app by accessing http://localhost:3000
        
## What it does
This project revolutionizes MLB information access through dual search interfaces:
### Audio search: 
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
![image](https://ff442e86fef6c9019a67136c8aa8e71f0ecfc974162199da7d2c6b0-apidata.googleusercontent.com/download/storage/v1/b/baseballfan/o/Untitled%20Diagram.png?jk=AXN3i9qyciudaroue3o-9GDc4Rn7VryuINQNwMG2MX1CU_i2Y2TTEQXVBqBp92aVM3R4O7PyUFTUhEcbcVfApLl5kwclxFw80kVuS3UayNZq7pZ2l7TgrSAzmczdCUb4lRZ_oNKy7LcFYGCIihDOzlS-moOyLywdfYbLFHFVYuWucfaBtULe3MEU5JzLmzEX_rhXVT5WOzhT6stpmNXX9CYLEWOTjDrx2XDgi5OSPp4ARMBO4j4dzAV5ABoaB89cpY40e5mQNZwHg1lXzBQUVIZGdMhhJVvaP-WRBeUGATA6WBK8SYaIHOH07YiazB2wPPK1BucBXbIJJRRXRPlReqEMdmqs6jWAenHayEMRw30SbzmtlsAj1pmJFSqEMoqyqDZcPQUOro8B82ywvNwPo5MfTs_ebJkwLLYSLHQGV6zxV1GeNzjlPzgcI_mFPOZ7BuYsJP5SHOK1XjR-ri5sqLXYkj0n7idXfj4AdSWk8p-ERT0AYTd9aA4u08ZxhadG4r-TxKsGEiuIEnfMHnTEynaV7RVR8WDgPOgxW4jRMElIRJEBHhmI194x4SVPY52oP6OOzWiUAjc4h4atQ7APr1XeO1H2N1zgiN5tt9FsUM_2hYee-bolnh0p348-8CC7Mt46CWi4IT6C84yiIju5y2GJGtPBk2KUbW0HrGBVw50C6Tpsriv0N_2KrJOtBseRnbtMyMASCseuYv1iMh5cxarGesnWd8cSsUYfbnztyNOME5SO34O1XPKnxgW0mgmT3bLn4zazN1f5zcToSvIoZ_zgWFW4SdCEA_jBf7tXf1xiiV10sa2s-a1i32D577-lKEYtQtFOfRg_qtoJOLlL4tVILz2DfJDIHnN0RreTi-TU30HthROiD1nmFPiWX4IQgbr3eYnPL3fMESFD2TcjQ1DltTDgdyxk_XVxPls7Tao5UGssI73s_e_oalnfFBCEJsL3rSMaRJfgADmlio_vVi1VuNz2BgKNMNvr86fCu_IP67DJLjU99EicMSIbOJ1soWRjDYs3rWTZKKpeywnthXMSDX8tJ3LYdsbzZF1Eg67jyGaCkRA899qX4fbAQjmkkPyqV5MiThSiJUT8Zdig76GM6NxyY8zBW0lGkiiAcEfokrwHuXi3j7grBXO75W4&isca=1)


### Frontend Architecture

* **Frameworks** - 
     * **React** - Frontend of the MLB clutch moments application is built using React.
     * **Google Material** - Front end design is powered by Google Material provide a rich user experience
* **Deployment** -  Google Cloud Run is used for deployment of the React application  

### Backend Architecture

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
