from flask import Flask, jsonify, redirect

import os
import requests

app = Flask(__name__)
app.config["DEBUG"] = False

@app.route('/')
def index():
    return redirect('https://basically.email/discord')

@app.route('/banner/<int:id>')
def banner(id=931049816895684638):
    return jsonify(requests.get(f'https://canary.discordapp.com/api/v9/users/{id}', headers={'Authorization': 'Bot {}'.format(os.environ['TOKEN'])}).text)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
