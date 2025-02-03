import requests
import json
import os
from google.cloud import aiplatform
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value
import vertexai
from flask_cors import CORS
from flask import Flask,jsonify,request
from vertexai.generative_models import GenerativeModel, Part

app = Flask(__name__)
CORS(app,origins=[""])

@app.route('/generateVideoSummary', methods=['GET'])
def summarize_video():
    
    aiplatform.init(project="", location="")
    query = request.args.get('query')

    print(query)
    model = GenerativeModel("gemini-2.0-flash-exp")

    prompt = """
    Provide a detailed description of the video and structure in bullet points. Show scores, player statsitics in a nice html table that can be rendered easily.
     """

    video_file = Part.from_uri(
    uri=query,
    mime_type="video/mp4",
    )

    contents = [video_file, prompt]

    response = model.generate_content(contents)
    # Create a dictionary with the summary
    structured_data = {
    "summary": response.text
    }

    # Convert to JSON
    json_response = json.dumps(structured_data, indent=2)

    return json_response

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
    