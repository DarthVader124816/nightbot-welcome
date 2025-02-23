from flask import Flask, request, jsonify
import openai
import os
import threading
import time

app = Flask(__name__)

# Get OpenAI API key from Replit secrets
openai.api_key = os.getenv("OPENAI_API_KEY")

FIRST_TIME_USERS_FILE = "users.txt"

# Function to check if a user is new
def is_first_time_user(username):
    if not os.path.exists(FIRST_TIME_USERS_FILE):
        open(FIRST_TIME_USERS_FILE, "w").close()

    with open(FIRST_TIME_USERS_FILE, "r") as file:
        users = file.read().splitlines()

    if username in users:
        return False  

    with open(FIRST_TIME_USERS_FILE, "a") as file:
        file.write(username + "\n")
    return True  

# Route to welcome new users
@app.route('/welcome', methods=['GET'])
def welcome():
    username = request.args.get('user', 'guest')

    if not is_first_time_user(username):
        return jsonify({"message": "Returning user, no welcome message."})

    prompt = f"Create a friendly, fun welcome message for {username} joining a Twitch stream for the first time."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",  # Use "gpt-4-turbo" or "gpt-3.5-turbo" for cost efficiency
            messages=[{"role": "system", "content": "You are a friendly chatbot welcoming new Twitch viewers."},
                      {"role": "user", "content": prompt}]
        )
        message = response["choices"][0]["message"]["content"]
        return jsonify({"message": message})
    except Exception as e:
        return jsonify({"error": str(e)})

# Function to reset users.txt after the stream ends (automatically clears after 6 hours)
def reset_users_file():
    time.sleep(6 * 3600)  # Adjust this based on your stream duration (6 hours = 6 * 3600 seconds)
    if os.path.exists(FIRST_TIME_USERS_FILE):
        os.remove(FIRST_TIME_USERS_FILE)
        print("User data reset after stream ended!")

# Start the reset timer in a separate thread
threading.Thread(target=reset_users_file, daemon=True).start()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
