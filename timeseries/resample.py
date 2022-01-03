import numpy as np
import pandas as pd


def parse_input(d):
    try:
        df = pd.read_json(d)
    except Exception:
        raise ValueError('Error parsing JSON.')

    if 'timeStamp' in df.columns:
        return df.set_index('timeStamp')

    if 'date_time' in df.columns:
        return df.set_index('date_time')

    raise ValueError('Error in data structure.')


def resample(df, rule, interpolation_method, to_json=True, aggregate=False):
    """
    :param aggregate:
    :param to_json:
    :param df: Pandas data frame with time-based index
    :param rule: pandas resample rule
    :param interpolation_method:
    """

    assert isinstance(df, pd.DataFrame)

    try:
        if not aggregate:
            df = df.resample(rule).interpolate(method=interpolation_method).reset_index(level=0)
        if aggregate:
            df = df.resample(rule).aggregate(np.sum).interpolate(method=interpolation_method).reset_index(level=0)

    except Exception as e:
        raise e

    if to_json:
        return df.to_json(orient='records', date_unit='s')

    return df
