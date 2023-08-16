## Project Euler #8

<sup>This is copied from my answer to a Stack Overflow question that may be found [here](https://stackoverflow.com/a/74454124/19123103).</sup>

[Project Euler's Problem #8 states](https://projecteuler.net/problem=8):

> Find the greatest product of five consecutive digits in the 1000-digit number:
> 
> The four adjacent digits in the 1000-digit number that have the greatest product are 9 x 9 x 8 x 9 = 5832.
> 
> 73167176531330624919225119674426574742355349194934
> 96983520312774506326239578318016984801869478851843
> 85861560789112949495459501737958331952853208805511
> 12540698747158523863050715693290963295227443043557
> 66896648950445244523161731856403098711121722383113
> 62229893423380308135336276614282806444486645238749
> 30358907296290491560440772390713810515859307960866
> 70172427121883998797908792274921901699720888093776
> 65727333001053367881220235421809751254540594752243
> 52584907711670556013604839586446706324415722155397
> 53697817977846174064955149290862569321978468622482
> 83972241375657056057490261407972968652414535100474
> 82166370484403199890008895243450658541227588666881
> 16427171479924442928230863465674813919123162824586
> 17866458359124566529476545682848912883142607690042
> 24219022671055626321111109370544217506941658960408
> 07198403850962455444362981230987879927244284909188
> 84580156166097919133875499200524063689912560717606
> 05886116467109405077541002256983155200055935729725
> 71636269561882670428252483600823257530420752963450
> 
> Find the thirteen adjacent digits in the 1000-digit number that have the greatest product. What is the value of this product?



This solution computes the product in each iteration by using the product from the previous iteration, so there's no need to re-compute most of it (saves a loop over each window). To do that, it uses `deque` from the built-in `collections` module to keep a running window that allows to drop elements from each window efficiently. 

The basic idea is, in each iteration, divide the product from the previous iteration by the first number used in its computation and multiply it by the number in the current iteration - similar to moving the window one slot to the right.

The main difficulty is that any number multiplied by 0 is 0, so once 0 enters a window, the product of the remaining numbers are lost. To recover that, two separate products are kept in each iteration: `prod` (which is the true running product) and `after_zero` (which is the product of non-zero numbers *after* a 0), and `after_zero` is assigned back to `prod` once the window doesn't contain a zero anymore.

The solution may be found on the current repo [here](./solution_for_str.py).


If `num` is an integer instead of a string, the following works in a very similar way; only, it starts from the end by iteratively dividing the integer by 10 to get the individual digits; so instead of moving the window to the right, it moves it to the left in each iteration.

This solution may be found on the current repo [here](./solution_for_int.py).


Output:

```python
print(greatest_product(num, 13))
# 23514624000
```