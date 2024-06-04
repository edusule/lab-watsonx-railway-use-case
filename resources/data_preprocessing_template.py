# Data Preprocessing Template

# Importing the libraries
import numpy as np
import pandas as pd

# Importing the dataset
dataset = pd.read_csv('raw_data/Student_Performance.csv')

dataset_test = dataset.sample(frac=0.2)  # Getting 2 rows with Exited = 1

# The rest of the data will be used for training
dataset_train = dataset.drop(dataset_test.index)

# Saving the datasets
dataset_test.to_csv('output_data/test_data_students.csv', index=False)
dataset_train.to_csv('output_data/train_data_students.csv', index=False)