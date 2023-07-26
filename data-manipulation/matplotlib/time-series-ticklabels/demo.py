import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

idx = pd.date_range('2011-05-01', '2011-07-01', freq='D')
s1 = pd.Series(np.random.randn(len(idx)), index=idx)


# first plot

ax = s1.plot(style='v-')
ax.xaxis.set(
    minor_locator=mdates.WeekdayLocator(),               # make minor ticks on each Tuesday
    minor_formatter=mdates.DateFormatter('%d\n%a'),      # format minor ticks
    major_locator=mdates.MonthLocator(),                 # make major ticks on first day of each month
    major_formatter=mdates.DateFormatter('\n\n\n%b\n%Y') # format major ticks
)
ax.figure.set_facecolor('white');
ax.figure.savefig('first_image.png');


# second plot

idx = pd.date_range('2011-05-01', '2011-07-01', freq='W')
s2 = pd.Series(np.random.randn(len(idx)), index=idx)

ax = s2.plot(style='v-', x_compat=True, rot=0)
ax.xaxis.set(
    minor_locator=mdates.WeekdayLocator(),              # make minor ticks on each Tuesday
    minor_formatter=mdates.DateFormatter('%d'),         # format minor ticks
    major_locator=mdates.MonthLocator(),                # make major ticks on first day of each month
    major_formatter=mdates.DateFormatter('\n\n%b\n%Y')  # format major ticks
)
ax.figure.set_facecolor('white');
ax.figure.savefig('second_image.png');


# third plot

plt.plot(s2.index, s2, 'v-')                            # use matplotlib instead
plt.gca().xaxis.set(
    minor_locator=mdates.WeekdayLocator(byweekday=0),   # make minor ticks on each Monday
    minor_formatter=mdates.DateFormatter('%d'),         # format minor ticks
    major_locator=mdates.MonthLocator(),                # make major ticks on first day of each month
    major_formatter=mdates.DateFormatter('\n\n%b\n%Y')  # format major ticks
);
ax.figure.set_facecolor('white');
ax.figure.savefig('third_image.png');
