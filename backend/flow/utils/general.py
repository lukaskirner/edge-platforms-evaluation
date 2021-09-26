import os


def list_files(path):
    """
        Returns list with all files within the given path.
    """
    cwd = f"{os.getcwd()}/{path}"
    files = os.listdir(cwd)
    return files


def unique(list_):
    """
        Return given list as a list containing only unique values.
    """
    list_set = set(list_)
    unique_list = (list(list_set))

    return unique_list


def is_int(s):
    """
        Check if given String contains an integer.
    """
    try:
        int(s)
        return True
    except ValueError:
        return False


def save_pkl(path, df, name):
    """
        Save given data frame .pkl encoded.

        @param path: The path to save the dataframe to.
        @param df: The dataframe to persist.
        @param name: Name of the .pkl file to create.
    """
    try:
        if not os.path.exists(path):
            os.mkdir(path)
    except OSError:
        print("Creation of the directory %s failed" % path)

    df.to_pickle(f"{path}/{name}")
    print(f"Successfully saved df to {path}/{name}")
