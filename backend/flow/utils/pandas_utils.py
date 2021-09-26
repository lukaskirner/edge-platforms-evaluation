import pandas as pd


def unique_values(df):
    """
        Count unique values for all cols in data frame and print sample values.
    """
    cols = list(df.columns)

    for col in cols:
        uniques = (df[col]).unique()
        print(f"{len(uniques)} unique items in {col}: {df[col].loc[0]},{df[col].loc[1]}, {df[col].loc[2]}...")


def strip_static_cols(df):
    """
        Strip all cols from given df containing static values or nans.
    """
    for col in df.columns:
        if len((df[col]).unique()) == 1:
            df.drop(columns=[col], inplace=True)
    return df


def seconds_from_datetime(df, time_col):
    #TODO rename timestamp to counter for generalization
    """
        Create row containing seconds since first datetime in a dataframe, called 'timestamp'.
    """
    start = pd.to_datetime(df[time_col].iloc[0])
    df['timestamp'] = df[time_col].map(
        lambda c_time: round(pd.Timedelta(pd.to_datetime(c_time) - start).total_seconds()))
    return df
