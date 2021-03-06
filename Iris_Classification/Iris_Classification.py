# Make Predictions with Naive Bayes On The Iris Dataset
from csv import reader
from math import sqrt
from math import exp
from math import pi
from sklearn.metrics import accuracy_score
import numpy as np
import time
# Load a CSV file
def load_csv(filename):
	dataset = list()
	with open(filename, 'r') as file:
		csv_reader = reader(file)
		for row in csv_reader:
			if not row:
				continue
			dataset.append(row)
	return dataset

# Normalizes values in columns
def normalise(dataset):
	maxvalue = np.amax(dataset,axis = 0)#max value of first 4 columns 
	minvalue = np.amin(dataset,axis = 0)#min value of first 4 columns 
	#loops through the rows and applies the normalization equation
	for column in range(len(dataset[0])-1):
		for row in dataset:
			row[column] = (row[column]-minvalue[column])/(maxvalue[column]-minvalue[column])

# Convert string column to float
def str_column_to_float(dataset, column):
	for row in dataset:
		row[column] = float(row[column].strip())

# Convert string column to integer
def str_column_to_int(dataset, column):
	class_values = [row[column] for row in dataset]
	unique = set(class_values)
	lookup = dict()
	for i, value in enumerate(unique):
		lookup[value] = i
		print('[%s] => %d' % (value, i))
	for row in dataset:
		row[column] = lookup[row[column]]
	return lookup

# Split the dataset by class values, returns a dictionary
def separate_by_class(dataset):
	separated = dict()
	for i in range(len(dataset)):
		vector = dataset[i]
		class_value = vector[-1]
		if (class_value not in separated):
			separated[class_value] = list()
		separated[class_value].append(vector)
	return separated

# Calculate the mean of a list of numbers
def mean(numbers):
	return sum(numbers)/float(len(numbers))

# Calculate the standard deviation of a list of numbers
def stdev(numbers):
	avg = mean(numbers)
	variance = sum([(x-avg)**2 for x in numbers]) / float(len(numbers)-1)
	return sqrt(variance)

# Calculate the mean, stdev and count for each column in a dataset
def summarize_dataset(dataset):
	summaries = [(mean(column), stdev(column), len(column)) for column in zip(*dataset)]
	del(summaries[-1])
	return summaries

# Split dataset by class then calculate statistics for each row
def summarize_by_class(dataset):
	separated = separate_by_class(dataset)
	summaries = dict()
	for class_value, rows in separated.items():
		summaries[class_value] = summarize_dataset(rows)
	return summaries

# Calculate the Gaussian probability distribution function for x
def calculate_probability(x, mean, stdev):
	exponent = exp(-((x-mean)**2 / (2 * stdev**2 )))
	return (1 / (sqrt(2 * pi) * stdev)) * exponent

# Calculate the probabilities of predicting each class for a given row
def calculate_class_probabilities(summaries, row):
	total_rows = sum([summaries[label][0][2] for label in summaries])
	probabilities = dict()
	for class_value, class_summaries in summaries.items():
		probabilities[class_value] = summaries[class_value][0][2]/float(total_rows)
		for i in range(len(class_summaries)):
			mean, stdev, _ = class_summaries[i]
			probabilities[class_value] *= calculate_probability(row[i], mean, stdev)
	return probabilities

# Predict the class for a given row
def predict(summaries, row):
	probabilities = calculate_class_probabilities(summaries, row)
	best_label, best_prob = None, -1
	for class_value, probability in probabilities.items():
		if best_label is None or probability > best_prob:
			best_prob = probability
			best_label = class_value
	return best_label

#Change this boolean to turn normalization on or off
normalization_enable = True

# Make a prediction with Naive Bayes on Iris Dataset
filename = 'training.csv'
dataset = load_csv(filename)
for i in range(len(dataset[0])-1): 
	str_column_to_float(dataset, i)

# convert class column to integers
str_column_to_int(dataset, len(dataset[0])-1)
#Normalise dataset
if normalization_enable:
	normalise(dataset)
#print(dataset)
# fit model
start = time.time()
model = summarize_by_class(dataset)
end = time.time()
print('Model fitting time', end-start)
#loading the testing dataset
filename2 = 'testing.csv'
testset = load_csv(filename2)
#converting the species name into index numbers
for i in range(len(testset[0])-1):
	str_column_to_float(testset, i)

str_column_to_int(testset, len(testset[0])-1)

if normalization_enable:
	normalise(testset)

#print(testset)
#predict the label
label = []
for i in range(len(testset)):
	label.append(predict(model, testset[i])) #predicted values array
	#print('Data=%s, Predicted: %s' % (testset[i], label[i]))

label_true = [val[4] for val in testset ] #true reference values array
#print(label_true)
#Calculates the accuracy of the model

print('Data accuracy score:',accuracy_score(label_true, label,normalize =True)*100,'%')