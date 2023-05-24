import numpy as np
import HIV
from scipy.integrate import solve_ivp

ulb = np.array([0, 0])
urb = np.array([0.7, 0.3])
x0 = [163573, 5, 11945, 46, 63919, 24]
fh = [HIV.T1, HIV.T2, HIV.I1, HIV.I2, HIV.V, HIV.E]
s = 5
l = 20
tf = 400


def _recursive(tz, x, u, u_space, res):
    if len(u) == l / s:
        res.append([x, u])
    else:
        for i in range(u_space.shape[0]):
            sol = solve_ivp(
                fun=lambda t, y: [fi(t, *y, *u_space[i, :]) for fi in fh],
                t_span=(tz, tz + s), y0=x, method='BDF')
            _recursive(tz + s, sol.y[:, -1], [*u, u_space[i, :]], u_space, res)
    return


def STI():
    r = ulb.shape[0]
    u = []
    u_space = np.zeros((2 ** r, r))

    for i in range(2 ** r):
        u_buf = np.zeros((r, 1))
        for u_idx in range(r):
            u_buf[u_idx, :] = urb[u_idx] * np.array((i >> u_idx) & 1)
            u = u_buf[u_idx, :]
            u[u == 0] = ulb[u_idx]
        u_space[i, :] = np.transpose(u_buf)

    x = x0.copy()
    for t in range(0, tf, l):
        res = []
        _recursive(t, x0, [], u_space, res)


STI()
