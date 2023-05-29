# How to increase the model accuracy of logistic regression


# 1. Add polynomial features
# 2. Remove outliers
# 3. Feature normalization

import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.linear_model import LogisticRegression

# read data
data = pd.read_csv("https://gist.githubusercontent.com/abyalias/3de80ab7fb93dcecc565cee21bd9501a/raw/d9d70f7e16082b09850aa545db86897c68ac3e71/gpa_final.csv", sep='\t')

# split into train and test data
xtrain, xtest = train_test_split(data, random_state=2)

# boxplot
# sns.boxplot(x='admit', y='gre', data=xtrain);

# remove outliers from training set
ztrain = xtrain.query("not ((admit==1 and gre < 350) or (admit==0 and gre>=800))")

# split into x and y variables
ytrain = ztrain.pop('admit')
ytest = xtest.pop('admit')

# normalize the data
sc = StandardScaler()
ztrain = sc.fit_transform(ztrain)
ztest = sc.transform(xtest)

# add polynomial features
poly = PolynomialFeatures(degree=4)
ztrain = poly.fit_transform(ztrain)
ztest = poly.transform(ztest)

# model
clf = LogisticRegression(penalty='none', max_iter=1000)
clf.fit(ztrain, ytrain)

# checking accuracy
print("Train accuracy =", clf.score(ztrain, ytrain))   # 0.7665505226480837
print("Test accuracy  =", clf.score(ztest, ytest))     # 0.76