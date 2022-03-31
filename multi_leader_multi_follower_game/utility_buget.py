import cvxpy as cvx
import numpy as np
import log_normal
import matplotlib.pyplot as plt
import copy
# follower层优化过程
def convex_follower(b_n_tol, a_m_n, l_m, w_m, g_m_n):
    # b_m代表follower,即需求者购买的频谱向量，b_m = { b(m,1), b(m,2), ..., b(m,N) }   sum(cvx.sum(b_m_n_convex, axis = 0) * a_n)
    b_m_n_convex = cvx.Variable(shape = (m, n), nonneg=True)
    # U_m 为follower的目标函数 np.sum(np.multiply(b_m_n, a_m_n), axis = 1)
    U_m = sum(cvx.multiply(w_m, cvx.sum(cvx.log(1 + cvx.multiply(g_m_n, b_m_n_convex)), axis = 1)) - cvx.sum(cvx.multiply(b_m_n_convex, a_m_n), axis = 1))
    object = cvx.Maximize(U_m)
    # constraints 为约束条件
    constraints = [
                   b_n_tol - cvx.sum(b_m_n_convex, axis = 0) >= 0,
                   l_m - cvx.sum(cvx.multiply(b_m_n_convex, a_m_n), axis = 1) >=0
                   ]
    prob = cvx.Problem(object, constraints)
    prob.solve(solver = cvx.ECOS)  # Returns the optimal value.
    return b_m_n_convex.value
# leader层优化过程
def convex_leader(c_n, b_m_n, a_n_max_1, a_n_max_2):
    # a_n代表leader定价向量
    a_n = cvx.Variable(shape = (n))
    # U_n 为leader的目标函数
    U_n = sum(cvx.multiply((a_n - c_n), cvx.sum(b_m_n, axis = 0)))
    object = cvx.Maximize(U_n)
    constraints = [ a_n - c_n >= 0,
                    a_n_max_1 >= a_n,
                    a_n_max_2 >= a_n
                   ]
    prob = cvx.Problem(object, constraints)
    prob.solve(solver = cvx.ECOS)  # Returns the optimal value.
    return a_n.value
def convex_leader2(c_n_1, b_m_n, tim_n):
    # a_n代表leader定价向量
    a_n_1 = cvx.Variable()
    # U_n 为leader的目标函数
    U_n = (a_n_1 - c_n_1) * cvx.sum(b_m_n[:, tim_n])
    object = cvx.Maximize(U_n)
    constraints = [ a_n_1 - c_n_1 >= 0,
                    a_n_1 <= 100]
    prob = cvx.Problem(object, constraints)
    prob.solve(solver = cvx.ECOS)  # Returns the optimal value.
    return a_n_1.value
def figure(l_m, y):
    fig, ax = plt.subplots()
    font1 = {'family': 'Times New Roman',
             'weight': 'normal',
             'size': 18,
             }
    font2 = {'family': 'Times New Roman',
             'weight': 'normal',
             'size': 13,
             }
    ax.tick_params(labelsize=12)
    # -------------两种算法能够支持的用户比例----------------------------------
    ax.set_ylabel(r'Utility of requestor $U_m$', font1)
    # ax.set_title('The bandwidth demand')
    ax.set_xlabel(r'Budget of requestor $\beta_m$', font1)
    marker = [".", "^", "x", "P"]
    ls = ["--", "-.", ":", "-"]
    # plt.savefig('fix.eps', dpi=300)  # 指定分辨率保存
    lns = ax.plot(l_m, y[0, :],  marker = "v", ls = "-", label= r"Requestor with $\omega_m$ = 5")
    for n in range(1, 5):
        lns2 = ax.plot(l_m, y[n, :], marker = marker[n-1], ls = ls[n-1], label= "Requestor with $\omega_m$ = " + str((n + 1) * 5))
        lns = lns + lns2
    labs = [l.get_label() for l in lns]
    ax.set_ylim(0, 20, 5)
    x_ticks = np.arange(0, 31, 5)
    plt.xticks(x_ticks)
    ax.legend(lns, labs, loc = 2, prop=font2, framealpha=0.8)
    ax.grid()
    ax.margins(0)
    plt.savefig('Utility_provider.eps', dpi=300)
    plt.show()

