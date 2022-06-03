from flask import Flask, jsonify, redirect

import os
import requests
import json
from PIL import Image, ImageChops, ImageDraw, ImageFont
from io import BytesIO
import asyncio
import numpy as np

app = Flask(__name__, template_folder='.')
app.config["DEBUG"] = False

@app.route('/')
def index():
    return redirect('https://basically.email/discord')

@app.route('/banner/<int:id>')
def banner(id):
    data = json.loads(requests.get(f"https://canary.discordapp.com/api/v9/users/{id}", headers={'Authorization': 'Bot {}'.format(os.environ['TOKEN'])}).text)
    avatar_url = f"https://cdn.discordapp.com/avatars/{id}/{data['avatar']}.png"
    avatar = requests.get(avatar_url).content
    background = Image.open("welcomeTemplate.png") 
    data = BytesIO(avatar.read())

    pfp = Image.open(data).convert("RGBA")
    pfp = circle(pfp)
    pfp = pfp.resize((265,265))

    draw = ImageDraw.Draw(background)
    font = ImageFont.truetype("KdamThmorPro.otf",42) 
    member_text = (f"Welcome {data['username']}")
    draw.text((383,410),member_text,font=font)

    background.paste(pfp, (379,123), pfp) 
    background.save(f'{id}.png')
    return send_file(f'{id}.png', mimetype='image/gif')
    
    


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
