import flask
import os
import pandas as pd

# Load all models files
# TODO: if files are big, load best model
from src.model import models
from src.input_processing import input_processing


port = int(os.getenv('PORT', 1111))
app = flask.Flask(__name__, template_folder='template')


@app.route('/', methods=['GET', 'POST'])
def main():
    if flask.request.method == 'GET':
        return(flask.render_template('main.html', original_input={}))

    if flask.request.method == 'POST':
        form = flask.request.form
        
        model = form['Model']
        
        if model in models:
            model = models[model]
        else:
            return '<h1>Error!</h1>'

        input_variables = input_processing(form)
        prediction = model.predict(input_variables)[0]

        return flask.render_template(
            'main.html',
            original_input=form,
            result=prediction)


if __name__ == '__main__':
    app.run(host='192.168.1.2', port=port)