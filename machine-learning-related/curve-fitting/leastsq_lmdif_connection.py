import numpy as np
from scipy import optimize, linalg

def func(xs, *params):
    return np.array(params) @ xs

def wrap_func(func, xdata, ydata):
    def func_wrapped(params, *args):
        return func(xdata, *params) - ydata
    return func_wrapped


x = np.random.default_rng(0).normal(0,1, size=10)
y = x.copy()
x = np.array([x, x, x, x])
y = x.sum(axis=0)

res = optimize.curve_fit(func, x, y, p0=[1]*len(x), full_output=1)
print(res)


f = wrap_func(func, x, y)
res = optimize.leastsq(f, [1]*len(x), full_output=1)
print(res)


retval = optimize._minpack._lmdif(f, [1]*len(x), ((),), 1)
print(retval)


# covariance matrix computation

info = retval[-1]
perm = retval[1]['ipvt'] - 1
n = len(perm)
r = np.triu(retval[1]['fjac'].T[:n, :])
inv_triu = linalg.get_lapack_funcs('trtri', (r,))
invR, trtri_info = inv_triu(r)
print(trtri_info, end='\n\n')

invR[perm] = invR.copy()
cov_x = invR @ invR.T
print(cov_x)