import matplotlib.pyplot as plt
import math
import ml.timeseries as ts

from sklearn.metrics import plot_confusion_matrix
from sklearn.model_selection import cross_val_score


def plot_grouped_bars(data, xindex):
    """
        Group given data by xindex value and create bar plot.

        @param data: The dataframe to group and plot.
        @param xindex: The column to group data by (corresponding to the plot's x axis).
    """
    grouped = data.groupby(xindex).count().reset_index()
    ax = grouped.plot.bar(x=xindex, rot=90, figsize=(16, 6))
    ax.get_legend().remove()


def plot_multi_confusion(clfs, X, y, X_test, y_test, cols=2):
    """
        Plot confusion matrices for given selection of classifiers. Additionally, determine cross validation
        accuracy and std and include in plot.

        @param clfs: Underlying classifiers to plot
        @param X: All features.
        @param y: Corresponding labels.
        @param X_test: Test data split.
        @param y_test: Test data labels.
        @param cols: Column layout, default 2.

    """
    # TODO enable plotting of only one classifier
    rows = math.ceil(len(clfs) / cols)
    fig, axes = plt.subplots(nrows=rows, ncols=cols, figsize=(30, 10 * rows))

    for clf, ax in zip(clfs, axes.flatten()):
        score = cross_val_score(clf, X, y, cv=5)

        # plot confusion
        plot_confusion_matrix(clf, X_test, y_test, xticks_rotation='vertical', ax=ax, cmap='Blues')
        ax.title.set_text(
            f"{type(clf).__name__}, Acc:{round(score.mean(), 2)}, Std:{round(score.std(), 2)}, {5}-fold CV")

    plt.subplots_adjust(hspace=0.8)
    plt.show()


def plot_data(data, show_legend=False, normalize=True):
    """
        Create line plot of all numeric data in the given dataframe, assuming that it contains a column
        called 'timestamp' containing up counting integer values, which is used as x index.

        @param data: The dataframe to plot.
        @param show_legend: Boolean, show legend or not.
        @param normalize: Boolean, Z-normalize contained data or not.

    """
    data = data.copy().select_dtypes(include=['number'])

    val_cols = list(data.columns)
    val_cols.remove('timestamp')
    if normalize:
        data[val_cols] = ts.z_normalize(data[val_cols].astype(float), val_cols)

    data[val_cols] = data[val_cols].cumsum()

    ax = data.set_index('timestamp').plot(figsize=(16, 6))
    ax.axhline(0, color="red", linestyle="--")

    if show_legend:
        ax.legend(loc='upper right', bbox_to_anchor=(1.255, 1))
    else:
        ax.get_legend().remove()

    return ax


def plot_single_scatter(data):
    """
        Scatter given dataframe columns into individual plots, assuming that a 'timestamp' column used as x index is
        contained by the given dataframe.
    """
    cols = list(data.columns)
    cols.remove('timestamp')
    figure, axes = plt.subplots(nrows=1, ncols=1, figsize=(20, 10))

    for col in cols:
        data.plot.scatter(x='timestamp', y=col, c='DarkBlue', ax=axes, s=1)

    return axes


# TODO comment and refactor
def plot_experiments(ax, row, color, show_label, label_rot):
    ax.axvspan(row.start_sec, row.end_sec,
               alpha=0.2,
               color=color,
               linewidth=2.0)

    ylim = ax.get_ylim()
    yrange = ylim[1] - ylim[0]
    pad_top = (yrange / 25) + 1.5 * math.ceil(row.id % 2) * (yrange / 25)

    if show_label:
        bbox_props = dict(boxstyle="round,pad=0.3", fc="white", ec="r", lw=1)
        text = ax.text(row.start_sec + 20, (ylim[1] - pad_top), row.experiment,
                       size=10,
                       rotation=label_rot,
                       bbox=bbox_props)


# TODO comment and refactor
def plot_scatter(data, fig_cols, lookupDF):
    cols = data.columns[1:len(data.columns)]
    fig_rows = math.ceil(len(cols) / fig_cols)
    figure, axes = plt.subplots(nrows=fig_rows, ncols=fig_cols, figsize=(15, 3 * fig_rows))
    for col, ax in zip(cols, axes.flatten()):
        data.plot.scatter(x='timestamp', y=col, c='DarkBlue', ax=ax, s=1)
        lookupDF.apply(lambda row: plot_experiments(ax, row, "green", False, 45), axis=1)
