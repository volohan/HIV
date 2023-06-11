from scipy.integrate import solve_ivp
import pickle
import numpy as np
import HIV


def STI(u1_max, u2_max, tf, s, l, signal=None):
    u_min = (0, 0)
    # u_max = (0.7, 0.3)
    u_max = (u1_max, u2_max)
    x0 = [163573, 5, 11945, 46, 63919, 24]
    xf = [967839, 621, 76, 6, 415, 353108]
    fh = [HIV.T1, HIV.T2, HIV.I1, HIV.I2, HIV.V, HIV.E]
    Q = 0.0001
    R1 = 50000
    R2 = 50000
    S = 1
    P = 100000

    # tf = 1000
    # s = 5
    # l = 20

    def Jcost(t, Vt, Et, u):
        cost = Q * ((Vt - xf[-2]) ** 2) + S * ((Et - xf[-1]) ** 2) + P * (
                tf ** 2)
        for t_s in range(int(t[0]), int(t[-1]), s):
            u_i = u[int((t_s % l) / s)]
            cost += s * (R1 * (u_i[0] ** 2) + R2 * (u_i[1] ** 2))
        return 0.5 * cost, u

    def _recursive(ti, tt, x, u, u_space, res):
        if len(u) == l / s:
            res.append([tt, x[:, 1:], u])
        else:
            for i in range(len(u_space)):
                sol = solve_ivp(
                    fun=lambda t, y: [fi(t, *y, *u_space[i]) for fi in fh],
                    t_span=(ti, ti + s), y0=x[:, -1], method='Radau')
                _recursive(ti + s, [*tt, *sol.t[1:]],
                           np.column_stack((x, sol.y[:, 1:])),
                           [*u, u_space[i]],
                           u_space, res)
        return

    u_states = {u_min: '0', (u_min[0], u_max[1]): '1',
                (u_max[0], u_min[1]): '2', u_max: '3'}
    u_space = [[i[0], i[1]] for i in u_states]

    tt = [0]
    f1 = [x0[0]]
    f2 = [x0[1]]
    f3 = [x0[2]]
    f4 = [x0[3]]
    f5 = [x0[4]]
    f6 = [x0[5]]
    uu = []
    for ti in range(0, tf, l):
        if signal:
            signal.emit(f"STI: {(ti, ti + l)}", ti)
        else:
            print((ti, ti + l))
        res = []
        xi = [[f1[-1]], [f2[-1]], [f3[-1]], [f4[-1]], [f5[-1]], [f6[-1]]]
        _recursive(ti, [ti], np.column_stack([xi, xi]), [], u_space, res)
        min_J, u_J = min(
            [Jcost(r[0], r[1][4, -1], r[1][5, -1], r[2]) for r in res])
        t = int(''.join([u_states[(i[0], i[1])] for i in u_J[-4:]]), 4)
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


if __name__ == '__main__':
    STI(0.7, 0.3, 1000, 5, 20)
