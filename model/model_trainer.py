from sklearn.exceptions import ConvergenceWarning
from sklearn.utils.testing import ignore_warnings
import xgboost as xgb
from sklearn.svm import SVR
from sklearn.datasets import make_regression
from sklearn.linear_model import ElasticNet
from sklearn.model_selection import KFold
from sklearn import model_selection
from sklearn.preprocessing import LabelEncoder
from sklearn import preprocessing
import numpy as np
import math
import pandas as pd

# Elastic Net, after testing ridge regression out performs lasso, tune l1_ratio to 0


def test_train_elastic_net(X, Y):
    print("training is started")
    kf = KFold(n_splits=5, shuffle=True, random_state=0)
    total_correct_train = 0
    total_train = 0
    total_correct_test = 0
    total_test = 0
    for train_index, test_index in kf.split(X):
        axis = 0
        model = ElasticNet(l1_ratio=0, max_iter=2**18)
        model.fit(np.take(X, train_index, axis), np.take(Y, train_index, axis))
        '''
        valid_attributes = []
        coef = preprocessing.scale(model.coef_.reshape(-1, 1))
        print(model.get_params())
        
        for i in range(len(attributes)):
            if abs(coef[i]) > 1:
                valid_attributes.append((attributes[i],coef[i][0]))
        print("attributes value: {}\n".format(valid_attributes))
        '''

        t_predicted = model.predict(np.take(X, train_index, axis))
        t_actual = np.take(Y, train_index, axis)
        t_wl_predicted = (t_predicted > 0).astype(int)
        t_wl_actual = (t_actual > 0).astype(int)
        t_correct = (t_wl_actual == t_wl_predicted).astype(int).sum()
        t_loss = (t_predicted - t_actual)**2
        total_correct_train += t_correct
        total_train += t_loss.shape[0]
        t_total_loss = t_loss.sum()
        print("training:")
        print("total loss: {}, average loss: {}".format(
            t_total_loss, t_total_loss/t_loss.shape[0]))
        print("correct: {}, correctness: {}\n".format(
            t_correct, t_correct/t_loss.shape[0]))

        predicted = model.predict(np.take(X, test_index, axis))
        actual = np.take(Y, test_index, axis)
        wl_predicted = (predicted > 0).astype(int)
        wl_actual = (actual > 0).astype(int)
        correct = (wl_actual == wl_predicted).astype(int).sum()
        loss = (predicted - actual)**2
        total_correct_test += correct
        total_test += loss.shape[0]
        total_loss = loss.sum()
        print("testing:")
        print("total loss: {}, average loss: {}".format(
            total_loss, total_loss/loss.shape[0]))
        print("correct: {}, correctness: {}\n".format(
            correct, correct/loss.shape[0]))
    print("training:")
    print("correct: {}, correctness: {}\n".format(
        total_correct_train, total_correct_train/total_train))
    print("testing:")
    print("correct: {}, correctness: {}\n".format(
        total_correct_test, total_correct_test/total_test))
    print("training is done")

# XGBoost


def test_train_XG_boost(X, Y, learning_rate=0.01):
    print("training is started")
    kf = KFold(n_splits=5, shuffle=True, random_state=0)
    total_correct_train = 0
    total_train = 0
    total_correct_test = 0
    total_test = 0
    for train_index, test_index in kf.split(X):
        axis = 0
        model = xgb.XGBClassifier(silent=False,
                                  scale_pos_weight=1,
                                  learning_rate=0.01,
                                  n_estimators=200)
        model.fit(np.take(X, train_index, axis), np.take(Y, train_index, axis))

        t_predicted = model.predict(np.take(X, train_index, axis))
        t_actual = np.take(Y, train_index, axis)
        t_wl_predicted = (t_predicted > 0).astype(int)
        t_wl_actual = (t_actual > 0).astype(int)
        t_correct = (t_wl_actual == t_wl_predicted).astype(int).sum()
        t_loss = (t_predicted - t_actual)**2
        total_correct_train += t_correct
        total_train += t_loss.shape[0]
        t_total_loss = t_loss.sum()
        print("training:")
        print("total loss: {}, average loss: {}".format(
            t_total_loss, t_total_loss/t_loss.shape[0]))
        print("correct: {}, correctness: {}\n".format(
            t_correct, t_correct/t_loss.shape[0]))

        predicted = model.predict(np.take(X, test_index, axis))
        actual = np.take(Y, test_index, axis)
        wl_predicted = (predicted > 0).astype(int)
        wl_actual = (actual > 0).astype(int)
        correct = (wl_actual == wl_predicted).astype(int).sum()
        loss = (predicted - actual)**2
        total_correct_test += correct
        total_test += loss.shape[0]
        total_loss = loss.sum()
        print("testing:")
        print("total loss: {}, average loss: {}".format(
            total_loss, total_loss/loss.shape[0]))
        print("correct: {}, correctness: {}\n".format(
            correct, correct/loss.shape[0]))
    print("training:")
    print("correct: {}, correctness: {}\n".format(
        total_correct_train, total_correct_train/total_train))
    print("testing:")
    print("correct: {}, correctness: {}\n".format(
        total_correct_test, total_correct_test/total_test))
    print("training is done")

