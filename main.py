import numpy as np
from scipy.integrate import odeint, solve_ivp
from scipy.optimize import minimize, Bounds

dyn = "[T1(t), T2(t), I1(t), I2(t), V(t), E(t)]"
t = [0]
x0 = np.array([1, 1, 1, 1, 1, 1, 1])
tz = np.zeros((100, 1))
z = np.array([[1, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1, 1]])
ulb = np.array([111, 111])
urb = np.array([111, 111])


def optP(p, xi, zi, F):
    fp = 0
    li = xi - zi
    for i in range(p):
        fp += p[i] * F[i]
    return np.dot(li, fp)


def EXTSHIFT(dyn, t, x0, tz, z, ulb, urb):
    # fh = eval('lambda t,x,u : ' + dyn)  # создаем функцию из строки
    def fh(t, x, u):
        return np.array([1111, 1111, 11111, 1111])

    r = ulb.shape[0]
    u = []
    u_space = np.zeros((2 ** r, r))

    for i in range(2 ** r):
        u_buf = np.zeros((r, 1))
        for u_idx in range(r):
            print(np.dot(urb[u_idx], np.array((i >> u_idx) & 1)))
            u_buf[u_idx, :] = urb[u_idx] * np.array((i >> u_idx) & 1)
            u = u_buf[u_idx, :]
            u[u == 0] = ulb[u_idx]
        u_space[i, :] = np.transpose(u_buf)

    N = tz.shape[0]
    n = x0.shape[0]
    x = np.zeros(n)
    t = np.zeros((N, 1))

    Aeq = np.ones((1, 2 ** r))
    beq = 1
    lb = np.zeros((1, 2 ** r))
    ub = np.ones((1, 2 ** r))
    p0 = np.ones((1, 2 ** r)) / (2 ** r)

    for i in range(N - 1):
        xi = x0
        zi = np.transpose(z[i, :])

        F = np.zeros((2 ** r, 2 + r))
        for j in range(2 ** r):
            F[j, :] = np.transpose(fh(tz[i], xi, u_space[j, :]))
        f = lambda p: optP(p, xi, zi, F)
        # res = minimize(optP, p0, args=(xi, zi, F))
        res = minimize(optP, p0,
                       args=(xi, zi, F),
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

        #tval, x0, info = odeint(fh, x0, [tz[i], tz[i + 1]], args=(u_ext,),
        #                        full_output=True)
        sol = solve_ivp(fun=lambda t, x: fh(t, x, u_ext),
                        t_span=(tz[i], tz[i + 1]), y0=x0, method='BDF')
        x = np.append(x, x0, axis=0)
        x0 = np.transpose(np.array([x0[-1, :]]))
        t = np.append(t, tval, axis=0)
        u = np.append(u, np.array([u_ext]), axis=0)

    for ind in range(1, t.shape[0]):
        if abs(t[ind - 1] - t[ind]) < 1e-9:
            t[ind] = t[ind] + 1e-9
    return t, x, u


EXTSHIFT(dyn, t, x0, tz, z, ulb, urb)
