from flask import Flask,render_template,redirect,url_for,request,Response,jsonify
import google.generativeai as genai
from flask_cors import CORS

API_KEY = 'AIzaSyDqDhf-M7C97tdCSE4yEQE0fbQyqfDjJBQ'

genai.configure(api_key=API_KEY)
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)
chat_session = model.start_chat(history=[])


app=Flask(__name__)

CORS(app,resources={r"/*": {"origins": "*"}})

def gemini_api(query):
    response = chat_session.send_message(f"{query}")
    #print(response)
    
    # Extract the text parts from the response
    text_parts = []
    candidates = response.candidates
    
    for candidate in candidates:
        content = candidate.content
        
        for part in content.parts:
            text = part.text
            cleaned_text = text.replace('\n', ' ').replace('[', '').replace(']', '').replace('**', '').strip('"')
            text_parts.append(cleaned_text)
    
    # Join all text parts into a single string
    return ' '.join(text_parts)

@app.route('/')
def main():
    return "<h1>api working properly</h1>"


@app.route('/query-response', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        query=request.json
        query = query.get('query', '')
        print(query)
        #query='army'
        if query:
            response = gemini_api(query)
            print(response)
            return jsonify({"response": response})
        else:
            return jsonify({"response": "No query provided"})
    
    return jsonify({"response": "Please enter a query using POST method"})



if __name__=="__main__":
    app.run(debug=True,host='0.0.0.0')