from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


x = ['2023-03-25 04:11:37', '2020-03-23 08:11:37', '2019-11-23 01:07:17', '2024-03-25 23:17:37', '2021-03-22 16:27:37']
y = [8.55, 6.55, 4.63, 10.46, 7.35]
z = [9.86, 4.95, 0.5, 6.35, 8.43]
x = [datetime.strptime(d, '%Y-%m-%d %H:%M:%S') for d in x]  # convert to datetime


xs, ys = zip(*sorted(zip(x, y)))                 # sort by date

# plot time-series
plt.plot(xs, ys);


#########################################################


# plot multiple time-series
xs, ys, zs = zip(*sorted(zip(x, y, z)))
plt.plot(xs, ys, label='y over time', color='blue')
plt.plot(xs, zs, label='z over time', color='red')
plt.legend();



#########################################################




plt.plot(xs, ys)
xmin, xmax = map(mdates.num2date, plt.xlim())               # get dates on x-limits as dates
for yr in range(xmin.year, xmax.year):
    plt.axvline(datetime(yr + 1, 1, 1), color='gray')       # vertical line on Jan 1 midnight

# show datetimes in a specific format
pos = mdates.AutoDateLocator()                   # detect tick locations automatically
fmt = mdates.DateFormatter('%Y-%m-%d')           # format the datetime with '%Y-%m-%d
plt.gca().xaxis.set(major_locator=pos, major_formatter=fmt)

# if the tick labels are too crowded, keep only a few of them
pos, labels = plt.xticks()                       # get xtick positions and labels
plt.xticks(pos[::2], labels[::2]);               # keep only every second tick