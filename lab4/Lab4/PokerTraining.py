import numpy as np
from sklearn.model_selection import train_test_split, KFold
from sklearn import svm
from sklearn import neighbors as nb
from sklearn import naive_bayes as nab

# import data

# Data specifics:
#   RANKS: 0 = highcard, 1 = onepair, 2 = twopair, 3 = 3ofakind, 4 = straight, 5 = flush, 6 = fullhouse, 7 = 4ofakind, 8 = straightflush
#   ACTION: fold = 0, call = 1, raise = 2, allin = 3
#   OTHER: no data = -1

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
print('Number of Correct Predictions with naive bayes:', "p1: ", Correct_Predictions_p1_knn, "p2: ", Correct_Predictions_p2_knn, 'Out_of:', len(PredictedOutcome_p1_knn),
      'Number of Test Data')
print('Accuracy of Prediction in Percent with naive bayes: ', "p1: ", (Correct_Predictions_p1_knn/float(len(PredictedOutcome_p1_knn)))*100, "p2: ", (Correct_Predictions_p2_knn/float(len(PredictedOutcome_p2_knn)))*100)
print ('*******************************************\n')

print ('*******************************************')
print('Number of Correct Predictions with naive bayes:', "p1: ", Correct_Predictions_p1_svc, "p2: ", Correct_Predictions_p2_svc, 'Out_of:', len(PredictedOutcome_p1_svc),
      'Number of Test Data')
print('Accuracy of Prediction in Percent with naive bayes: ', "p1: ", (Correct_Predictions_p1_svc/float(len(PredictedOutcome_p1_svc)))*100, "p2: ", (Correct_Predictions_p2_svc/float(len(PredictedOutcome_p2_svc)))*100)
print ('*******************************************\n')

fold = KFold(n_splits=10)
fold.get_n_splits(Input_train)
for train_index, test_index in fold.split(Input_train):
    print("TRAIN:", train_index, "TEST:", test_index)
    X_train, X_test = Input_train[train_index], Input_train[test_index]
    y_train, y_test = Input_test[train_index], Input_test[test_index]
