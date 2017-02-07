import itertools
import os
import pathlib

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/render')
def render():
    pass


@app.route('/')
def index():
    root = pathlib.Path(os.environ['NBRUNNER_ROOT'])
    files = root.rglob('*.ipynb')
    file_items = itertools.groupby(sorted(files), lambda f: f.parent)
    return render_template('index.html', files=file_items, root=root)


if __name__ == '__main__':
    app.run()
