import pandas as pd
import pprint

df = pd.read_csv("comments_no_blank.csv", header=None)
print(df['id'])