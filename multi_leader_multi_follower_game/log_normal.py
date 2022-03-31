import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
def get_trunc_lognorm( mu, sigma, data_num):
    lower, upper = mu - 2 * sigma, mu + 2 * sigma  # 截断在[μ-2σ, μ+2σ]
    X = stats.truncnorm((lower - mu) / sigma, (upper - mu) / sigma, loc=mu, scale=sigma)
    log_data = X.rvs(data_num)
    return log_data