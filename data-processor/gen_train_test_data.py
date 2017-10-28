from sklearn.cross_validation import train_test_split
import numpy as np
import pandas as pd

def gen_train_test_files(prefix):
    print("Gen file for " + prefix + " ...")
    input_file = prefix+".csv"
    df = pd.read_csv(input_file, header = 0, names=['label', 'message'])
    yData = df['label']
    xData = df['message']
    X_train, X_test, y_train, y_test = train_test_split(xData, yData, test_size=0.3, random_state=0)
    XY_train = pd.concat([y_train, X_train], axis=1)
    XY_test = pd.concat([y_test, X_test], axis=1)
    XY_train.to_csv(prefix+'_train.csv', index=False)
    XY_test.to_csv(prefix+'_test.csv', index=False)

gen_train_test_files('label')
gen_train_test_files('sentiment')
