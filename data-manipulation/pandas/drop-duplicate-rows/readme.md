## Drop duplicate rows across multiple columns

<sup>This post is based on my answer to a Stack Overflow question that may be found [here](https://stackoverflow.com/a/75250654/19123103).</sup> 

Given a dataframe such as the following:

```none
    A   B   C
0   foo 0   A
1   foo 1   A
2   foo 1   B
3   bar 1   A
```
how do we drop duplicate rows across multiple columns?

---
