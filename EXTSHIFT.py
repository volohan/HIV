import pickle
import numpy as np
import HIV
from scipy.optimize import LinearConstraint, differential_evolution
from scipy.integrate import solve_ivp


def opt_p(p, xi, sti, t1, fh, u_space):
    fp = [0, 0, 0, 0, 0, 0]
    li = xi - sti
    for i in range(len(p)):
        fp = [i + j for i, j in
              zip(fp, [p[i] * fi(t1, *xi, *u_space[i]) for fi in fh])]
    return np.dot(li, fp)


def EXTSHIFT(fh, x0, ulb, urb, signal=None):
    with open('STI.pickle', 'rb') as f:
        sti = pickle.load(f)
    index_list = [i for i in range(len(sti[0])) if sti[0][i] % 5 == 0]
    tz = sti[0]
    r = ulb.shape[0]
    u_space = np.zeros((2 ** r, r))

    for i in range(2 ** r):
        u_buf = np.zeros((r, 1))
        for u_idx in range(r):
            u_buf[u_idx, :] = urb[u_idx] * np.array((i >> u_idx) & 1)
        u_space[i, :] = np.transpose(u_buf)

    x = np.transpose(np.array((x0, x0)))
    t = [0]
    u = []
    p0 = np.array(np.ones((1, 2 ** r)) / (2 ** r))
    xi = x0
    for i in range(len(index_list) - 1):
        if signal:
            signal.emit(
                f"EXTSHIFT: {(tz[index_list[i]], tz[index_list[i + 1]])}",
                tz[index_list[i]])
        else:
            print((tz[index_list[i]], tz[index_list[i + 1]]))
        t1 = tz[index_list[i]]

        # Настройки метода оптимизации
        # rand1exp
        # currenttobest1exp
        # randtobest1bin
        # currenttobest1bin
        # best2bin
        strategy = 'currenttobest1exp'  # Стратегия выбора родителей
        bounds = [(0, 1)] * 4  # Нижние и верхние границы переменных
        constraints = LinearConstraint(np.ones((1, 2 ** r)), 1, 1)

        # Глобальная оптимизация с ограничениями
        res = differential_evolution(opt_p, bounds, strategy=strategy,
                                     args=(xi, [fi[index_list[i]] for fi in
                                                sti[1:]], t1, fh, u_space),
                                     constraints=constraints,
                                     x0=p0)

        '''
        best_x = np.inf
        p = []
        zx = [[1, 0, 0, 0],
              [0, 1, 0, 0],
              [0, 0, 1, 0],
              [0, 0, 0, 1],
              [0.25, 0.25, 0.25, 0.25],
              [0.4, 0.2, 0.2, 0.2],
              [0.2, 0.4, 0.2, 0.2],
              [0.2, 0.2, 0.4, 0.2],
              [0.2, 0.2, 0.2, 0.4],
              [0.94, 0.02, 0.02, 0.02],
              [0.02, 0.94, 0.02, 0.02],
              [0.02, 0.02, 0.94, 0.02],
              [0.02, 0.02, 0.02, 0.94],
              [0.97, 0.01, 0.01, 0.01],
              [0.01, 0.97, 0.01, 0.01],
              [0.01, 0.01, 0.97, 0.01],
              [0.01, 0.01, 0.01, 0.97]]
        for p0 in zx:
            res_x = opt_p(p0, xi, [fi[index_list[i]] for fi in
                                   sti[1:]], t1, fh, u_space)
            if res_x < best_x:
                best_x = res_x
                p = p0
        '''

        p = res.x
        if not signal:
            print(p)
        rand_p = np.random.rand(1, 1)
        sum_p = 0
        u_ext = []
        for j in range(4):
            if sum_p <= rand_p < (sum_p + p[j]):
                u_ext = u_space[j, :]
                break
            sum_p += p[j]

        sol = solve_ivp(fun=lambda t, y: [fi(t, *y, *u_ext) for fi in fh],
                        t_span=(tz[index_list[i]], tz[index_list[i + 1]]),
                        y0=x0, method='Radau')
        x = np.append(x, sol.y[:, 1:], axis=1)
        x0 = sol.y[:, -1]
        t.extend(sol.t[1:])
        u.append([u_ext])

    return t, x[:, 1:], u


def compute(u1_max, u2_max, signal=None):
    fh = [HIV.T1, HIV.T2, HIV.I1, HIV.I2, HIV.V, HIV.E]
    x0 = np.array([163573, 5, 11945, 46, 63919, 24])
    ulb = np.array([0, 0])
    # urb = np.array([0.7, 0.3])
    urb = np.array([u1_max, u2_max])

    t, x, u = EXTSHIFT(fh, x0, ulb, urb, signal)

    with open('EXTSHIFT.pickle', 'wb') as p:
        pickle.dump([t, *x], p)


if __name__ == '__main__':
    compute(0.7, 0.3)
