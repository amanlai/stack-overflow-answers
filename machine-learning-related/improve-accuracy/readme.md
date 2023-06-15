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
> I built a Logistic Regression model using scikit-learn but the ones are wrongly predicted. How do I increase the model accuracy?	   


A relatively easy way to try out is to add **polynomial features**. You can tune the degrees required.

Also, check out the benchmark model results. The confusion matrix of the benchmark model (in the OP) shows that almost no positive predictions are being made on the test data. One reason for this could be that outliers are "confusing" the model. In fact, the box plot of `admit` vs `gre` of the training data of the dataset in the OP looks as follows:

[![boxplot][1]][1]

There are people who weren't admitted even though their GRE score was 800 and there are people who were admitted even though their GRE score was less than 350. We could simply **remove these outliers** from the training dataset and train `LogisticRegression` on the trimmed data. It's important to note that you shouldn't remove anything from the test set as it's a held-out set that is assumed to be unseen data. So any outlier handling should be done only on the training set.

Also as [Abhinav Arora][2] mentioned, feature normalization is also something you can try with minimal fuss.

All in all, with very minimal additional code, the test accuracy was improved by 10 percentage points from 0.66 to 0.76.

The code may be found on this repo [here](./demo.py).

That said, for other datasets, it's very possible that adding polynomial features, normalization, handling outliers etc. simply cannot improve accuracy because the data is too limiting. In that case, you'll need to get more data to come up with more predictive features.


  [1]: https://i.stack.imgur.com/FKCCd.png
  [2]: https://stackoverflow.com/a/38083189/19123103