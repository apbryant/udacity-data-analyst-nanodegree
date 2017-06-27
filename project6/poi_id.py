#!/usr/bin/python

import sys
import pickle
sys.path.append("../tools/")
import numpy as np
import matplotlib.pyplot as plt
from functions import *

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
#features_list = ['poi','salary', 'total_payments', 'total_stock_value', 'exercised_stock_options', 'poi_messages', 'from_poi_fraction', 'to_poi_fraction' ] # You will need to use more features
#features_list = ['poi','salary', 'total_payments', 'total_stock_value', 'exercised_stock_options', 'from_poi_to_this_person', 'from_this_person_to_poi' ] # You will need to use more features
features_list = (['poi', 'salary', 'deferral_payments',
                  'total_payments', 'loan_advances', 'bonus',
                  'restricted_stock_deferred', 'deferred_income',
                  'total_stock_value', 'expenses',
                  'exercised_stock_options', 'other',
                  'long_term_incentive', 'restricted_stock',
                  'director_fees','to_messages', 
                  'from_poi_to_this_person', 'from_messages',
                  'from_this_person_to_poi', 'shared_receipt_with_poi',
                  'poi_messages', 'from_poi_fraction',
                  'to_poi_fraction'])
features_list = (['poi', 'salary', 'deferral_payments',
                  'total_payments', 'loan_advances', 'bonus',
                  'restricted_stock_deferred', 'deferred_income',
                  'total_stock_value', 'expenses',
                  'exercised_stock_options', 'other',
                  'long_term_incentive', 'restricted_stock',
                  'director_fees','to_messages', 
                  'from_poi_to_this_person', 'from_messages',
                  'from_this_person_to_poi', 'shared_receipt_with_poi'])
                 
### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

counter = 0
for value in data_dict.values():
    if value['poi']:
        counter += 1

### Task 2: Remove outliers

del data_dict['TOTAL']
del data_dict['THE TRAVEL AGENCY IN THE PARK']
del data_dict['LOCKHART EUGENE E']

# Turn 'NaN' values to 0

salary = []
total_payments = []

# turn NaNs to 0
salary, total_payments = nanToNumber(
        salary, total_payments, 'salary', 'total_payments', data_dict)

# reshape the lists
salary, total_payments = reshape(salary, total_payments)

# create a regression prediction line
predictions = plotWithPrediction(salary, total_payments)

# clean the outliers from the lists   
salary, total_payments, errors = cleanAndPlot(
        predictions, salary, total_payments)

# remove the outliers from the main dictionary
removeOutliersFromDict(
        salary, total_payments, 'salary', 'total_payments', data_dict)


# from and to poi email outlier removal

from_poi = []
to_poi = []

from_poi, to_poi = nanToNumber(
        from_poi, to_poi, 
        'from_poi_to_this_person', 'from_this_person_to_poi',
        data_dict)

from_poi, to_poi = reshape(from_poi, to_poi)

predictions = plotWithPrediction(from_poi, to_poi)

from_poi, to_poi, errors = cleanAndPlot(
        predictions, from_poi, to_poi)

removeOutliersFromDict(from_poi, to_poi, 
                       'from_poi_to_this_person', 'from_this_person_to_poi', 
                       data_dict)

# total stock value and exercised stock options outlier removal

total_stock_value = []
exercised_stock_options = []

total_stock_value, exercised_stock_options = nanToNumber(
        total_stock_value, exercised_stock_options,
        'total_stock_value', 'exercised_stock_options',
        data_dict)

total_stock_value, exercised_stock_options = reshape(
        total_stock_value, exercised_stock_options)

predictions = plotWithPrediction(total_stock_value, exercised_stock_options)

total_stock_value, exercised_stock_options, errors = cleanAndPlot(
        predictions, total_stock_value, exercised_stock_options)

removeOutliersFromDict(
        total_stock_value, exercised_stock_options,
        'total_stock_value', 'exercised_stock_options',
        data_dict)

### Task 3: Create new feature(s)

# create poi_messages, from_poi_fraction, and to_poi_fraction
for value in data_dict.values():
    if value['from_poi_to_this_person'] == 'NaN':
        value['from_poi_to_this_person'] = 0
    if value['from_this_person_to_poi'] == 'NaN':
        value['from_this_person_to_poi'] = 0
    if value['to_messages'] == 'NaN':
        value['to_messages'] = 0
    if value['from_messages'] == 'NaN':
        value['from_messages'] = 0
    if value['shared_receipt_with_poi'] == 'NaN':
        value['shared_receipt_with_poi'] = 0
    try:
        value['poi_messages'] = (
                float(value['from_poi_to_this_person'] +
                      value['from_this_person_to_poi'])) / (
                      value['to_messages'] + value['from_messages']) 
    except ZeroDivisionError:
        value['poi_messages'] = 0
for value in data_dict.values():
    try:
        value['from_poi_fraction'] = float(
                value['from_poi_to_this_person']) / value['from_messages'] 
    except ZeroDivisionError:
        value['from_poi_fraction'] = 0
    try:
        value['to_poi_fraction'] = float(
                value['from_this_person_to_poi']) / value['to_messages']
    except ZeroDivisionError:
        value['to_poi_fraction'] = 0

### Store to my_dataset for easy export below.
my_dataset = data_dict


### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)

from sklearn.feature_selection import SelectKBest

### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html

# Provided to give you a starting point. Try a variety of classifiers.

# import and setup

from sklearn.naive_bayes import GaussianNB
from sklearn import tree
from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, recall_score
from sklearn.model_selection import GridSearchCV, StratifiedShuffleSplit 
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler

features_train, features_test, labels_train, labels_test = train_test_split(
        features, labels, test_size=0.3, random_state=42)
scaler = MinMaxScaler()
select = SelectKBest(k = 5)
kfit = select.fit(features_test, labels_test)
score = kfit.scores_
NB = GaussianNB()

# create pipeline steps    
steps = [('scaling', scaler), ('selection', select), ('NB' , NB)]

# run the pipeline
pipeline = Pipeline(steps)

# create a list of tuples of the most important features and their scores
most_important_features = []

klist =  kfit.get_support()
for i in range(len(klist)):
    if klist[i]:
        t = (features_list[i], kfit.scores_[i])
        most_important_features.append(t)
        
most_important_features.sort(key = lambda x: x[1], reverse = True)
print most_important_features
# fit the pipeline and make test the model
clf = pipeline.fit(features_train, labels_train)
pred = clf.predict(features_test)

print 'NB pipe accuracy:', clf.score(features_test, labels_test)
print 'NB pipe precision:', precision_score(labels_test, pred)
print 'NB pipe recall:', recall_score(labels_test, pred)

### Task 5: Tune your classifier to achieve better than .3 precision and recall 
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info: 
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

# Example starting point. Try investigating other evaluation techniques!


### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf, my_dataset, features_list)