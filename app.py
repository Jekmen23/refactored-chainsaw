
from flask import Flask, request, render_template, session, redirect
import openai


OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY

app = Flask(__name__)
app.secret_key = "T.M"

class Message:
    def __init__(self, sender, content):
        self.sender = sender
        self.content = content

class Chatbot:
    def __init__(self):
        self.chat_history = []

    def get_prompt(self, user_input):
        return f"User: {user_input}\nChatbot: "

    def generate_response(self, prompt):
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            temperature=0.5,
            max_tokens=1000,
            top_p=1,
            frequency_penalty=0,
            stop=["\nUser: ", "\nChatbot: "]
        )
        return response.choices[0].text.strip()

    def append_to_chat_history(self, sender, content):
        message = Message(sender, content)
        self.chat_history.append(message)


chatbot = Chatbot()

@app.route("/")
def home():
    if 'username' in session:
        return render_template("chatbot.html", chat_history=chatbot.chat_history)
    return render_template("login.html")

@app.route("/chatbot_route", methods=["POST"])
def chatbot_route():
    user_input = request.form["message"]
    prompt = chatbot.get_prompt(user_input)
    bot_response = chatbot.generate_response(prompt)
    chatbot.append_to_chat_history("user", user_input)
    chatbot.append_to_chat_history("bot", bot_response)

    return render_template(
        "chatbot.html",
        chat_history=chatbot.chat_history
    )

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        session['username'] = email
        return redirect('/')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')

if __name__ == "__main__":
    app.run(debug=True)