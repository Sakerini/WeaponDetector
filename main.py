import flask
import os

port = int(os.getenv('PORT', 1111))
app = flask.Flask(__name__, template_folder='template')

@app.route('/camera')
def main():
    return(flask.render_template('camera.html'))

if __name__ == '__main__':
    host = 'localhost'    # if testing on local machine
    #host = '192.168.1.2'
    app.run(host=host, port=port)