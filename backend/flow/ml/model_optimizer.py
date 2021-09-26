import numpy as np
import pandas as pd
import ml.helpers as ml

from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.utils.fixes import loguniform
from sklearn.model_selection import cross_val_score

from scipy import stats


RANDOM_SEARCH_ITERS = 100
CV_FOLDS = 3

"""
    Wrapper script to automatically find optimized classifier models.
"""

# Static parameters with ranges to test during parameter optimization for different classifiers.
# Add new parameter sets if you want to use new classifiers not covered below.

clf_params = {'ExtraTreesClassifier': {'ccp_alpha': np.arange(0.0, 1, 0.05).tolist(),
                                       'max_depth': np.arange(1, 100, 1).tolist(),
                                       'max_features': ['auto', 'sqrt', 'log2'],
                                       'max_leaf_nodes': np.arange(20).tolist(),
                                       'min_samples_leaf': np.arange(1, 20, 1).tolist(),
                                       'min_samples_split': np.arange(1, 20, 1).tolist()},
              'RandomForestClassifier': {'max_features': ['auto', 'sqrt', 'log2'],
                                         'max_depth': np.arange(1, 50, 1).tolist(),
                                         'criterion': ['gini', 'entropy'],
                                         'min_samples_leaf': np.arange(1, 40, 1).tolist(),
                                         'min_samples_split': np.arange(1, 40, 1).tolist(),
                                         'n_estimators': np.arange(5, 100, 1).tolist(), },
              'DecisionTreeClassifier': {'ccp_alpha': np.arange(0.0, 1, 0.05).tolist(),
                                         'criterion': ['gini', 'entropy'],
                                         'max_depth': np.arange(1, 100, 1).tolist(),
                                         'max_features': ['auto', 'sqrt', 'log2'],
                                         'max_leaf_nodes': np.arange(20).tolist(),
                                         'min_samples_leaf': np.arange(1, 20, 1).tolist(),
                                         'min_samples_split': np.arange(1, 20, 1).tolist(),
                                         'splitter': ['best', 'random'], },
              'SVC': {'C': np.arange(0, 100 + 1, 1).tolist(),
                      'kernel': ['poly', 'sigmoid', 'rbf'],
                      'degree': np.arange(0, 100, 1).tolist(),
                      'gamma': np.arange(0.0, 10.0, 0.1).tolist(),
                      'coef0': np.arange(0.0, 10.0, 0.1).tolist(),
                      'tol': np.arange(0.001, 0.01, 0.001).tolist(),
                      'cache_size': [2000], },
              'SGDClassifier': {'average': [True, False],
                                'l1_ratio': stats.uniform(0, 1),
                                'alpha': loguniform(1e-4, 1e0),
                                'loss': ['hinge'],
                                'penalty': ['elasticnet']},
              'LogisticRegression': {'C': np.arange(0, 100 + 1, 1).tolist(),
                                     'dual': [True, False],
                                     'fit_intercept': [True, False],
                                     'intercept_scaling': np.arange(1, 2, 0.05).tolist(),
                                     'max_iter': np.arange(100, 300, 20).tolist(),
                                     'penalty': ['l1', 'l2', 'elasticnet', 'none'],
                                     'solver': ['newton-cg', 'lbfgs', 'liblinear', 'sag', 'saga'],
                                     'tol': np.arange(0.001, 0.01, 0.001).tolist()},
              }


def get_random_search_optimized_clf(clf, X, y, iters=RANDOM_SEARCH_ITERS, cv=CV_FOLDS):
    """
        Create, fit and return randomized search for the given parameters.

        @params clf: The classifier to instantiate the random search for.
        @param X: Dataset to use for fitting.
        @param y: labels corresponding to X
        @param iters: Number of random search iterations to execute.
        @param cv: Number of folds to use for cross validation.

    """
    random_search = RandomizedSearchCV(estimator=clf,
                                       param_distributions=clf_params[clf.__class__.__name__],
                                       n_iter=iters,
                                       cv=cv,
                                       verbose=0,
                                       random_state=42,
                                       n_jobs=-1)

    random_search.fit(X, y)

    print(f"{clf.__class__.__name__}: candidate with best acc achieves {round(random_search.best_score_ * 100, 2)}%.")

    return random_search


