import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

import ml.visualization as viz

import ml.timeseries as ts
from scipy.stats import kurtosis, skew

from sklearn.model_selection import train_test_split

from scipy.stats import linregress

from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.dummy import DummyClassifier


def sketch_supervised_classification(data, clfs, col_layout=2, balance_dataset=True):
    """
        Fast supervised classification and plotting within a confusion matrix for the given dataset.
        Non-number columns are dropped automatically, dataset needs to contain a 'label' column.

        @param data: The dataset to use for classification
        @param clfs: List with classifiers to use (optional). If not provided, default selection is used.
        @param col_layout: Column layout to use for plotting, default is 2 (optional).
        @param balance_dataset: Balance dataset in case of not evenly distributed classes
                                or not (optional), default True.
    """

    if balance_dataset:
        data = balance_data_by_downsampling(data)

    cols = list(data.select_dtypes(include=['number']).columns)
    if 'timestamp' in cols:
        cols.remove('timestamp')

    X = data[cols].to_numpy()
    y = data['label'].to_numpy()

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    if clfs is None:
        clfs = [
                GaussianNB(),
                RandomForestClassifier(max_depth=3, random_state=0),
                DecisionTreeClassifier(max_depth=3),
                DummyClassifier(strategy="most_frequent")
                ]

    for clf in clfs:
        clf.fit(X_train, y_train)

    viz.plot_multi_confusion(clfs, X, y, X_test, y_test, col_layout)

    return clfs


def select_cols_by_correlation(cor, thresh, target, skip_cols=['timestamp', 'label']):
    """
        Returns list of features pruned by correlation threshold in comparison to the target column.

        @param cor: Correlation matrix containing all Pearson correlation of all columns to each other.
        @param thresh: Pruning threshold, all features with lower absolute correlation are dropped.
        @param target: The target column to compare all other column's correlations to.
        @param list skip_cols: Columns to ignore for selection (optional). Default is 'timestamp', 'label'.
    """
    cor_target = abs(cor[target])
    rel_feat = cor_target[cor_target > thresh]
    selection = list(rel_feat.index.values)
    for col in skip_cols:
        if col in selection:
            selection.remove(col)

    return selection


def pearson_cor(data, plot=True):
    """
        Calculate and return pearson correlation matrix for given columns to each other and plot it.

        @param data: dataframe to calculate correlation for, must contain numerical columns only.
        @param plot: Flag indicating if plot correlation matrix or not.
    """
    cor = data.corr()
    if plot:
        plt.figure(figsize=(12, 10))
        sns.heatmap(cor, annot=True, cmap=plt.cm.Reds)
        plt.show()

    return cor


def string_cols_to_numeric(data, cols):
    """
        Return a new dataframe with replaced values for the given columns with their
        corresponding index in a unique list.

        @param data: The data frame to process.
        @param cols: The Cols to replace
    """

    dataset = data.copy()
    for col in cols:
        labels = list(dataset[col].unique())
        dataset[col] = dataset[col].apply(lambda x: float(labels.index(x)))

    return dataset


def aggregate_labels(label, agg_map=None):
    """
        Match given label with substring labels in agg_map and return key as the new label.

        @param label: Label to aggregate.
        @param agg_map: Map containing potential labels for aggregation (optional).

    """
    keys = agg_map.keys()
    for key in keys:
        if label in agg_map.get(key):
            label = key

    return label


def balance_data_by_downsampling(data, label_col='label'):
    """
        Down sample underlying classes of given dataset to the size of the smallest class,
        by random selection.

        @param data: Data containing unbalanced classes.
        @param label_col: Column containing labels (optional), default 'label'
    """

    grouped = data.groupby(label_col).count()
    min_class = grouped.min(skipna=True)[0]

    shuffled_df = data.sample(frac=1)

    balanced_splits = []
    for label in data[label_col].unique():
        balanced_splits.append(shuffled_df.loc[shuffled_df[label_col] == label]
                               .sample(n=min_class, random_state=42))

    return pd.concat(balanced_splits)


def get_balanced_split(data, cols):
    """
        Balance given data and return it as X and y.

        @param data: The data to balance and split.
        @param cols: Value cols.
    """
    data = balance_data_by_downsampling(data)
    x = data[cols]
    y = data['label']

    return x, y


def label_experiment_data(data, lookup):
    #TODO
    # extract experiments and add labels
    data["label"] = np.nan

    def add_exp_label(row):
        ts = row.timestamp
        for i, r in lookup.iterrows():
            if r.start_sec <= ts < r.end_sec:
                row.label = r.experiment
                break

        return row

    data = data.apply(lambda row: add_exp_label(row), axis=1)
    data = data.dropna()
    return data


def add_statistical_features(data):
    # TODO comment and refactor
    # data column format needs to be: ['timestamp', ......., 'label']

    featuresDF = data.copy().groupby("timestamp").mean()

    # add several handcrafted statistical features
    channels = list(data.columns)
    channels.remove('timestamp')
    channels.remove('label')

    featuresDF[channels] = ts.z_normalize_df(featuresDF[channels])

    for chan in channels:
        featuresDF[f"{chan}-std"] = data[chan].groupby(data['timestamp']).std()
        featuresDF[f"{chan}-var"] = data[chan].groupby(data['timestamp']).var()
        featuresDF[f"{chan}-min"] = data[chan].groupby(data['timestamp']).min()
        featuresDF[f"{chan}-max"] = data[chan].groupby(data['timestamp']).max()
        featuresDF[f"{chan}-slope"] = data[chan].groupby(data['timestamp']).apply(
            lambda g: linregress(g.values, g.index.values)[0])
        featuresDF[f"{chan}-range"] = data[chan].groupby(data['timestamp']).apply(
            lambda g: g.values.max() - g.values.min())
        featuresDF[f"{chan}-skew"] = data[chan].groupby(data['timestamp']).apply(
            lambda g: skew(g.values))
        featuresDF[f"{chan}-kurtosis"] = data[chan].groupby(data['timestamp']).apply(
            lambda g: kurtosis(g.values))
        featuresDF = featuresDF.fillna(0)

    featuresDF.reset_index(inplace=True)

    return featuresDF