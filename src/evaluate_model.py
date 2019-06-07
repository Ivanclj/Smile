import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
import yaml
import argparse
from scipy import stats
from scipy.stats import randint
import random

# prep
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.datasets import make_classification
from sklearn.preprocessing import binarize, LabelEncoder, MinMaxScaler
from sklearn.feature_selection import SelectFromModel

# models
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier

# Validation libraries
from sklearn import metrics
from sklearn.metrics import accuracy_score, mean_squared_error, precision_recall_curve,confusion_matrix, classification_report, roc_auc_score, f1_score
from sklearn.model_selection import cross_val_score

#Neural Network
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import StratifiedKFold

#Bagging
from sklearn.ensemble import BaggingClassifier, AdaBoostClassifier
from sklearn.neighbors import KNeighborsClassifier

#Naive bayes
from sklearn.naive_bayes import GaussianNB

#XGBoost
import xgboost as xgb
import pickle



def evalClassModel(X,y,model, y_test, y_pred_class, plot=False):
    # Classification accuracy: percentage of correct predictions
    # calculate accuracy
    print('Accuracy:', metrics.accuracy_score(y_test, y_pred_class))

    # Null accuracy: accuracy that could be achieved by always predicting the most frequent class
    # examine the class distribution of the testing set (using a Pandas Series method)
    print('Null accuracy:\n', y_test.value_counts())

    # calculate the percentage of ones
    print('Percentage of ones:', y_test.mean())

    # calculate the percentage of zeros
    print('Percentage of zeros:', 1 - y_test.mean())

    # Comparing the true and predicted response values
    # print('True:', y_test.values[0:25])
    # print('Pred:', y_pred_class[0:25])

    # Conclusion:
    # Classification accuracy is the easiest classification metric to understand
    # But, it does not tell you the underlying distribution of response values
    # And, it does not tell you what "types" of errors your classifier is making

    # Confusion matrix
    # save confusion matrix and slice into four pieces
    confusion = metrics.confusion_matrix(y_test, y_pred_class)
    # [row, column]
    TP = confusion[1, 1]
    TN = confusion[0, 0]
    FP = confusion[0, 1]
    FN = confusion[1, 0]



    # visualize Confusion Matrix
    # sns.heatmap(confusion, annot=True, fmt="d")
    # plt.title('Confusion Matrix')
    # plt.xlabel('Predicted')
    # plt.ylabel('Actual')
    # plt.show()

    # Metrics computed from a confusion matrix
    # Classification Accuracy: Overall, how often is the classifier correct?
    accuracy = metrics.accuracy_score(y_test, y_pred_class)
    print('Classification Accuracy:', accuracy)

    # Classification Error: Overall, how often is the classifier incorrect?
    print('Classification Error:', 1 - metrics.accuracy_score(y_test, y_pred_class))

    # False Positive Rate: When the actual value is negative, how often is the prediction incorrect?
    false_positive_rate = FP / float(TN + FP)
    print('False Positive Rate:', false_positive_rate)

    # Precision: When a positive value is predicted, how often is the prediction correct?
    print('Precision:', metrics.precision_score(y_test, y_pred_class))

    # IMPORTANT: first argument is true values, second argument is predicted probabilities
    print('AUC Score:', metrics.roc_auc_score(y_test, y_pred_class))

    # calculate cross-validated AUC
    print('Cross-validated AUC:', cross_val_score(model, X, y, cv=10, scoring='roc_auc').mean())
    print('Cross-validated Accuracy:', cross_val_score(model, X, y, cv=10, scoring='accuracy').mean())
    print('Cross-validated F1:', cross_val_score(model, X, y, cv=10, scoring='f1').mean())

    ##########################################
    # Adjusting the classification threshold
    ##########################################
    # print the first 10 predicted responses
    # 1D array (vector) of binary values (0, 1)
    # print('First 10 predicted responses:\n', model.predict(X_test)[0:10])
    #
    # # print the first 10 predicted probabilities of class membership
    # print('First 10 predicted probabilities of class members:\n', model.predict_proba(X_test)[0:10])
    #
    # # print the first 10 predicted probabilities for class 1
    # model.predict_proba(X_test)[0:10, 1]
    #
    # # store the predicted probabilities for class 1
    # y_pred_prob = model.predict_proba(X_test)[:, 1]
    #
    # if plot == True:
    #     # histogram of predicted probabilities
    #     # adjust the font size
    #     plt.rcParams['font.size'] = 12
    #     # 8 bins
    #     plt.hist(y_pred_prob, bins=8)
    #
    #     # x-axis limit from 0 to 1
    #     plt.xlim(0, 1)
    #     plt.title('Histogram of predicted probabilities')
    #     plt.xlabel('Predicted probability of treatment')
    #     plt.ylabel('Frequency')
    #
    # # predict treatment if the predicted probability is greater than 0.3
    # # it will return 1 for all values above 0.3 and 0 otherwise
    # # results are 2D so we slice out the first column
    # y_pred_prob = y_pred_prob.reshape(-1, 1)
    # y_pred_class = binarize(y_pred_prob, 0.3)[0]
    #
    # # print the first 10 predicted probabilities
    # print('First 10 predicted probabilities:\n', y_pred_prob[0:10])
    #
    # ##########################################
    # # ROC Curves and Area Under the Curve (AUC)
    # ##########################################
    #
    # # Question: Wouldn't it be nice if we could see how sensitivity and specificity are affected by various thresholds, without actually changing the threshold?
    # # Answer: Plot the ROC curve!
    #
    # # AUC is the percentage of the ROC plot that is underneath the curve
    # # Higher value = better classifier
    # roc_auc = metrics.roc_auc_score(y_test, y_pred_prob)
    #
    # # IMPORTANT: first argument is true values, second argument is predicted probabilities
    # # we pass y_test and y_pred_prob
    # # we do not use y_pred_class, because it will give incorrect results without generating an error
    # # roc_curve returns 3 objects fpr, tpr, thresholds
    # # fpr: false positive rate
    # # tpr: true positive rate
    # fpr, tpr, thresholds = metrics.roc_curve(y_test, y_pred_prob)
    # if plot == True:
    #     plt.figure()
    #
    #     plt.plot(fpr, tpr, color='darkorange', label='ROC curve (area = %0.2f)' % roc_auc)
    #     plt.plot([0, 1], [0, 1], color='navy', linestyle='--')
    #     plt.xlim([0.0, 1.0])
    #     plt.ylim([0.0, 1.0])
    #     plt.rcParams['font.size'] = 12
    #     plt.title('ROC curve for treatment classifier')
    #     plt.xlabel('False Positive Rate (1 - Specificity)')
    #     plt.ylabel('True Positive Rate (Sensitivity)')
    #     plt.legend(loc="lower right")
    #     plt.show()
    #
    # # define a function that accepts a threshold and prints sensitivity and specificity
    # def evaluate_threshold(threshold):
    #     # Sensitivity: When the actual value is positive, how often is the prediction correct?
    #     # Specificity: When the actual value is negative, how often is the prediction correct?print('Sensitivity for ' + str(threshold) + ' :', tpr[thresholds > threshold][-1])
    #     print('Specificity for ' + str(threshold) + ' :', 1 - fpr[thresholds > threshold][-1])
    #
    # # One way of setting threshold
    # predict_mine = np.where(y_pred_prob > 0.50, 1, 0)
    # confusion = metrics.confusion_matrix(y_test, predict_mine)
    # print(confusion)
    return metrics.roc_auc_score(y_test, y_pred_class)

def evaluate(args):
    with open(args.config, "r") as f:
        config = yaml.load(f)

    config = config['evaluate_model']
    path = config['path_to_tmo']
    with open(path, 'rb') as output:
        forest = pickle.load(output)
        print('model loaded successfully')

    ##load test set
    X = pd.read_csv(config['dataset']['X'], index_col=0)
    y = pd.read_csv(config['dataset']['y'], index_col=0)
    y = y['treatment']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=config['split_data']['test_size'],
                                                        random_state= int(config['split_data']['random_state']))



    # make class predictions for the testing set
    y_pred_class = forest.predict(X_test)

    accuracy_score = evalClassModel(X,y,forest, y_test, y_pred_class, True)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('--config', default= 'config/config.yml',help='path to yaml file with configurations')

    args = parser.parse_args()

    evaluate(args)







