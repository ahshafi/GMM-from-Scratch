# -*- coding: utf-8 -*-
"""offline4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jML156j5ybLsQrOy_Ut5ehTp0hgQr3-X
"""
import sys
import numpy as np
from sklearn.decomposition import PCA
csv_file_path = sys.argv[1]
data = np.genfromtxt(csv_file_path, delimiter=',')

from scipy import stats

if data.shape[1] > 2:
    # data = stats.zscore(data, axis= 0)

    cov_matix = np.cov(data, rowvar= False)
    # print(cov_matix)
    # cov_matix = np.cov(data - np.sum(data, axis= 0).reshape(1, -1) / data.shape[0], rowvar= False)
    # print(cov_matix)
    u, s, v = np.linalg.svd(cov_matix.dot(cov_matix.T))
    data = data.dot(u)


import matplotlib.pyplot as plt



# Add labels and title
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Scatter Plot of Data Points')
plt.scatter(data[:, 0], data[:, 1])
plt.show()
# print(len(data))
# Show the plot

from math import nan
from matplotlib import ticker
from   scipy.stats import multivariate_normal
def plotGMM(mean, covariance_matrix):

    N    = 200
    # X    = np.linspace(np.min(data[:, 0]) - 3, np.max(data[:, 1]) + 3, N)
    # Y    = np.linspace(np.min(data[:, 1]) - 3, np.max(data[:, 1]) + 3, N)
    X = np.linspace(-20, 20, N)
    Y = np.linspace(-20, 20, N)
    X, Y = np.meshgrid(X, Y)
    pos  = np.dstack((X, Y))
    rv   = multivariate_normal(mean, covariance_matrix)
    Z    = rv.pdf(pos)
    levels = sorted(np.max(Z) * np.exp(-.5 * np.arange(0, 3, .4) ** 2))
    plt.contour(X, Y, Z, levels= levels, linewidths= 1)

def cluster(data, k, it, seed):
    np.random.seed(seed)
    data = data[:, :2]
    # print(data)
    data += np.random.rand(data.shape[0], data.shape[1]) * 1e-15
    # print(data)
    mu_lo = -100
    mu_hi = 100
    sigma_lo = 0
    sigma_hi = 100

    # mu = np.random.uniform(mu_lo, mu_hi, (k, 2))
    # sigma = np.random.uniform(sigma_lo, sigma_hi, (k, 2))

    p = np.array([np.random.uniform(0, 1, k) for _ in range(len(data))])
    p /= np.sum(p, axis= 1).reshape(-1, 1)
    # print(np.sum(p, axis= 1))
    n = np.empty(shape= k ,dtype= float)
    w = np.empty(shape= k ,dtype= float)
    for _ in range(it):
        n = np.sum(p, axis= 0)
        # print(n)
        # print(data.shape)
        # print(p.shape)
        # print(n.shape)
        mu = np.array([np.sum(data * p[:, i:i + 1], axis= 0) for i in range(k)])
        # print(mu.shape)
        mu /= n.reshape(-1, 1)

        sigma = []

        for i in range(k):
            tmp = np.random.rand(2, 2) * 1e-15
            for j in range(len(data)):
                tmp += (p[j][i] / n[i]) * (data[j] - mu[i]).reshape(-1, 1).dot((data[j] - mu[i]).reshape(1, -1))
            sigma.append(tmp)
        # sigma = np.array([sum([(p[j][i] / n[i]) * (data[j] - mu[i]).reshape(-1, 1).dot((data[j] - mu[i]).reshape(1, -1)) for j in range(len(data))]) for i in range(k)])
        sigma = np.array(sigma)
        # print(sigma.shape)
        # print(sigma)
        w = n / len(data)
        assert(np.sum(np.all(sigma < 0)) == 0), sigma
        for i in range(len(data)):
            for j in range(k):
                # print((data[j] - mu[i]).reshape(1, -1).dot(np.linalg.inv(sigma[j]).dot((data[j] - mu[i]).reshape(-1, 1))).shape)
                pw = min(0, -.5 * ((data[i] - mu[j]).reshape(1, -1).dot(np.linalg.inv(sigma[j]).dot((data[i] - mu[j]).reshape(-1, 1)))).item())
                # assert(pw <= 0)
                # np.exp(pw)
                # assert(np.linalg.det(sigma[j]) >= 0), sigma[j]
                p[i][j] = w[j] * np.exp(min(0, -.5 * ((data[i] - mu[j]).reshape(1, -1).dot(np.linalg.inv(sigma[j]).dot((data[i] - mu[j]).reshape(-1, 1)))).item())) / (2 * np.pi * abs(np.linalg.det(sigma[j])) ** .5)

        p /= np.sum(p, axis= 1).reshape(-1, 1)
        # Plot the data points
        # plt.scatter(data[:, 0], data[:, 1], s= 1, label= 'data', c= 'gray')
        # plt.scatter(mu[:, 0], mu[:, 1], s= 50, label= 'mean', c= 'red')
        # for i in range(k):
        #     plotGMM(mu[i], sigma[i])
        # plt.show()
        # print(mu)

    p += np.random.rand(p.shape[0], p.shape[1]) * 1e-15
    lll = 0
    for i in range(len(data)):
        lll -= p[i].dot(np.log2(p[i]))
    print(lll)
    return lll, mu, sigma, p

seeds = [906, 240, 420, 1805016, 11801075]
col = ['red', 'blue', 'green', 'purple', 'cyan', 'black', 'orange', 'olive']

it = 50
ks = int(sys.argv[2])
kt = int(sys.argv[3])
lll = 1e15
mu = None
sigma = None
p = None
hist = []
for tk in range(ks, kt + 1):
    kll = 1e15
    for i in range(5):
        tll, tmu, tsigma, tp = cluster(data, tk, it, seeds[i])
        # print("tll", tll)
        if tll < kll:
            kll = tll
        if tll < lll:
            lll = tll
            mu = tmu
            sigma = tsigma
            p = tp
            k = tk
    print("kll", kll)
    hist.append(kll)

print(hist)
# Plot histogram
plt.hist(x= [_ for _ in range(ks, kt + 1)], weights= hist)

# Add labels and title
plt.xlabel('K')
plt.ylabel('Loglikelihood')
plt.title('K vs Loglikelihood')

# Show the plot
# plt.show()
plt.savefig(f'{csv_file_path}_k_vs_log-likelihood.jpg')
plt.clf()

print("k: ", k)
for i in range(k):
    plotGMM(mu[i], sigma[i])
for i in range(len(data)):
    plt.scatter(data[i][0], data[i][1], s= 1, label= 'data', c= col[np.argsort(p[i])[-1]])

# plt.show()
plt.savefig(f'{csv_file_path}_GMM.jpg')
