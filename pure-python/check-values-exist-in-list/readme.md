## Check if values exist in a list

<sup>This post is based on my answer to a Stack Overflow question that may be found [here](https://stackoverflow.com/a/77021171/19123103).</sup>

#### Check if values exist in a list

[xslittlegrass's answer](https://stackoverflow.com/a/40963434/19123103) shows that when checking if multiple values exist in a list, converting the list into a set first and using the `in` operator on the set is much faster than using the `in` operator on lists. On the other hand, [Nico's answer](https://stackoverflow.com/a/68438122/19123103) shows that when checking if a single value exists in a list, converting the list into a set first is not worth it, as converting to a set itself is costly to begin with. Together, these answers imply that there is some number of values where converting to a set and checking if those values exist in the set becomes faster than checking if they exist in the list.

It turns out, that number is very small. The figure below shows the runtime difference between `in` on sets and `in` on lists for different numbers of values to check. As it shows, on average, if you need to check whether 5 (or more) values exist in a list, it's faster to convert that list into a set first and check on the set instead.<sup>1</sup>

[![result][1]][1]

---

#### Get their indices if values exist in a list

On the other hand, if you want to check if values exist in a list and return the indices of the values that do, then regardless of the length of the list, for small number of values, directly searching for it using `list.index()` in a try-except block is the fastest way to do it. In particular, if you want to find the index of a single value, this is the fastest option. However, on average, if there are more than 10 values to search for, then constructing an index lookup dictionary (as in [DarrylG's answer](https://stackoverflow.com/a/58844693/19123103)) is the fastest option.<sup>2</sup>

[![result2][2]][2]

---

<sup>1</sup> Code used to produce the first figure may be found [here](./first_figure.py) and that used to produce the second figure is [here](./second_figure.py).



  [1]: https://i.stack.imgur.com/uSZ7U.png
  [2]: https://i.stack.imgur.com/3tTbc.png