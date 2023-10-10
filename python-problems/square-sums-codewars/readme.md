## [Square sums Kata on Codewars](https://www.codewars.com/kata/5a6b24d4e626c59d5b000066/train/python)


> Write function `square_sums_row` that, given integer number N (in range 2..43), returns array of integers 1..N arranged in a way, so sum of each 2 consecutive numbers is a square.
>
> Solution is valid if and only if following two criterias are met:
> 
> 1. Each number in range 1..N is used once and only once. 
> 2. Sum of each 2 consecutive numbers is a perfect square.
> 
> **Example:**
> For `N=15` solution could look like this: 
> `[ 9, 7, 2, 14, 11, 5, 4, 12, 13, 3, 6, 10, 15, 1, 8 ]`
> 
> If there is no solution, return False. For example if N=5, then numbers 1,2,3,4,5 cannot be put into square sums row: 1+3=4, 4+5=9, but 2 has no pairs and cannot link `[1,3]` and `[4,5]`.

In this solution, a graph is created and iteratively checked to see if the condition passes. 