It's a post that was first posted as an answer to the following Stack Overflow question and can be found at https://stackoverflow.com/a/75701518/19123103

## How to increase the model accuracy of logistic regression in Scikit-learn in python?

> I am trying to predict the admit variable with predictors such as gre,gpa and ranks. But the prediction accuracy is very low (0.66).The dataset is given below.
>
> https://gist.github.com/abyalias/3de80ab7fb93dcecc565cee21bd9501a
> 
> The first few rows of the dataset looks like:
> ```none
>    admit  gre   gpa  rank_2  rank_3  rank_4
> 0      0  380  3.61     0.0     1.0     0.0
> 1      1  660  3.67     0.0     1.0     0.0
> 2      1  800  4.00     0.0     0.0     0.0
> 3      1  640  3.19     0.0     0.0     1.0
> 4      0  520  2.93     0.0     0.0     1.0
> 5      1  760  3.00     1.0     0.0     0.0
> 6      1  560  2.98     0.0     0.0     0.0
> ```
> 
> My code:
> ```python
> from sklearn.model_selection import train_test_split
> from sklearn.linear_model import LogisticRegression
> from sklearn.metrics import confusion_matrix, accuracy_score
> 
> y = data['admit']
> x = data[data.columns[1:]]
> 
> xtrain, xtest, ytrain, ytest = train_test_split(x, y, random_state=2)
> 
> #modelling 
> clf = LogisticRegression(penalty='l2')
> clf.fit(xtrain, ytrain)
> ypred_train = clf.predict(xtrain)
> ypred_test = clf.predict(xtest)
> 
> #checking the classification accuracy
> accuracy_score(ytrain, ypred_train)
> # 0.70333333333333337
> accuracy_score(ytest, ypred_test)
> # 0.66000000000000003
> 
> #confusion metrix...
> confusion_matrix(ytest, ypred)
> # array([[62,  1],
> #        [33,  4]])
> ```
	   

A relatively easy way to try out is to add **polynomial features**. You can tune the degrees required.

Also, check out the benchmark model results. The confusion matrix of the benchmark model (in the OP) shows that almost no positive predictions are being made on the test data. One reason for this could be that outliers are "confusing" the model. In fact, the box plot of `admit` vs `gre` of the training data of the dataset in the OP looks as follows:

[![boxplot][1]][1]

There are people who weren't admitted even though their GRE score was 800 and there are people who were admitted even though their GRE score was less than 350. We could simply **remove these outliers** from the training dataset and train `LogisticRegression` on the trimmed data. It's important to note that you shouldn't remove anything from the test set as it's a held-out set that is assumed to be unseen data. So any outlier handling should be done only on the training set.

Also as [Abhinav Arora][2] mentioned, feature normalization is also something you can try with minimal fuss.

All in all, with very minimal additional code, the test accuracy was improved by 10 percentage points from 0.66 to 0.76.

```python
import pandas as pd
# import seaborn as sns
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
```

That said, for other datasets, it's very possible that adding polynomial features, normalization, handling outliers etc. simply cannot improve accuracy because the data is too limiting. In that case, you'll need to get more data to come up with more predictive features.


  [1]: https://i.stack.imgur.com/FKCCd.png
  [2]: https://stackoverflow.com/a/38083189/19123103
The ones are wrongly predicted. How do I increase the model accuracy?