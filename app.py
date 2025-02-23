import flask
import openai

app = flask.Flask(__name__)

@app.route("/welcome")
def welcome():
    user = flask.request.args.get("user", "Guest")
    
    # Call OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": f"Welcome {user} to the stream! Keep the message under 350 characters."}]
    )

    # Get response text
    message = response["choices"][0]["message"]["content"]

    # Ensure it's under 350 characters
    message = message[:350]  # Trim if necessary

    return {"message": message}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
