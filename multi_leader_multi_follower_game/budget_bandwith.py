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
def figure(y):
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
    ax.set_ylabel(r'Bought bandwith', font1)
    x = np.arange(0, cycle_index * l_m_gap, l_m_gap)
    # ax.set_title('The bandwidth demand')
    ax.set_xlabel(r'Budget of one BOP', font1)
    marker = [".", "^", "x", "P", "s"]
    ls = ["--", "-.", ":", "-", "solid"]
    # plt.savefig('fix.eps', dpi=300)  # 指定分辨率保存
    linewidth = 2
    lns = ax.plot(x, np.sum(y, axis = 1),  marker = "v", ls = "-", linewidth = linewidth, label= r"Total bought bandwith")
    for n_0 in range(0, n):
        lns2 = ax.plot(x, y[:, n_0], marker = marker[n_0], ls = ls[n_0], linewidth = linewidth, label= r" Bought bandwith from SOP " + str(n_0+1))
        lns = lns + lns2
    labs = [l.get_label() for l in lns]
    ax.set_ylim(0, 2.5, 0.5)
    x_ticks = np.arange(0, cycle_index * l_m_gap, l_m_gap * 4)
    plt.xticks(x_ticks)
    ax.legend(lns, labs, loc = 'lower left', bbox_to_anchor = (0.4, 0.6),  prop=font2, framealpha=0.5)
    ax.grid()
    ax.margins(0)
    plt.savefig('E:\cloud files\Students\lizuguang\my papers\preparing\IEEEtran\Figure\\bandwith_budget.eps', dpi=300)
    plt.show()

if __name__ == '__main__':
    # m 代表follower的数量
    print(cvx.installed_solvers())
    m = 30
    # n 代表leader的数量
    n = 3
    # b_n_tol为leader所拥有的频谱资源总数
    #b_n_tol = np.random.randint(10, 11, size = n).astype(np.float64)
    #b_n_tol = log_normal.get_trunc_lognorm(10, 5, n) #均值为12， 上下限为12+-5*2
    #b_n_tol= abs(np.sort(-b_n_tol))
    b_n_tol = np.linspace(40, 120, n)
    #print("leader所拥有的频谱资源总数b_n_tol:", b_n_tol)
    # b_m_n 为所有m对应n所购买的频谱
    #b_m_n = np.zeros([m,n])  # b_m_n的初始值
    # a_n 为leader的定价
    a_n = np.linspace(2, 2, n) # a_n的初始值, np.random.normal(2, 1, n)均值为2，方差为1，的n个数
    #a_n_min = copy.copy(a_n)
    #a_n = log_normal.get_trunc_lognorm(2, 1, n)
    # l_m 为follower的预算
    #l_m = np.random.randint(4, 10, size = m)
    #l_m = log_normal.get_trunc_lognorm(20, 4, m)
    l_m = np.random.poisson(lam = 20, size = m)
    #print("follower的预算l_m:", l_m)
    # w_m 为follower收益函数的系数
    #w_m = log_normal.get_trunc_lognorm(10, 2, m)
    w_m = np.random.randint(10,11, size = m)
    #print("follower收益函数的系数w_m:", w_m)
    # g_m 为follower资源的利用率
    #g_m = log_normal.get_trunc_lognorm(0.8, 0.05, m)
    g_m = 0.1 * np.random.randint(8, 9, size = m)
    # leader的定价要小于wg_m中的最小值
    a_n_max_2 = min(w_m * g_m)
    # g_m_n将g_m扩展为M*N矩阵，每一行数据相同,g_m_n = [[g_1,...,g_1],[g_2,...,g_2],...[g_M,...,g_M]]
    g_m_n = np.multiply(g_m.reshape((m,1)), np.ones((1, n)))
    # c_n 为leader每带宽的成本价格
    #c_n = log_normal.get_trunc_lognorm(0.2, 0.1, n)
    c_n = np.random.randint(1, 2, size = n)
    #a_n_min = c_n * ( b_n_tol / np.sum(b_n_tol) * 10)
    # iter迭代次数
    iter = 15
    cycle_index = 21
    l_m_gap = 2
    bandwith_m0 = np.zeros([cycle_index, n])
    for l_m_0 in range(cycle_index):
        l_m[0] = l_m_0 * l_m_gap
        for ite in range(iter):
            # a_m_n为a_n的扩展，a_m_n = [[a_1,...,a_N],[a_1,...,a_N],...,[a_1,...,a_N]]
            a_m_n = np.zeros([m, n])
            for m_i in range(m):
                a_m_n[m_i, :] = a_n
            b_m_n = convex_follower(b_n_tol, a_m_n, l_m, w_m, g_m_n)
            # 计算第ite次迭代时，第time_m个follower的效用函数
            #U_M_iter[time_m][ite] = w_m[time_m] * math.log(1 + g_m[time_m] * sum(b_m_new)) - (b_m_new @ a_n)
            b_n_remained = np.sum(b_m_n, axis = 0) - b_n_tol
            a_n_max_1 = 10 * np.exp(- b_n_tol / max(b_n_tol))
            a_n_old = copy.copy(a_n)
            a_n = convex_leader(c_n, b_m_n, a_n_max_1, a_n_max_2)
            a_n = (a_n_old + a_n) / 2
        bandwith_m0[l_m_0, :] = b_m_n[0, :]
        # 计算第ite次迭代时，第time_n个leader的效用函数
    # Tol_m 为每个需求者获得的带宽总量
    #Tol_m = np.sum(b_m_n, axis = 1)
    figure(bandwith_m0)
    print("结束")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/