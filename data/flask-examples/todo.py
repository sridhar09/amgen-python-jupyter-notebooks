import os
from flask import Flask, render_template, request, url_for, redirect

from .state import StateManager

app = Flask(__name__)

STATE_MANAGER = StateManager(
    os.path.abspath(
        os.path.join(
            os.path.dirname('__file__'),
            'state.pkl'
        )
    )
)

@app.route('/')
def home():
    state = STATE_MANAGER.get()
    items = state.get('items', [])
    return render_template('todo.html', items=items)


@app.route('/add', methods=['POST'])
def add_todo():
    state = STATE_MANAGER.get()
    state.setdefault('items', []).append(request.form['item'])
    STATE_MANAGER.save()
    return redirect(url_for('home'))


@app.route('/del', methods=['POST'])
def del_todo():
    print(f'Delete {request.form["index"]}')
    state = STATE_MANAGER.get()
    index = int(request.form['index'])
    items = state.get('items', [])
    if index < len(items):
        del items[index]
        STATE_MANAGER.save()
    return redirect(url_for('home'))
