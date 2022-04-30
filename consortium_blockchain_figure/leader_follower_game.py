import cvxpy as cvx
import numpy as np
import copy
from scipy import stats
from datetime import datetime, timedelta
import hashlib
def get_trunc_lognorm( mu, sigma, data_num):
    lower, upper = mu - 2 * sigma, mu + 2 * sigma  # 截断在[μ-2σ, μ+2σ]
    X = stats.truncnorm((lower - mu) / sigma, (upper - mu) / sigma, loc=mu, scale=sigma)
    log_data = X.rvs(data_num)
    return log_data
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
def game(num):
    global m, n
    # m 代表follower的数量
    m = num
    # n 代表leader的数量
    n = num
    # b_n_tol为leader所拥有的频谱资源总数
    b_n_tol = np.linspace(20, 100, n)
    # a_n 为leader的定价
    a_n = np.linspace(2, 1, n) # a_n的初始值, np.random.normal(2, 1, n)均值为2，方差为1，的n个数
    # l_m 为follower的预算
    l_m = np.random.poisson(lam = 50, size = m)
    # w_m 为follower收益函数的系数
    w_m = get_trunc_lognorm(10, 2, m)
    # g_m 为follower资源的利用率
    g_m = get_trunc_lognorm(0.8, 0.05, m)
    # leader的定价要小于wg_m中的最小值
    a_n_max_2 = min(w_m * g_m)
    # g_m_n将g_m扩展为M*N矩阵，每一行数据相同,g_m_n = [[g_1,...,g_1],[g_2,...,g_2],...[g_M,...,g_M]]
    g_m_n = np.multiply(g_m.reshape((m,1)), np.ones((1, n)))
    # c_n 为leader每带宽的成本价格
    c_n = np.random.randint(1, 2, size = n)
    # iter迭代次数
    iter = 20
    for ite in range(iter):
        # a_m_n为a_n的扩展，a_m_n = [[a_1,...,a_N],[a_1,...,a_N],...,[a_1,...,a_N]]
        a_m_n = np.zeros([m, n])
        for m_i in range(m):
            a_m_n[m_i, :] = a_n
        b_m_n = convex_follower(b_n_tol, a_m_n, l_m, w_m, g_m_n)
        # 计算第ite次迭代时，第time_m个follower的效用函数
        b_n_remained = np.sum(b_m_n, axis = 0) - b_n_tol
        a_n_max_1 = a_n_max_2 * np.exp(b_n_remained / b_n_tol)
        a_n_old = copy.copy(a_n)
        a_n = convex_leader(c_n, b_m_n, a_n_max_1, a_n_max_2)
        a_n = (a_n_old + a_n) / 2
    return b_m_n
if __name__ == '__main__':
    # start_time1为计算平均时延的开始时间，仿真2
    start_time0 = datetime.now()
    end_time0 = datetime.now()
    a = (end_time0 - start_time0).total_seconds()
    print(a)