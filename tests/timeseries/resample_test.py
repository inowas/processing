import json
import pytest
import pandas as pd
from pandas.util.testing import assert_frame_equal

from timeseries.resample import parse_input, resample


def read_file(filename):
    with open(filename, 'r') as file:
        return file.read().replace('\n', '')


def test_parse_invalid_input_data_structure():
    with pytest.raises(ValueError) as e:
        parse_input(json.dumps({}))
    assert 'Error in data structure.' in str(e.value)


def test_parse_invalid_json():
    with pytest.raises(ValueError) as e:
        parse_input('')
    assert 'Error parsing JSON.' in str(e.value)


def test_parse_valid_input():
    assert isinstance(parse_input(read_file('timeseries/examples/data_hourly.json')), pd.DataFrame)
    assert isinstance(parse_input(read_file('timeseries/examples/data_weekly.json')), pd.DataFrame)


def test_resample_without_pandas_df():
    with pytest.raises(AssertionError):
        resample({}, '1D', 'linear')


def test_resample_with_unknown_rule():
    data = parse_input(read_file('tests/timeseries/data_hourly.json'))
    with pytest.raises(ValueError) as e:
        resample(data, 'unknown_rule', 'linear')
    assert 'Invalid frequency: unknown_rule' in str(e.value)


def test_resample_with_unknown_method():
    data = parse_input(read_file('tests/timeseries/data_hourly.json'))
    with pytest.raises(ValueError) as e:
        resample(data, '1D', 'unknown_method')
    assert 'method must be one of' in str(e.value)


def test_resample_to_json():
    raw = parse_input(read_file('tests/timeseries/data_hourly.json'))
    calculated = resample(raw, '1D', 'linear', to_json=True)
    expected = json.dumps([
        {'timeStamp': 1567296000, 'value': 0.5160186539}, {'timeStamp': 1567382400, 'value': 0.5160186539},
        {'timeStamp': 1567468800, 'value': 0.5449929634}, {'timeStamp': 1567555200, 'value': 0.5534393287},
        {'timeStamp': 1567641600, 'value': 0.5256767571}, {'timeStamp': 1567728000, 'value': 0.515862069},
        {'timeStamp': 1567814400, 'value': 0.515862069}, {'timeStamp': 1567900800, 'value': 0.515862069},
        {'timeStamp': 1567987200, 'value': 0.5172413793}, {'timeStamp': 1568073600, 'value': 0.5489655172},
        {'timeStamp': 1568160000, 'value': 0.5434482759}
    ])

    assert json.loads(calculated) == json.loads(expected)


def test_resample_to_pandas_df():
    raw = parse_input(read_file('tests/timeseries/data_hourly.json'))
    calculated = resample(raw, '1D', 'linear', to_json=False)
    expected = pd.read_json(
        json.dumps([
            {'timeStamp': 1567296000, 'value': 0.5160186539}, {'timeStamp': 1567382400, 'value': 0.5160186539},
            {'timeStamp': 1567468800, 'value': 0.5449929634}, {'timeStamp': 1567555200, 'value': 0.5534393287},
            {'timeStamp': 1567641600, 'value': 0.5256767571}, {'timeStamp': 1567728000, 'value': 0.515862069},
            {'timeStamp': 1567814400, 'value': 0.515862069}, {'timeStamp': 1567900800, 'value': 0.515862069},
            {'timeStamp': 1567987200, 'value': 0.5172413793}, {'timeStamp': 1568073600, 'value': 0.5489655172},
            {'timeStamp': 1568160000, 'value': 0.5434482759}
        ])
    )

    assert_frame_equal(
        calculated,
        expected
    )
