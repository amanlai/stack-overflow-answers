import pandas as pd
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

# make sample data
X, y = make_classification(1000, 200, n_informative=195, random_state=2023)
# split into train-test datasets
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=2023)

# normalize the data
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

# train Logistic Regression models for different values of C
# and collect train and test accuracies
scores = {}
for C in (10**k for k in range(-6, 6)):
    lr = LogisticRegression(C=C)
    lr.fit(X_train, y_train)
    scores[C] = {'train accuracy': lr.score(X_train, y_train), 
                 'test accuracy': lr.score(X_test, y_test)}

# plot the accuracy scores for different values of C
df = pd.DataFrame.from_dict(scores, 'index')
ax = df.plot(logx=True, xlabel='C', ylabel='accuracy', figsize=(7,4))
ax.figure.set_facecolor('white');