import numpy as np
import seaborn as sns

x_data, y_data = np.repeat(np.linspace(0, 9, 100)[None,:], 2, axis=0) + np.random.rand(2, 100)*2
sns.regplot(x=x_data, y=y_data, ci=False, line_kws={'color':'red'});
