""" Tests full suite of linear models for MyoASL """
import cPickle
import sys
import os
import numpy as np
from sklearn.linear_model import *
from sklearn.svm import *
import argparse

from myoasl.ml import preprocess

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--save-directory", dest="save_directory",
        default="classifiers/")
    parser.add_argument("-d", "--data", required=True)

    return parser.parse_args()

def evaluate(model, test_set, true_labels, dest=sys.stdout):
    """ Runs various evaluation metrics on a model."""
    pred_labels = model.predict(test_set)
    accuracy = np.sum(pred_labels == true_labels) / float(true_labels.size)
    print >> dest, '-'*30
    print >> dest, model
    print >> dest, "Accuracy:", accuracy
    return accuracy

def save_classifier(model, name):
    with open(name, 'w') as fp:
        cPickle.dump(model, fp)

def test_model(model, X_train, X_val, y_train, y_val,
               logfile='log.linear-models.txt'):
    """ Trains a model and evaluates it, writing results to logfile. """
    model.fit(X_train, y_train)
    with open(logfile, 'a') as fp:
        evaluate(model, X_val, y_val, dest=fp)


def test_all(data_filename, save_directory):
    """ Create and evaluate various linear models. """
    data = preprocess.create_train_val_splits(data_filename, series_length=50)

    models = {
        'log-reg-multinomial': LogisticRegression(multi_class='multinomial', solver='lbfgs', C=1.0),
        'log-reg-ovr': LogisticRegression(multi_class='ovr', solver='lbfgs', C=1.0),
        'linear-svc': LinearSVC(penalty='l2', loss='squared_hinge', dual=True, tol=0.0001,
                  C=1.0, multi_class='ovr', fit_intercept=True,
                  intercept_scaling=1, class_weight=None, verbose=0,
                  random_state=None, max_iter=1000)

    }

    for model_name in models:
        test_model(models[model_name], *data)

    if not os.path.isdir(save_directory):
        os.makedirs(save_directory)

    for model_name in models:
        save_classifier(models[model_name], os.path.join(save_directory, model_name + '.mdl'))

def main():
    args = get_args()
    test_all(args.data, args.save_directory)

if __name__ == "__main__":
    main()