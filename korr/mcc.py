from .confusion import confusion
import scipy.stats
import numpy as np


def confusion_to_mcc(tn, fp, fn, tp):
    return (tp * tn - fp * fn) / np.sqrt(
        (tp + fp) * (tp + fn) * (tn + fp) * (tn + fn))


def mcc(x, axis=0):
    """Matthews correlation

    Parameters
    ----------
    x : ndarray
        dataset of binary [0,1] values

    axis : int, optional
        Variables as columns is the default (axis=0). If variables
        are in the rows use axis=1

    Returns
    -------
    r : ndarray
        Matthews correlation

    p : ndarray
        p-values of the Chi^2 test statistics

    Notes:
    ------
    (1) We cannot directly transform the Chi^2 test statistics to
    the Matthews correlation because the relationship is

         |r| = sqrt(chi2 / n)
         chi2 = r * r * n

    (2) The sign would be missing. Therefore, as a rule of thumbs,
    If you want to optimize ABS(r_mcc) then just use the Chi2/n
    directly (Divide Chi^2 by the number of observations)

    Examples:
    ---------
        import korr
        r, pval = korr.mcc(X)

    Alternatives:
    -------------
        from sklearn.metrics import matthews_corrcoef
        r = matthews_corrcoef(y_true, y_pred)
    """
    # transpose if axis<>0
    if axis is not 0:
        x = x.T

    # read dimensions and
    n, c = x.shape

    # check if enough variables provided
    if c < 2:
        raise Exception(
            "Only " + str(c) + " variables provided. Min. 2 required.")

    # allocate variables
    r = np.ones((c, c))
    p = np.zeros((c, c))

    # compute each (i,j)-th correlation
    for i in range(0, c):
        for j in range(i + 1, c):
            cm = confusion(x[:, i], x[:, j])
            r[i, j] = confusion_to_mcc(*cm.ravel().astype(float))
            r[j, i] = r[i, j]
            p[i, j] = 1 - scipy.stats.chi2.cdf(r[i, j] * r[i, j] * n, 1)
            p[j, i] = p[i, j]
    # done
    return r, p
