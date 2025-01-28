import requests
import json
from google.cloud import aiplatform
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value
import vertexai
from flask_cors import CORS
from flask import Flask,jsonify,request
from vertexai.generative_models import GenerativeModel, Part

app = Flask(__name__)
CORS(app,origins=["http://localhost:3100"])

@app.route('/generateVideoSummary', methods=['GET'])
def summarize_video():
    
    aiplatform.init(project="", location="")
    query = request.args.get('query')


    model = GenerativeModel("gemini-2.0-flash-exp")

    prompt = """
    Provide a detailed description of the video. Show scores, player statsitics
     """

    video_file = Part.from_uri(
    uri=query,
    mime_type="video/mp4",
    )

    contents = [video_file, prompt]

    response = model.generate_content(contents)
    print(response.text)
    
    return response.text

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5100)
    