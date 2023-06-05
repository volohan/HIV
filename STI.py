from scipy.integrate import solve_ivp, quad
import pickle
import numpy as np
import HIV

d = {(0.0, 0.0): '0', (0.0, 0.3): '1', (0.7, 0.0): '2', (0.7, 0.3): '3'}
x0 = [163573, 5, 11945, 46, 63919, 24]
xf = [967839, 621, 76, 6, 415, 353108]
fh = [HIV.T1, HIV.T2, HIV.I1, HIV.I2, HIV.V, HIV.E]
Q = 0.1
R1 = 20000
R2 = 20000
S = 1000
s = 5
l = 20
tf = 1000


def _opt_J(t, Vt, Et, u):
    J = Q * ((Vt - xf[-2]) ** 2) + S * ((Et - xf[-1]) ** 2)
    for t_s in range(int(t[0]), int(t[-1]), s):
        t_u = int((t_s % l) / s)
        integral, _ = quad(lambda x: R1 * u[t_u][0] + R2 * u[t_u][1], t_s,
                           t_s + s)
        J += integral
    return J, u


def _recursive(tz, t, x, u, u_space, res):
    if len(u) == l / s:
        res.append([t, x[:, 1:], u])
    else:
        for i in range(len(u_space)):
            sol = solve_ivp(
                fun=lambda t, y: [fi(t, *y, *u_space[i]) for fi in fh],
                t_span=(tz, tz + s), y0=x[:, -1], method='BDF')
            _recursive(tz + s, [*t, *sol.t[1:]],
                       np.column_stack((x, sol.y[:, 1:])), [*u, u_space[i]],
                       u_space, res)
    return


def STI():
    u_space = [[i[0], i[1]] for i in d]

    tt = [0]
    f1 = [x0[0]]
    f2 = [x0[1]]
    f3 = [x0[2]]
    f4 = [x0[3]]
    f5 = [x0[4]]
    f6 = [x0[5]]
    uu = []
    min_J = 0
    for t in range(0, tf, l):
        print((t, t + l))
        res = []
        temp = [[f1[-1]], [f2[-1]], [f3[-1]], [f4[-1]], [f5[-1]], [f6[-1]]]
        _recursive(t, [t], np.column_stack([temp, temp]), [], u_space, res)
        min_J = min(
            [_opt_J(r[0], r[1][4, -1], r[1][5, -1], r[2]) for r in res])
        t = int(''.join([d[(i[0], i[1])] for i in min_J[1][-4:]]), 4)
        tt.extend(res[t][0][1:])
        f1.extend(res[t][1][0, 1:])
        f2.extend(res[t][1][1, 1:])
        f3.extend(res[t][1][2, 1:])
        f4.extend(res[t][1][3, 1:])
        f5.extend(res[t][1][4, 1:])
        f6.extend(res[t][1][5, 1:])
        uu.extend(res[t][2])

    with open('STI.pickle', 'wb') as p:
        pickle.dump([tt, f1, f2, f3, f4, f5, f6], p)


STI()
