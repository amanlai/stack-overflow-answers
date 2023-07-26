## How to set x-axis major and minor ticks and labels in a pandas time-series plot

<sup>This post is based on my answer to a Stack Overflow question that may be found [here](https://stackoverflow.com/a/76774571/19123103).</sup>

In matplotlib's `plot()`, the default time-series unit is 1 day but in pandas' `plot()`, 1 unit is equal to the frequency of the time-series, so if the frequency is 1 day, 1 unit is 1 day; if it is 1 hour, then it is 1 hour etc. This makes the `plot()` calls of matplotlib and pandas different when it comes to time-series data.

If **the frequency of the time-series is 1-day**, then `matplotlib.dates.WeekdayLocator`, `matplotlib.dates.MonthLocator` etc. can "locate" tick positions<sup>1</sup> because 1 day is used as the base unit to make xtick positions by pandas `plot()` (coincides with matplotlib's default).

Since pandas' `plot()` call returns an Axes object, the tick labels of that Axes object may be modified using `matplotlib.dates`.

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

idx = pd.date_range('2011-05-01', '2011-07-01', freq='D')
s1 = pd.Series(np.random.randn(len(idx)), index=idx)

ax = s1.plot(style='v-')
ax.xaxis.set(
    minor_locator=mdates.WeekdayLocator(),               # make minor ticks on each Tuesday
    minor_formatter=mdates.DateFormatter('%d\n%a'),      # format minor ticks
    major_locator=mdates.MonthLocator(),                 # make major ticks on first day of each month
    major_formatter=mdates.DateFormatter('\n\n\n%b\n%Y') # format major ticks
);
```

[![first image][1]][1]

---

However, if the frequency is not 1-day but, say, 1-week, then `matplotlib.dates` won't be able to locate the positions because, as mentioned previously, pandas' `plot()` sets the unit to be the same as the time-series frequency (1-week), which "confuses" `matplotlib.dates`. So if we try to use the same code used to set tick labels of `s1` to set the tick labels of `s2`, then we would get very wrong ticklabels.

To "solve" the problem, one way is to remove pandas' automatic tick resolution adjustment by passing `x_compat=True`. Then major/minor tick labels may be set using matplotlib's resolution; in other words, it may be set in the same way as above.

```python
idx = pd.date_range('2011-05-01', '2011-07-01', freq='W')
s2 = pd.Series(np.random.randn(len(idx)), index=idx)

ax = s2.plot(style='v-', x_compat=True, rot=0)
ax.xaxis.set(
    minor_locator=mdates.WeekdayLocator(),              # make minor ticks on each Tuesday
    minor_formatter=mdates.DateFormatter('%d'),         # format minor ticks
    major_locator=mdates.MonthLocator(),                # make major ticks on first day of each month
    major_formatter=mdates.DateFormatter('\n\n%b\n%Y')  # format major ticks
);
```

[![second image][2]][2]

Another way to get around the issue is to use matplotlib's `plot()` instead (as suggested by [@bmu][3]). Because the unit is fixed in matplotlib, we can set the tick labels as above without issue.
```python
plt.plot(s2.index, s2, 'v-')                            # use matplotlib instead
plt.gca().xaxis.set(
    minor_locator=mdates.WeekdayLocator(byweekday=0),   # make minor ticks on each Monday
    minor_formatter=mdates.DateFormatter('%d'),         # format minor ticks
    major_locator=mdates.MonthLocator(),                # make major ticks on first day of each month
    major_formatter=mdates.DateFormatter('\n\n%b\n%Y')  # format major ticks
);
```




---

<sup>1</sup> `matplotlib.dates.num2timedelta(1) == datetime.timedelta(days=1)` is True.


  [1]: https://i.stack.imgur.com/9Zq4I.png
  [2]: https://i.stack.imgur.com/d9zaA.png
  [3]: https://stackoverflow.com/a/13674286/19123103
  [4]: https://i.stack.imgur.com/O7fCf.png