from sklearn.cross_validation import train_test_split
import numpy as np
import pandas as pd

def gen_train_test_files(file_name, class_name):
    print("Gen file for " + class_name + " ...")
    input_file = file_name+".csv"
    df = pd.read_csv(input_file, header = 0, names=['label', 'message'])
    label_name = "__label__"+class_name
    df.ix[df['label']!=label_name, 'label'] = "__label__not-"+class_name
    df.to_csv(class_name+'.csv', index=False)
    # yData = df['label']
    # xData = df['message']
    # X_train, X_test, y_train, y_test = train_test_split(xData, yData, test_size=0.3, random_state=0)
    # XY_train = pd.concat([y_train, X_train], axis=1)
    # XY_test = pd.concat([y_test, X_test], axis=1)
    # XY_train.to_csv(class_name+'_train.csv', index=False)
    # XY_test.to_csv(class_name+'_test.csv', index=False)

gen_train_test_files('label', 'complain')
gen_train_test_files('label', 'question')
gen_train_test_files('sentiment', 'positive')
gen_train_test_files('sentiment', 'negative')
