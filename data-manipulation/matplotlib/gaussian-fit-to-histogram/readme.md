## Plotting a gaussian fit to a histogram

<sup>This post is based on my answer to a Stack Overflow question that may be found [here](https://stackoverflow.com/a/76966863/19123103).</sup>

Plotting a gaussian fit onto a histogram is possible using seaborn's `distplot` as follows.
```python
import seaborn as sns
from scipy import stats
sns.distplot(data, kde=False, fit=stats.norm);
```
However, `distplot` is deprecated, so how do we fill in the gap in this functionality?

---

