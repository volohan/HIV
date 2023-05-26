from scipy.integrate import solve_ivp, quad, simps
import pickle
import numpy as np
import HIV
import graphs

ulb = np.array([0, 0])
urb = np.array([0.7, 0.3])
x0 = [163573, 5, 11945, 46, 63919, 24]
fh = [HIV.T1, HIV.T2, HIV.I1, HIV.I2, HIV.V, HIV.E]
Q = 0.1
R1 = 20000
R2 = 20000
S = 1000
s = 5
l = 20
tf = 1000


def _opt_J(t, Vt, Et, u):
    f_Vt = simps(Vt, t)
    f_Et = simps(Et, t)
    J = Q * f_Vt - S * f_Et
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
        for i in range(u_space.shape[0]):
            sol = solve_ivp(
                fun=lambda t, y: [fi(t, *y, *u_space[i, :]) for fi in fh],
                t_span=(tz, tz + s), y0=x[:, -1], method='BDF')
            _recursive(tz + s, [*t, *sol.t[1:]],
                       np.column_stack((x, sol.y[:, 1:])), [*u, u_space[i, :]],
                       u_space, res)
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

    J_min = 0
    result = [[[], np.column_stack((x0.copy(), x0.copy())), []]]
    for t in range(0, tf, l):
        print(t)
        res = []
        _recursive(t, [t], np.column_stack(
            (result[-1][1][:, -1], result[-1][1][:, -1])), [], u_space, res)
        J_res = [_opt_J(r[0], r[1][4, :], r[1][5, :], r[2]) for r in res]
        min_J = min(J_res)
        d = {(0.0, 0.0): '0', (0.7, 0.0): '1', (0.0, 0.3): '2',
             (0.7, 0.3): '3'}
        t = int(''.join([d[(i[0], i[1])] for i in min_J[1]]), 4)
        result.append(res[t])
        J_min += min_J[0]

    result = result[1:]
    with open('STI.pickle', 'wb') as f:
        pickle.dump(result, f)

    t = [0]
    f1 = [x0[0]]
    f2 = [x0[1]]
    f3 = [x0[2]]
    f4 = [x0[3]]
    f5 = [x0[4]]
    f6 = [x0[5]]
    for i in result:
        t.extend(i[0][1:])
        f1.extend(i[1][0, 1:])
        f2.extend(i[1][1, 1:])
        f3.extend(i[1][2, 1:])
        f4.extend(i[1][3, 1:])
        f5.extend(i[1][4, 1:])
        f6.extend(i[1][5, 1:])

    print(J_min)
    graphs.draw(t, f1, f2, f3, f4, f5, f6)


STI()