if __name__ == '__main__':
    # m 代表follower的数量
    print(cvx.installed_solvers())
    m = 60
    # n 代表leader的数量
    n = 5
    # b_n_tol为leader所拥有的频谱资源总数
    #b_n_tol = np.random.randint(10, 11, size = n).astype(np.float64)
    #b_n_tol = log_normal.get_trunc_lognorm(10, 5, n) #均值为12， 上下限为12+-5*2
    #b_n_tol= abs(np.sort(-b_n_tol))
    b_n_tol = np.linspace(60, 60, n)
    #print("leader所拥有的频谱资源总数b_n_tol:", b_n_tol)
    # b_m_n 为所有m对应n所购买的频谱
    #b_m_n = np.zeros([m,n])  # b_m_n的初始值
    # a_n 为leader的定价
    a_n = np.linspace(2, 2, n) # a_n的初始值, np.random.normal(2, 1, n)均值为2，方差为1，的n个数
    #a_n_min = copy.copy(a_n)
    #a_n = log_normal.get_trunc_lognorm(2, 1, n)
    # l_m 为follower的预算
    #l_m = np.random.randint(4, 10, size = m)
    #l_m = log_normal.get_trunc_lognorm(16, 4, m)
    l_m = np.linspace(0, 30, m)
    #print("follower的预算l_m:", l_m)
    # c_n 为leader每带宽的成本价格
    #c_n = log_normal.get_trunc_lognorm(0.2, 0.1, n)
    c_n = np.random.randint(1, 2, size = n)
    #a_n_min = c_n * ( b_n_tol / np.sum(b_n_tol) * 10)
    # iter迭代次数
    iter = 10
    # U_M_iter 为每次迭代follower的收益
    U_M_iter = np.zeros([5, m])
    a_n_iter = np.zeros([iter, n])
    for w_m_0 in range(5):
        # w_m 为follower收益函数的系数
        # w_m = log_normal.get_trunc_lognorm(10, 0, m)
        w_m = np.random.randint((w_m_0 + 1) * 5, (w_m_0 + 1) * 5 + 1, size=m)
        # print("follower收益函数的系数w_m:", w_m)
        # g_m 为follower资源的利用率
        # g_m = log_normal.get_trunc_lognorm(0.8, 0, m)
        g_m = 0.1 * np.random.randint(8, 9, size=m)
        # leader的定价要小于wg_m中的最小值
        a_n_max_2 = min(w_m * g_m)
        # g_m_n将g_m扩展为M*N矩阵，每一行数据相同,g_m_n = [[g_1,...,g_1],[g_2,...,g_2],...[g_M,...,g_M]]
        g_m_n = np.multiply(g_m.reshape((m, 1)), np.ones((1, n)))
        for ite in range(iter):
            # a_m_n为a_n的扩展，a_m_n = [[a_1,...,a_N],[a_1,...,a_N],...,[a_1,...,a_N]]
            a_m_n = np.zeros([m, n])
            for m_i in range(m):
                a_m_n[m_i, :] = a_n
            b_m_n = convex_follower(b_n_tol, a_m_n, l_m, w_m, g_m_n)
            b_n_remained = np.sum(b_m_n, axis = 0) - b_n_tol
            a_n_max_1 = a_n_max_2 * np.exp(b_n_remained / b_n_tol)
            a_n_old = copy.copy(a_n)
            a_n = convex_leader(c_n, b_m_n, a_n_max_1, a_n_max_2)
            a_n = (a_n_old + a_n) / 2
        U_M_iter[w_m_0, :] = w_m * np.sum(np.log(1 + np.multiply(g_m_n, b_m_n)), axis=1) - np.sum(np.multiply(b_m_n, a_m_n), axis = 1)
    figure(l_m, U_M_iter)
    print("结束")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
