import math

import numpy as np
import warnings
from sklearn.model_selection import train_test_split, KFold
from sklearn.model_selection import cross_val_score
from sklearn import svm, ensemble
from sklearn import neighbors as nb
from sklearn import naive_bayes as nab

# import data

#********************
#***Data specifics***
#********************
#   RANKS: 0 = highcard, 1 = onepair, 2 = twopair, 3 = 3ofakind, 4 = straight,
#          5 = flush, 6 = fullhouse, 7 = 4ofakind, 8 = straightflush
#   ACTION: fold = 0, call = 1, raise = 2, allin = 3PredictedOutcome = svc.predict(Input_test)
#   OTHER: no data = -1

warnings.filterwarnings("ignore")

Data = np.loadtxt(open("Lab4PokerData_numbersonly2.csv", "rb"), delimiter=";", skiprows=1)
print ('*******************************************')
print('Length of Total Data:', len(Data))

Train_set, Test_set = train_test_split(Data, test_size=0.2)
Input_train = Train_set[:, :29]     # input features
Targetp1_train = Train_set[:, 29]      # output labels
Targetp2_train = Train_set[:, 30]

Input_test = Train_set[:, :29]
Targetp1_test = Train_set[:, 29]
Targetp2_test = Train_set[:, 30]

print ('*******************************************')
print('Length of Train Data:', len(Train_set))
print('Length of Test Data', len(Test_set))

p1_naive = nab.GaussianNB().fit(Input_train, Targetp1_train)
p2_naive = nab.GaussianNB().fit(Input_train, Targetp2_train)
p1_knn = nb.KNeighborsClassifier(3).fit(Input_train, Targetp1_train)
p2_knn = nb.KNeighborsClassifier(3).fit(Input_train, Targetp2_train)
p1_svc = svm.SVC(kernel='linear', C=1.0).fit(Input_train, Targetp1_train)
p2_svc = svm.SVC(kernel='linear', C=1.0).fit(Input_train, Targetp2_train)

print ('*******************************************\n')
print(p1_knn)

PredictedOutcome_p1_naive = p1_naive.predict(Input_test)
PredictedOutcome_p2_naive = p2_naive.predict(Input_test)
PredictedOutcome_p1_knn = p1_knn.predict(Input_test)
PredictedOutcome_p2_knn = p2_knn.predict(Input_test)
PredictedOutcome_p1_svc = p1_svc.predict(Input_test)
PredictedOutcome_p2_svc = p2_svc.predict(Input_test)

Correct_Predictions_p1_naive = len([i for i, j in zip(PredictedOutcome_p1_naive, Targetp1_test) if i == j])
Correct_Predictions_p2_naive = len([i for i, j in zip(PredictedOutcome_p2_naive, Targetp2_test) if i == j])
Correct_Predictions_p1_knn = len([i for i, j in zip(PredictedOutcome_p1_knn, Targetp1_test) if i == j])
Correct_Predictions_p2_knn = len([i for i, j in zip(PredictedOutcome_p2_knn, Targetp2_test) if i == j])
Correct_Predictions_p1_svc = len([i for i, j in zip(PredictedOutcome_p1_svc, Targetp1_test) if i == j])
Correct_Predictions_p2_svc = len([i for i, j in zip(PredictedOutcome_p2_svc, Targetp2_test) if i == j])

print ('*******************************************')
print('Number of Correct Predictions with naive bayes:', "p1: ", Correct_Predictions_p1_naive, "p2: ", Correct_Predictions_p2_naive, 'Out_of:', len(PredictedOutcome_p1_naive),
      'Number of Test Data')
print('Accuracy of Prediction in Percent with naive bayes: ', "p1: ", (Correct_Predictions_p1_naive/float(len(PredictedOutcome_p1_naive)))*100, "p2: ", (Correct_Predictions_p2_naive/float(len(PredictedOutcome_p2_naive)))*100)
print ('*******************************************\n')

print ('*******************************************')
print('Number of Correct Predictions with naive bayes:', "p1: ", Correct_Predictions_p1_svc, "p2: ", Correct_Predictions_p2_svc, 'Out_of:', len(PredictedOutcome_p1_svc),
      'Number of Test Data')
print('Accuracy of Prediction in Percent with naive bayes: ', "p1: ", (Correct_Predictions_p1_svc/float(len(PredictedOutcome_p1_svc)))*100, "p2: ", (Correct_Predictions_p2_svc/float(len(PredictedOutcome_p2_svc)))*100)
print ('*******************************************\n')


best_score = best_metric = best_k = 0.0

for k in range(1, 6):
    for metric in nb.VALID_METRICS.get('kd_tree'):
        p1_knn = nb.KNeighborsClassifier(k, weights='distance', metric=metric).fit(Input_train, Targetp1_train)
        p2_knn = nb.KNeighborsClassifier(k, weights='distance', metric=metric).fit(Input_train, Targetp2_train)

        PredictedOutcome_p1_knn = p1_knn.predict(Input_test)
        PredictedOutcome_p2_knn = p2_knn.predict(Input_test)

        Correct_Predictions_p1_knn = len([i for i, j in zip(PredictedOutcome_p1_knn, Targetp1_test) if i == j])
        Correct_Predictions_p2_knn = len([i for i, j in zip(PredictedOutcome_p2_knn, Targetp2_test) if i == j])

        print ('*******************************************')
        print ('Classifier:', p1_knn)
        print('Number of Correct Predictions', Correct_Predictions_p1_knn, 'Out_of:', len(PredictedOutcome_p1_knn),
              'Number of Test Data')
        print('Accuracy of Prediction in Percent', (Correct_Predictions_p1_knn / float(len(PredictedOutcome_p1_knn))) * 100)
        print ('*******************************************\n')
        validation_p1 = cross_val_score(p1_knn, Input_train, Targetp1_test, cv=10)
        validation_p1_avg = sum(validation_p1) / float(len(validation_p1))
        print 'cross validation score = ', validation_p1_avg
        if best_score < validation_p1_avg:
            best_score = validation_p1_avg
            best_metric = metric
            best_k = k

        print ('*******************************************')
        print ('Classifier:', p2_knn)
        print('Number of Correct Predictions', Correct_Predictions_p2_knn, 'Out_of:', len(PredictedOutcome_p2_knn),
              'Number of Test Data')
        print(
        'Accuracy of Prediction in Percent', (Correct_Predictions_p2_knn / float(len(PredictedOutcome_p2_knn))) * 100)
        print ('*******************************************\n')
        validation_p2 = cross_val_score(p2_knn, Input_train, Targetp2_test, cv=10)
        validation_p2_avg = sum(validation_p2) / float(len(validation_p2))
        print 'cross validation score = ', validation_p2_avg
        if best_score < validation_p2_avg:
            best_score = validation_p2_avg
            best_metric = metric
            best_k = k

print '\n##############################################'
print '##############################################\n'
print 'Best score', best_score, 'with k = ', best_k, '& metric = ', best_metric