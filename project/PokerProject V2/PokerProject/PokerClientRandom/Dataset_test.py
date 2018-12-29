
import socket
import random
import ClientBase
import os.path
import pandas as pd
import numpy as np
from deuces import Evaluator, Card
from sklearn.model_selection import train_test_split
from sklearn import naive_bayes
from sklearn import neighbors as nb
import warnings

warnings.filterwarnings("ignore")

# Datasets
AGENT_OPEN_DATA = np.loadtxt(open("datasets/open_agent.csv", "rb"), delimiter=",", skiprows=1)
OP1_OPEN_DATA = np.loadtxt(open("datasets/open_opponent0.csv", "rb"), delimiter=",", skiprows=1)
OP2_OPEN_DATA = np.loadtxt(open("datasets/open_opponent1.csv", "rb"), delimiter=",", skiprows=1)
OP3_OPEN_DATA = np.loadtxt(open("datasets/open_opponent2.csv", "rb"), delimiter=",", skiprows=1)
OP4_OPEN_DATA = np.loadtxt(open("datasets/open_opponent3.csv", "rb"), delimiter=",", skiprows=1)

AGENT_RESPOND_DATA = np.loadtxt(open("datasets/respond_agent.csv", "rb"), delimiter=",", skiprows=1)
OP1_RESPOND_DATA = np.loadtxt(open("datasets/respond_opponent0.csv", "rb"), delimiter=",", skiprows=1)
OP2_RESPOND_DATA = np.loadtxt(open("datasets/respond_opponent1.csv", "rb"), delimiter=",", skiprows=1)
OP3_RESPOND_DATA = np.loadtxt(open("datasets/respond_opponent2.csv", "rb"), delimiter=",", skiprows=1)
OP4_RESPOND_DATA = np.loadtxt(open("datasets/respond_opponent3.csv", "rb"), delimiter=",", skiprows=1)

OPEN_TRAINING_DATA = []
OPEN_TRAINING_ROW = []
OPEN_TARGET_DATA = []

for i in range(0, len(AGENT_OPEN_DATA), 1):
    OPEN_TARGET_DATA.append(AGENT_OPEN_DATA[i][11])
    OPEN_TRAINING_ROW.extend(AGENT_OPEN_DATA[i][1:11])
    OPEN_TRAINING_ROW.extend(OP1_OPEN_DATA[i])
    OPEN_TRAINING_ROW.extend(OP2_OPEN_DATA[i])
    OPEN_TRAINING_ROW.extend(OP3_OPEN_DATA[i])
    OPEN_TRAINING_ROW.extend(OP4_OPEN_DATA[i])
    OPEN_TRAINING_DATA.append(OPEN_TRAINING_ROW)

Xtrain, Xtest = train_test_split(OPEN_TRAINING_DATA, test_size=0.25)
Ytrain, Ytest = train_test_split(OPEN_TARGET_DATA, test_size=0.25)

print OPEN_TRAINING_DATA
print OPEN_TARGET_DATA
knn = nb.KNeighborsClassifier(n_neighbors=3, metric='cityblock')
knn.fit(Xtrain, Ytrain)
predict = knn.predict(Xtest)
actual = Ytest
print 'predicted ' + str(predict) + ', was ' + str(actual)


RESPOND_TRAINING_DATA = []
RESPOND_TARGET_DATA = AGENT_RESPOND_DATA[11:]
RESPOND_TRAINING_DATA.extend(AGENT_RESPOND_DATA[1:11])
RESPOND_TRAINING_DATA.extend(OP1_RESPOND_DATA[:])
RESPOND_TRAINING_DATA.extend(OP2_RESPOND_DATA[:])
RESPOND_TRAINING_DATA.extend(OP3_RESPOND_DATA[:])
RESPOND_TRAINING_DATA.extend(OP4_RESPOND_DATA[:])


#print RESPOND_TRAINING_DATA
#print RESPOND_TARGET_DATA
