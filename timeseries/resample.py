import pandas as pd


def parse_input(d):
    df = pd.read_json(d)
    if 'timeStamp' in df.columns:
        return df.set_index('timeStamp')

    return False


def resample(df, rule, interpolation_method, to_json=True):
    """
    :param to_json:
    :param df: Pandas dataframe with time-based index
    :param rule: pandas resample rule
    :param interpolation_method:
    """

    if not isinstance(df, pd.DataFrame):
        return False

    df = df.resample(rule).interpolate(method=interpolation_method).reset_index(level=0)

    if to_json:
        return df.to_json(orient='records', date_unit='s')

    return df