def get_grid_search_optimized_clf(clf, X, y):
    """
        Create, fit and return grid search for the given parameters.

        @params clf: The classifier to instantiate the random search for.
        @param X: Dataset to use for fitting.
        @param y: labels corresponding to X.

    """
    grid_search = GridSearchCV(clf, param_grid=clf_params[clf.__class__.__name__])
    grid_search.fit(X, y)

    print_best_config(grid_search)

    return grid_search


def print_best_config(random_search):
    """
        Print simple report for given random search object covering the best performing estimator.
    """
    print("\n")
    print(f"Classifier: {random_search.best_estimator_}")
    print(f"Accuracy: {round(random_search.best_score_,2)}")
    print(f"Params: {random_search.best_params_}")
    print("\n------")


def report(random_search, n_top=3):
    """
        Report best n parameter combinations for given random search.
    """

    for i in range(1, n_top + 1):
        candidates = np.flatnonzero(random_search['rank_test_score'] == i)
        for candidate in candidates:
            print("Model with rank: {0}".format(i))
            print("Mean validation score: {0:.3f} (std: {1:.3f})"
                  .format(random_search['mean_test_score'][candidate],
                          random_search['std_test_score'][candidate]))
            print("Parameters: {0}".format(random_search['params'][candidate]))
            print("")


# TODO below document and refactor
def determine_cor_thresh_range(data, cor, clfs):
    folds = 5
    scores = pd.DataFrame()
    for clf in clfs:

        score = []
        i = 1
        thresh = []
        while i > 0:

            mean = 0
            cols = ml.select_cols_by_correlation(cor, i, 'label')

            if len(cols) > 2:

                X, y = ml.get_balanced_split(data, cols)

                s = cross_val_score(clf, X, y, cv=folds)
                mean = np.mean(s)

            thresh.append(i)
            score.append(mean)
            i = i - 0.01

        scores[clf.__class__.__name__] = score

    scores['thresh'] = thresh

    ax = scores.set_index('thresh').plot(figsize=(20, 8))
    ax.set_xlabel("correlation threshold")
    ax.set_ylabel("accuracy")

    for s in scores.columns[:len(scores.columns) - 1]:
        max_acc_idx = scores.index[scores[s] == scores[s].max()][0]
        xpos = scores['thresh'].iloc[max_acc_idx]
        ypos = scores[s].iloc[max_acc_idx]
        ax.plot(xpos, ypos, 'ro')
        bbox_props = dict(boxstyle="round,pad=0.3", fc="white", ec="r", lw=1)
        text = ax.text(xpos, ypos, f"{s}, max-Acc: {round(scores[s].max(), 2)}", size=12, rotation=45, bbox=bbox_props)

    return scores


# TODO below document and refactor
def determine_tree_depth_optimum(clfs, data, cor, thresh, max_depth=15):

    feat_cols = ml.select_cols_by_correlation(cor, thresh, 'label')

    X, y = ml.get_balanced_split(data, feat_cols)

    folds = 3
    scores = pd.DataFrame()
    for clf in clfs:

        tree_depth = 1
        max_trees = max_depth
        score = []
        depth = []
        while tree_depth <= max_trees:
            clf.set_params(max_depth=tree_depth)

            score.append(np.mean(cross_val_score(clf, X, y, cv=folds)))
            depth.append(tree_depth)

            tree_depth = tree_depth + 1

        scores[clf.__class__.__name__] = score

    scores['depth'] = depth

    ax = scores.set_index('depth').plot(figsize=(16, 6))
    ax.set_xlabel("tree depth")
    ax.set_ylabel("accuracy")

    for s in scores.columns[:len(scores.columns) - 1]:
        max_acc_idx = scores.index[scores[s] == scores[s].max()][0]
        xpos = max_acc_idx + 1
        ypos = scores[s].iloc[max_acc_idx]
        ax.plot(xpos, ypos, 'ro')
        bbox_props = dict(boxstyle="round,pad=0.3", fc="white", ec="r", lw=1)
        ax.text(xpos, ypos, f"{s}, max-Acc: {round(scores[s].max(), 2)}", size=10, rotation=45,
                bbox=bbox_props)

    return scores
