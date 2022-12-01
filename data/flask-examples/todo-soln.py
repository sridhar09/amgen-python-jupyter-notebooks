import os
from flask import Flask, render_template, request, url_for, redirect

from .state import StateManager

app = Flask(__name__)

STATE_MANAGER = StateManager(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            'state.pkl'
        )
    )
)

@app.route('/')
def home():
    state = STATE_MANAGER.get()
    items = state.get('items', [])
    return render_template('todo2.html', items=items)


@app.route('/item', methods=['POST'])
def add_todo():
    state = STATE_MANAGER.get()
    items = state.setdefault('items', [])
    items.append(request.form['item'])
    STATE_MANAGER.save()
    return redirect(url_for('home'))


@app.route('/item/<int:index>', methods=['POST'])
def update_todo(index):
    state = STATE_MANAGER.get()
    items = state.get('items', [])
    if index < len(items):
        if 'delete' in request.form:
            del items[index]
        else:
            items[index] = request.form['item']
        STATE_MANAGER.save()
    return redirect(url_for('home'))
