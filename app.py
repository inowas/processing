from flask import Flask
from flask_cors import CORS

# Blueprints
from rasters.rasters import rasters
from timeseries.timeseries import timeseries
from visualization.visualization import visualization

app = Flask(__name__)
CORS(app)

if __name__ == '__main__':
    app.register_blueprint(rasters)
    app.register_blueprint(timeseries)
    app.register_blueprint(visualization)
    app.secret_key = '2349978342978342907889709154089438989043049835890'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.debug = app.env == 'development'

    app.run(host='0.0.0.0')
