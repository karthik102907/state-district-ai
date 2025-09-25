from flask import Flask, render_template, request
import openai
import os

# Load your API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

def generate_state_district_info(state_name):
    prompt = (
        f"List all the districts in the Indian state of {state_name}. "
        f"For each district, provide a brief description mentioning major cities, economy, culture, or geography."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant knowledgeable about Indian geography."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        return response['choices'][0]['message']['content']
    
    except openai.error.OpenAIError as e:
        return f"An error occurred: {str(e)}"

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    if request.method == "POST":
        state = request.form["state"]
        result = generate_state_district_info(state)
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
