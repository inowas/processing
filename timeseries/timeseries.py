from flask import abort, Blueprint, request
from flask_cors import cross_origin
import json
from timeseries.resample import parse_input, resample

timeseries = Blueprint('timeseries', __name__, url_prefix='/timeseries', template_folder='templates',
                       static_folder='static')


@timeseries.route('/resample', methods=['POST'])
@cross_origin()
def resample_request():
    if request.content_type != 'application/json':
        abort(422, 'The content type is expected to be "application/json".')

    rule = request.args.get('rule', default='1D')
    interpolation_method = request.args.get('interpolation_method', 'linear')
    aggregate = request.args.get('aggregate', default=False) == 'true'

    data = None
    try:
        data = parse_input(json.dumps(request.json))
    except ValueError as e:
        abort(422, str(e))

    try:
        data = resample(data, rule=rule, interpolation_method=interpolation_method, to_json=True, aggregate=aggregate)
    except ValueError as e:
        abort(422, str(e))

    if data is False:
        abort(422, 'The content seems do be wrong')

    return data
