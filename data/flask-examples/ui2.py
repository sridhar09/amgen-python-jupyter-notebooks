
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/form')
def form():
    return render_template('form.html')
    

@app.route('/post', methods=['POST'])
def post():
    return render_template('post.html', form=request.form)
