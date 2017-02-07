import glob
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
        filepath = pathlib.Path(root, path)
        fp = filepath.open('r')
        notebook = nbformat.read(fp, as_version=4)
    except FileNotFoundError:
        abort(404)
    pre = ExecutePreprocessor()
    pre.preprocess(notebook, {'metadata': {'path': filepath.parent}})
    exporter = HTMLExporter()
    body, resources = exporter.from_notebook_node(notebook)
    return body


@app.route('/')
def index():
    # unfortunately, pathlib.{i,}glob cannot be used in most versions < 3.6
    # due to a bug with permissions - see http://bugs.python.org/issue24120
    root = os.path.normpath(os.environ['NBRUNNER_ROOT'])
    files = glob.glob('{}/**/*.ipynb'.format(root), recursive=True)
    file_items = itertools.groupby(sorted(files), lambda f: os.path.dirname(f))
    folder_files = {}
    for path, items in file_items:
        folder_files[path] = [(os.path.relpath(file, root), os.path.basename(file)) for file in items]
    return render_template('index.html', files=folder_files)


if __name__ == '__main__':
    app.run()
