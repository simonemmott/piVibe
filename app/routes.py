from flask import render_template
from app import app, vibe
from piVibe import modes

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', vibe=vibe, modes=modes)