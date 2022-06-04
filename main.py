from flask import Flask, jsonify, redirect, send_file

import os
import requests
import json
from PIL import Image, ImageChops, ImageDraw, ImageFont
from io import BytesIO
import asyncio
import numpy as np

app = Flask(__name__, template_folder='.')
app.config["DEBUG"] = False

'''
@app.route('/')
def index():
    return redirect('https://basically.email/discord')
'''

@app.route('/banner/<int:id>')
def banner(id):
    data = json.loads(requests.get(f"https://canary.discordapp.com/api/v9/users/{id}", headers={'Authorization': 'Bot {}'.format(os.environ['TOKEN'])}).text)
    avatar_url = f"https://cdn.discordapp.com/avatars/{id}/{data['avatar']}.png"
    avatar = requests.get(avatar_url).content
    background = Image.open("welcomeTemplate.png") 
    byte_pfp = BytesIO(avatar)

    pfp = Image.open(byte_pfp).convert("RGBA")
    pfp = pfp.resize((512,512))

    draw = ImageDraw.Draw(background)
    font = ImageFont.truetype("KdamThmorPro.ttf",120) 
    member_text = (f"Welcome {data['username']}")
    
    w, h = draw.textsize(member_text)
    draw.text(((2400-(len(member_text)*10))//2,650), member_text,font=font)

    background.paste(pfp, ((2400//2)-400//2,123), pfp) 
    background.save(f'{id}.png')
    return send_file(f'{id}.png', mimetype='image/gif')
    
    


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
