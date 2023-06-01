import pickle
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import minimize, Bounds
import HIV
import graphs

dyn = "[T1(t), T2(t), I1(t), I2(t), V(t), E(t)]"
fh = [HIV.T1, HIV.T2, HIV.I1, HIV.I2, HIV.V, HIV.E]
t = [0]
x0 = np.array([163573, 5, 11945, 46, 63919, 24])
z = np.array([[1, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1, 1]])
ulb = np.array([0, 0])
urb = np.array([0.7, 0.3])


def optP(p, xi, STI, t1, t2, u_space):
    fp = 0
    li = xi - STI
    for i in range(len(p)):
        sol = solve_ivp(
            fun=lambda t, y: [fi(t, *y, *u_space[i]) for fi in fh],
            t_span=(t1, t2), y0=xi, method='BDF')
        fp += p[i] * sol.y[:, -1]
    a = np.dot(li, fp)
    return np.dot(li, fp)


def EXTSHIFT(dyn, t, x0, z, ulb, urb):
    STI = []
    with open('STI.pickle', 'rb') as f:
        STI = pickle.load(f)
    index_list = [i for i in range(len(STI[0])) if STI[0][i] % 5 == 0]
    tz = STI[0]

    r = ulb.shape[0]
    u = []
    u_space = np.zeros((2 ** r, r))

    for i in range(2 ** r):
        u_buf = np.zeros((r, 1))
        for u_idx in range(r):
            u_buf[u_idx, :] = urb[u_idx] * np.array((i >> u_idx) & 1)
        u_space[i, :] = np.transpose(u_buf)

    x = np.transpose(np.array((x0, x0)))
    t = [0]

    Aeq = np.ones((1, 2 ** r))
    beq = 1
    lb = np.zeros((1, 2 ** r))
    ub = np.ones((1, 2 ** r))
    p0 = np.ones((1, 2 ** r)) / (2 ** r)

    for i in range(len(index_list) - 1):
        print(tz[index_list[i]])
        xi = x0
        t1 = tz[index_list[i]]
        t2 = tz[index_list[i + 1]]
        f = lambda p: optP(p, xi, [fi[index_list[i]] for fi in STI[1:]], t1,
                           t2, u_space)
        res = minimize(f, p0,
                       method='SLSQP',
                       constraints=[{'type': 'eq',
                                     'fun': lambda p: np.dot(Aeq, p) - beq}],
                       bounds=Bounds(lb.transpose(), ub.transpose()))
        # res = minimize(f, p0, constraints=(
        #    {'type': 'eq', 'fun': lambda p: np.sum(p) - 1}), method='SLSQP',
        #               bounds=[(0, 1) for k in range(2 ** r)])
        p = res.x

        rand_p = np.random.rand(1, 1)
        sum_p = 0
        u_ext = []
        for j in range(p.shape[0]):
            if sum_p <= rand_p < (sum_p + p[j]):
                u_ext = u_space[j, :]
                break
            sum_p += p[j]

        # tval, x0, info = odeint(fh, x0, [tz[i], tz[i + 1]], args=(u_ext,),
        #                        full_output=True)
        sol = solve_ivp(fun=lambda t, y: [fi(t, *y, *u_ext) for fi in fh],
                        t_span=(tz[index_list[i]], tz[index_list[i + 1]]),
                        y0=x0, method='BDF')
        x = np.append(x, sol.y[:, 1:], axis=1)
        x0 = sol.y[:, -1]
        t.extend(sol.t[1:])
        u.append([u_ext])

    '''
    for ind in range(1, len(t)):
        if abs(t[ind - 1] - t[ind]) < 1e-9:
            t[ind] = t[ind] + 1e-9
    '''
    return t, x[:, 1:], u


t, x, u = EXTSHIFT(dyn, t, x0, z, ulb, urb)

with open('EXTSHIFT.pickle', 'wb') as p:
    pickle.dump([t, x, u], p)

graphs.draw(t, x[0, :], x[1, :], x[2, :], x[3, :], x[4, :], x[5, :])
