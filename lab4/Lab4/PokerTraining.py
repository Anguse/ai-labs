import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import svm

# import data

# Data specifics:
#   ranks: 0 = highcard, 1 = onepair, 2 = twopair, 3 = 3ofakind, 4 = straight, 5 = flush, 6 = fullhouse, 7 = 4ofakind, 8 = straightflush
#   action: fold = 0, call = 1, raise = 2, allin = 3

Data = np.loadtxt(open("Lab4PokerData_numbersonly.csv", "rb"), delimiter=";", skiprows=1)
print ('*******************************************')
print('Length of Total Data:', len(Data))

Train_set, Test_set = train_test_split(Data, test_size=0.2)
Input_train = Train_set[1, :28]     # input features
Target_train = Train_set[:, 29:30]      # output labels

Input_test = Test_set[1:, :28]
Target_test = Test_set[:, 29:30]
print ('*******************************************')
print('Length of Train Data:', len(Train_set))
print('Length of Test Data', len(Test_set))
