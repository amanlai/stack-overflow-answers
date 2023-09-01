## Apply a function to a dataframe which includes previous row data

<sup> This post is based on my answer to a Stack Overflow question that may be found [here](https://stackoverflow.com/q/75241163/19123103). </sup>

The specific use case is as follows.

Suppose you have a dataframe (`spend_df`) for daily fruit spend which looks like this:

```none
    Date   Apples   Pears   Grapes
01/01/22       10      47        0
02/01/22        0      22        3
03/01/22       11       0        3
...
```

For each fruit, we need to apply a function using their respective parameters and inputs spends. The function includes the previous day and the current day spends, which is as follows:

```none
y = beta(1 - exp(-(theta*previous + current)/alpha))
```

The parameters of this function is stored in another dataframe (`parameters_df`) as follows.

```none
Parameter   Apples   Pears   Grapes
    alpha      132     323       56
     beta      424      31       33
    theta       13     244      323
```

Now, we want to apply the above formula to `spend_df` using the parameters in `parameters_df`, so that the output dataframe looks like the following.

```none
    Date   Apples   Pears   Grapes     
01/01/22    30.93    4.19        0       
02/01/22   265.63   31.00     1.72
03/01/22    33.90   30.99    32.99
...     
```

---

It might be easier to read if you extract the necessary variables from `parameters_df` and `spend_df` first. Then a simple application of the formula will produce the expected output.

```python
# extract alpha, beta, theta from parameters df
alpha, beta, theta = parameters_df.iloc[:, 1:].values
# select fruit columns
current = spend_df[['Apples', 'Pears', 'Grapes']]
# find previous values of fruit columns
previous = current.shift(fill_value=0)

# calculate profit using formula
y = beta*(1 - np.exp(-(theta*previous + current) / alpha))
profit_df = spend_df[['Date']].join(y)
```
[![res][1]][1]


  [1]: https://i.stack.imgur.com/X5ifi.png