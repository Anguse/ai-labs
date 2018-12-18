import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import svm

# import data
Data = np.loadtxt(open("Lab4Data.csv", "rb"), delimiter=";", skiprows=1)
print ('*******************************************')
print('Length of Total Data:', len(Data))

Train_set, Test_set = train_test_split(Data, test_size=0.2)
Input_train = Train_set[:, :8]     # input features
Target_train = Train_set[:, 9]  # output labels

Input_test = Test_set[:, :8]
Target_test = Test_set[:, 9]
print ('*******************************************')
print('Length of Train Data:', len(Train_set))
print('Length of Test Data', len(Test_set))


svc = svm.SVC(kernel='linear', C=1.0).fit(Input_train, Target_train)
#svc = svm.SVC(kernel='rbf', degree=3, C=1.0).fit(Input_train, Target_train)
print ('*******************************************')
print(svc)

PredictedOutcome = svc.predict(Input_test)
Number_of_Correct_Predictions = len([i for i, j in zip(PredictedOutcome, Target_test) if i == j])

print ('*******************************************')
print('Number of Correct Predictions:', Number_of_Correct_Predictions, 'Out_of:', len(PredictedOutcome),
      'Number of Test Data')
print('Accuracy of Prediction in Percent:', (Number_of_Correct_Predictions/float(len(PredictedOutcome)))*100)