# SVM


def test_train_SVM(X, Y, kernel='linear'):
    print("training is started")
    kf = KFold(n_splits=5, shuffle=True, random_state=0)
    total_correct_train = 0
    total_train = 0
    total_correct_test = 0
    total_test = 0
    for train_index, test_index in kf.split(X):
        axis = 0
        model = SVR(kernel=kernel, gamma='scale',
                    epsilon=0.1, C=1, max_iter=-1)
        model.fit(np.take(X, train_index, axis), np.take(Y, train_index, axis))

        t_predicted = model.predict(np.take(X, train_index, axis))
        t_actual = np.take(Y, train_index, axis)
        t_wl_predicted = (t_predicted > 0).astype(int)
        t_wl_actual = (t_actual > 0).astype(int)
        t_correct = (t_wl_actual == t_wl_predicted).astype(int).sum()
        t_loss = (t_predicted - t_actual)**2
        total_correct_train += t_correct
        total_train += t_loss.shape[0]
        t_total_loss = t_loss.sum()
        print("training:")
        print("total loss: {}, average loss: {}".format(
            t_total_loss, t_total_loss/t_loss.shape[0]))
        print("correct: {}, correctness: {}\n".format(
            t_correct, t_correct/t_loss.shape[0]))

        predicted = model.predict(np.take(X, test_index, axis))
        actual = np.take(Y, test_index, axis)
        wl_predicted = (predicted > 0).astype(int)
        wl_actual = (actual > 0).astype(int)
        correct = (wl_actual == wl_predicted).astype(int).sum()
        loss = (predicted - actual)**2
        total_loss = loss.sum()
        total_correct_test += correct
        total_test += loss.shape[0]
        print("testing:")
        print("total loss: {}, average loss: {}".format(
            total_loss, total_loss/loss.shape[0]))
        print("correct: {}, correctness: {}\n".format(
            correct, correct/loss.shape[0]))
    print("training:")
    print("correct: {}, correctness: {}\n".format(
        total_correct_train, total_correct_train/total_train))
    print("testing:")
    print("correct: {}, correctness: {}\n".format(
        total_correct_test, total_correct_test/total_test))
    print("training is done")


def find_important_attributes(model):
    valid_attributes = []
    coef = model.coef_.reshape(-1, 1)
    for i in range(len(attributes)):
        if abs(coef[i]) > 0.25:
            valid_attributes.append((attributes[i], coef[i][0]))
    print("attributes value: {}\n".format(valid_attributes))
    return model


@ignore_warnings(category=ConvergenceWarning)
def train_predictor(X, Y, pre_model):
    print("training is started")
    model = pre_model
    model.fit(X, Y)
    predicted = model.predict(X)
    actual = Y
    print(actual)
    print(predicted)
    wl_predicted = (predicted > 0).astype(int)
    wl_actual = (actual > 0).astype(int)
    correct = (wl_actual == wl_predicted).astype(int).sum()
    loss = abs(predicted - actual)
    total_loss = loss.sum()
    print("total loss: {}, average loss: {}".format(
        total_loss, total_loss/loss.shape[0]))
    print("correct: {}, correctness: {}".format(
        correct, correct/loss.shape[0]))
    print("training is ended\n")
    return model


if __name__ == "__main__":
    df = pd.read_csv("./season_average_data.csv").drop(["match_up"], axis=1)
    average_data = df.to_numpy().astype(float)
    X_average = average_data[:, :-1]
    Y_average = average_data[:, -1]
    label_encoder = LabelEncoder()
    label_encoder = label_encoder.fit(Y_average)
    label_encoded_y = label_encoder.transform(Y_average)
    scaler = preprocessing.StandardScaler().fit(X_average)
    X_average = scaler.transform(X_average)
    df = df.drop(["diff"], axis=1)
    attributes = list(df.columns.values)

    test_train_SVM(X_average, Y_average)
    test_train_elastic_net(X_average, Y_average)
    test_train_XG_boost(X_average, Y_average)
