""" Tests full suite of linear models for MyoASL """
import sys
import numpy as np
from sklearn.linear_model import *
from sklearn.svm import *

from myoasl.ml import preprocess


def evaluate(model, test_set, true_labels, dest=sys.stdout):
    """ Runs various evaluation metrics on a model."""
    pred_labels = model.predict(test_set)
    accuracy = np.sum(pred_labels == true_labels) / float(true_labels.size)
    print >> dest, '-'*30
    print >> dest, model
    print >> dest, "Accuracy:", accuracy
    return accuracy


def test_model(model, X_train, X_val, y_train, y_val,
               logfile='log.linear-models.txt'):
    """ Trains a model and evaluates it, writing results to logfile. """
    model.fit(X_train, y_train)
    with open(logfile, 'a') as fp:
        evaluate(model, X_val, y_val, dest=fp)


def test_all(data_filename):
    """ Create and evaluate various linear models. """
    data = preprocess.create_train_val_splits(data_filename)

    models = [
        LogisticRegression(multi_class='multinomial', solver='lbfgs', C=1.0),
        LogisticRegression(multi_class='ovr', solver='lbfgs', C=1.0),
        LinearSVC(penalty='l2', loss='squared_hinge', dual=True, tol=0.0001,
                  C=1.0, multi_class='ovr', fit_intercept=True,
                  intercept_scaling=1, class_weight=None, verbose=0,
                  random_state=None, max_iter=1000)

    ]

    for model in models:
        test_model(model, *data)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Please specify data filename."
        sys.exit(1)

    data_filename = sys.argv[1]
    test_all(data_filename)
