import numpy as np
from scipy.optimize import minimize

dyn = "[T1(t), T2(t), I1(t), I2(t), V(t), E(t)]"
t = [0]
x0 = np.array([1, 1, 1, 1, 1, 1, 1])
tz = np.array([0])
z = [[1, 1, 1, 1, 1, 1],
     [1, 1, 1, 1, 1, 1]]
ulb = np.array([[0, 0], [0, 0], [0, 0]])
urb = np.array([[0, 0], [0, 0], [0, 0]])


def EXTSHIFT(dyn, t, x0, tz, z, ulb, urb):
    fh = eval('lambda t,x,u : ' + dyn)  # создаем функцию из строки

    r = ulb.shape[1]
    u = []
    u_space = np.zeros((2 ** r, r))

    for i in range(2 ** r):
        u_buf = np.zeros((r, 1))
        for u_idx in range(r):
            u_buf[u_idx, :] = urb[u_idx] * np.array(
                [(i >> u_idx) & 1])
            u = u_buf[u_idx, :]
            u[u == 0] = ulb[u_idx]
        u_space[i, :] = np.transpose(u_buf)

    n = x0.shape[1]
    x = np.empty((0, n))
    t = np.empty((0, 1))

    Aeq = np.ones((1, 2 ** r))
    beq = 1
    lb = np.zeros((1, 2 ** r))
    ub = np.ones((1, 2 ** r))
    p0 = np.ones((1, 2 ** r)) / (2 ** r)

    for i in range(tz.shape[0] - 1):
        xi = x0
        zi = np.transpose(z[i, :])
        F = np.zeros((2 ** r, n))
        for j in range(2 ** r):
            F[j, :] = np.transpose(fh(tz[i], xi, u_space[j, :]))
        res = minimize(lambda p: optP(p, xi, zi, F), p0, constraints=(
            {'type': 'eq', 'fun': lambda p: np.sum(p) - 1}), method='SLSQP',
                       bounds=[(0, 1) for k in range(2 ** r)])
        p = res.x

        rand_p = np.random.rand(1, 1)
        sum_p = 0
        u_ext = []
        for j in range(p.shape[0]):
            if rand_p >= sum_p and rand_p < (sum_p + p[j]):
                u_ext = u_space[j, :]
                break
            sum_p += p[j]

        tval, x0, info = odeint(fh, x0, [tz[i], tz[i + 1]], args=(u_ext,),
                                full_output=True)
        x = np.append(x, x0, axis=0)
        x0 = np.transpose(np.array([x0[-1, :]]))
        t = np.append(t, tval, axis=0)
        u = np.append(u, np.array([u_ext]), axis=0)

    for ind in range(1, t.shape[0]):
        if abs(t[ind - 1] - t[ind]) < 1e-9:
            t[ind] = t[ind] + 1e-9
    return t, x, u


def optP(p, x, z, F):
    N = x.shape[0]
    K = F.shape[0]
    dec_fact = 0.99
    p_norm = np.divide(p, np.dot(np.ones((1, K)), np.transpose(np.array([p]))))
    val = 0
    for i in range(N):
        val_term = dec_fact ** i
        f0 = np.dot(p_norm, F[:, i])
        val -= val_term * np.log(f0)
    val *= -1
    return val


EXTSHIFT(dyn, t, x0, tz, z, ulb, urb)
