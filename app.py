import flask
import os
import pandas as pd

# Load all models files
# TODO: if files are big, load best model
from src.model import models
from src.input_processing import input_processing


port = int(os.getenv('PORT', 1111))
app = flask.Flask(__name__, template_folder='template')


def err_message():
    return '<h1>Error!</h1>'


@app.route('/', methods=['GET', 'POST'])
def main():
    if flask.request.method == 'GET':
        return(flask.render_template('main.html', original_input={}))

    if flask.request.method == 'POST':
        form = flask.request.form
        
        model = form['Model']
        
        if model not in models:
            return err_message()
        
        model = models[model]

        input_variables = input_processing(form)
        
        if not input_variables:
            return err_message()
        
        prediction = model.predict(input_variables)[0]

        return flask.render_template(
            'main.html',
            original_input=form,
            result=prediction)


@app.route('/api')
def get_all():
    models_list = [
        'svc',
        'knn',
        'log',
        'random_forest',
        'gaussian',
        'perceptron',
        'sgd',
        'linear_svc',
        'decision_tree'
    ]
    
    args = flask.request.args
    model = args.get('Model')
    
    try:
        input_variables = input_processing(dict(args))
    except:
        return err_message()
    
    if model and model in models:
        model = models[model]
        return str(model.predict(input_variables)[0])
    else:
        res = {}
        for model in models_list:
            res[model] = models[model].predict(input_variables)[0]
        return str(res)


if __name__ == '__main__':
#     host = 'localhost'    # if testing on local machine
    host = '192.168.1.2
    app.run(host=host, port=port)