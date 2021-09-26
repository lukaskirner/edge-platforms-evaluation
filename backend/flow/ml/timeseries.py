

def z_normalize_df(df):
    """
        Z normalize and return given dataframe.
    """
    return (df - df.mean()) / df.std()


def z_normalize(df, cols):
    """
        Z normalize only specified cols of the given dataframe and return it.

        @param df: The dataframe to normalize.
        @param cols: Columns to include for normalization.
    """
    return df.loc[:, cols].copy(deep=True).apply(lambda x: (x - x.mean()) / x.std())


def min_max_scale(df, cols):
    """
        Min-max scale and return specified columns of given dataframe.

        @param df: The dataframe to scale.
        @param cols: Columns to include for scaling.
    """
    return df.loc[:, cols].copy(deep=True).apply(lambda x: (x - x.min()) / (x.max() - x.min()))


def normalize_row_wise(data, cols):
    """
        Normalize rows all rows for given columns by summing them up and dividing by column count.

        @param data: Dataframe to normalize.
        @param cols: Cols to involve in normalization.
    """
    # row normalized results
    return data[cols].div(data[cols].sum(axis=1), axis=0)

