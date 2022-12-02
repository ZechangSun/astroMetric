"""
astroMetric: useful function to quantify mean, scatter with respect to outlier
author: Zechang Sun [http://zechangsun.github.io]
email: szc22@mails.tsinghua.edu.cn
year: 2022
"""
import numpy as np
from typing import Optional, Tuple


def _u(delta: np.ndarray, m:float, mad:float, c: Optional[float]=6.)->np.ndarray:
    """
    used for scale estimation as in Equation (2) in arXiv:2003.01511

    """
    return (delta - m)/(c*mad)


def _cal_params(delta: np.ndarray, c: Optional[float]=6., m: Optional[float]=None)->Tuple[float, np.ndarray]:
    if m is None:
        m = np.median(delta)
    mad = np.median(np.abs(delta-m))
    u = _u(delta, m, mad, c=c)
    return m, u



def MAD(delta: np.ndarray)->float:
    r"""
    Median Absolutie Deviation (MAD)

    $$
    MAD(delta) = MEDIAN(|delta-|delta||) 
    $$
    """
    m = np.median(np.abs(delta))
    return np.median(np.abs(delta-m))


def biweight_mean(delta, niter: Optional[int]=10, threshold: Optional[float]=1e-3, c: Optional[float]=6.)->float:
    """
    bi-weighted mean defined as Equation (1) in arXiv: 2003.01511
    """
    m, u = _cal_params(delta, c=c)
    b = 0
    for _ in range(niter):
        b0 = b
        sigu = np.abs(u)<1.
        d, u = delta[sigu], u[sigu]
        b = m + np.sum((d-m)*(1-u*u)*(1-u*u))/np.sum((1-u*u)*(1-u*u))
        m, u = _cal_params(delta, b, c=c)
        if np.abs(b-b0)/b < threshold:
            return b
    return b
    

def biweight_scatter(delta, niter: Optional[int]=10, threshold: Optional[float]=1e-3, c: Optional[float]=9.)->Tuple[float, float]:
    """
    bi-weighted scatter defined as Equation (3) in arXiv: 2003.01511
    """
    m, u = _cal_params(delta, c=c)
    b, s = 0, 0
    N = delta.shape[0]
    for _ in range(niter):
        s0 = s
        sigu = np.abs(u)<1.
        d, u = delta[sigu], u[sigu]
        b = m + np.sum((d-m)*(1-u*u)*(1-u*u))/np.sum((1-u*u)*(1-u*u))
        s = np.sqrt(np.sum(N*(d-m)*(d-m)*(1-u*u)**4))/np.abs((1-u*u)*(1-5*u*u))
        m, u = _cal_params(delta, m=b, c=c)
        if np.abs(s-s0)/s < threshold:
            return b, s
    return b, s


def outlier_rate(delta: np.ndarray, threshold=0.15)->float:
    r"""
    Outlier rate defined as Equation (11) in arXiv:1704.05988

    $$
    f_{outlier} = N(|delta|>threshold)/N_{total}
    $$
    """
    Ntotal = delta.shape[0]
    Noutlier = np.sum(np.abs(delta)>threshold)
    return Noutlier/Ntotal


def biweight_outlier_rate(delta: np.ndarray, nsigma: Optional[float]=2., niter: Optional[int]=10, threshold: Optional[float]=1e-3, c: Optional[float]=9.)->float:
    r"""
    bi-weighted outlier rate defined as Equation (5) in arXiv: 2003.01511
    """
    b, s = biweight_scatter(delta, niter, threshold, c)
    Ntotal = delta.shape[0]
    Noutlier = np.sum(np.abs(delta-b)>nsigma*s)
    return Noutlier/Ntotal


def loss(delta: np.ndarray, gamma: Optional[float]=0.15)->np.ndarray:
    r"""
    Loss function defined as Equation (12) in arXiv:1704.05988
    
    $$
        L(delta) = 1 - \frac{1}{1+(delta/gamma)^2}
    $$
    """
    return 1 - 1/(1+(delta*delta)/(gamma*gamma))