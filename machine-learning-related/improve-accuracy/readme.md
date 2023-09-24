## How to increase the model accuracy of logistic regression in Scikit-learn in python?

<sup> This post is based on my answer to a Stack Overflow question that may be found [here](https://stackoverflow.com/a/75701518/19123103).</sup>

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