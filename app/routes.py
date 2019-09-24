from flask import render_template
from app import app, vibe

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', vibe=vibe)