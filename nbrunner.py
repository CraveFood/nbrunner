import itertools
import os
import pathlib

import nbformat
from flask import Flask, abort, render_template, request
from nbconvert.exporters import HTMLExporter
from nbconvert.preprocessors import ExecutePreprocessor

app = Flask(__name__)


@app.route('/render')
def render():
    root = pathlib.Path(os.environ['NBRUNNER_ROOT'])
    path = request.args.get('file', '')
    if not path.endswith('.ipynb'):
        abort(404)
    try:
        fp = pathlib.Path(root, path).open('r')
        notebook = nbformat.read(fp, as_version=4)
    except FileNotFoundError:
        abort(404)
    pre = ExecutePreprocessor()
    pre.preprocess(notebook, {})
    exporter = HTMLExporter()
    body, resources = exporter.from_notebook_node(notebook)
    return body


@app.route('/')
def index():
    root = pathlib.Path(os.environ['NBRUNNER_ROOT'])
    files = root.rglob('*.ipynb')
    file_items = itertools.groupby(sorted(files), lambda f: f.parent)
    return render_template('index.html', files=file_items, root=root)


if __name__ == '__main__':
    app.run()
