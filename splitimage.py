import os.path

import numpy as np


def detect_peaks(x, mph=None, mpd=1, threshold=0, edge='rising',
                 kpsh=False, valley=False, show=False, ax=None, title=True):
    x = np.atleast_1d(x).astype('float64')
    if x.size < 3:
        return np.array([], dtype=int)
    if valley:
        x = -x
        if mph is not None:
            mph = -mph
    # find indices of all peaks
    dx = x[1:] - x[:-1]
    # handle NaN's
    indnan = np.where(np.isnan(x))[0]
    if indnan.size:
        x[indnan] = np.inf
        dx[np.where(np.isnan(dx))[0]] = np.inf
    ine, ire, ife = np.array([[], [], []], dtype=int)
    if not edge:
        ine = np.where((np.hstack((dx, 0)) < 0) & (np.hstack((0, dx)) > 0))[0]
    else:
        if edge.lower() in ['rising', 'both']:
            ire = np.where((np.hstack((dx, 0)) <= 0) & (np.hstack((0, dx)) > 0))[0]
        if edge.lower() in ['falling', 'both']:
            ife = np.where((np.hstack((dx, 0)) < 0) & (np.hstack((0, dx)) >= 0))[0]
    ind = np.unique(np.hstack((ine, ire, ife)))
    # handle NaN's
    if ind.size and indnan.size:
        # NaN's and values close to NaN's cannot be peaks
        ind = ind[np.in1d(ind, np.unique(np.hstack((indnan, indnan - 1, indnan + 1))), invert=True)]
    # first and last values of x cannot be peaks
    if ind.size and ind[0] == 0:
        ind = ind[1:]
    if ind.size and ind[-1] == x.size - 1:
        ind = ind[:-1]
    # remove peaks < minimum peak height
    if ind.size and mph is not None:
        ind = ind[x[ind] >= mph]
    # remove peaks - neighbors < threshold
    if ind.size and threshold > 0:
        dx = np.min(np.vstack([x[ind] - x[ind - 1], x[ind] - x[ind + 1]]), axis=0)
        ind = np.delete(ind, np.where(dx < threshold)[0])
    # detect small peaks closer than minimum peak distance
    if ind.size and mpd > 1:
        ind = ind[np.argsort(x[ind])][::-1]  # sort ind by peak height
        idel = np.zeros(ind.size, dtype=bool)
        for i in range(ind.size):
            if not idel[i]:
                # keep peaks with the same height if kpsh is True
                idel = idel | (ind >= ind[i] - mpd) & (ind <= ind[i] + mpd) \
                       & (x[ind[i]] > x[ind] if kpsh else True)
                idel[i] = 0  # Keep current peak
        # remove the small peaks and sort back the indices by their occurrence
        ind = np.sort(ind[~idel])

    if show:
        if indnan.size:
            x[indnan] = np.nan
        if valley:
            x = -x
            if mph is not None:
                mph = -mph
        _plot(x, mph, mpd, threshold, edge, valley, ax, ind, title)

    return ind


def _plot(x, mph, mpd, threshold, edge, valley, ax, ind, title):
    """Plot results of the detect_peaks function, see its help."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print('matplotlib is not available.')
    else:
        if ax is None:
            _, ax = plt.subplots(1, 1, figsize=(8, 4))
            no_ax = True
        else:
            no_ax = False

        ax.plot(x, 'b', lw=1)
        if ind.size:
            label = 'valley' if valley else 'peak'
            label = label + 's' if ind.size > 1 else label
            ax.plot(ind, x[ind], '+', mfc=None, mec='r', mew=2, ms=8,
                    label='%d %s' % (ind.size, label))
            ax.legend(loc='best', framealpha=.5, numpoints=1)
        ax.set_xlim(-.02 * x.size, x.size * 1.02 - 1)
        ymin, ymax = x[np.isfinite(x)].min(), x[np.isfinite(x)].max()
        yrange = ymax - ymin if ymax > ymin else 1
        ax.set_ylim(ymin - 0.1 * yrange, ymax + 0.1 * yrange)
        ax.set_xlabel('Data #', fontsize=14)
        ax.set_ylabel('Amplitude', fontsize=14)
        if title:
            if not isinstance(title, str):
                mode = 'Valley detection' if valley else 'Peak detection'
                title = "%s (mph=%s, mpd=%d, threshold=%s, edge='%s')" % \
                        (mode, str(mph), mpd, str(threshold), edge)
            ax.set_title(title)
        # plt.grid()
        if no_ax:
            plt.show()


import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import sys
for t in range(3,4):
    file = "D:\QC\YA\collect_phy" + str(t) + ".txt"
    with open(file, 'r') as file_read:
        for row in file_read:
            row = row.rstrip('\n')
            arr = row.split('_')
            path0 = "D:\\QC\\YA\\" + str(t) + "\\"+row +".txt"  # 读取路径
            path = "D:\\QC\\YA\\image\\" + str(t) +"\\" + row        # 保存路径
            data = np.loadtxt(path0)
            a_data_R = data[:,1]
            a_data_P = data[:,2]
            folder = os.path.exists(path)
            if not folder:
                os.makedirs(path)




            a_data_P_fir = a_data_P[:(a_data_P.shape[0] // 10000 * 10000)].reshape(-1, 10000)
            fig1, axs1 = plt.subplots(ncols=1, nrows=17, figsize=(10, 20))
            # peak = []
            for i in range(17):
                tmp = detect_peaks(a_data_P_fir[i], mph=np.mean(a_data_P), mpd=250, threshold=0, show=True, title=False,
                                   valley=True, ax= axs1[i])
            plt.savefig(os.path.join(path, "P_1"))
            plt.cla()
            plt.close("all")
                # peak.append(tmp)
            fig2, axs2 = plt.subplots(ncols=1, nrows=18, figsize=(10, 20))
            if a_data_P_fir.shape[0]==34:
                for i in range(17,34,1):
                    tmp = detect_peaks(a_data_P_fir[i], mph=np.mean(a_data_P), mpd=250, threshold=0, show=True, title=False,
                                       valley=True, ax= axs2[i-17])
                tmp = detect_peaks(a_data_P_fir[i], mph=np.mean(a_data_P), mpd=250, threshold=0, show=True, title=False,
                                   valley=True, ax=axs2[17])
                plt.savefig(os.path.join(path, "P_2"))
                plt.cla()
                plt.close("all")
                # peak.append(tmp)
            # tmp = detect_peaks(a_data_P_fir, mph=np.mean(a_data_P), mpd=250, threshold=0, show=True, title=False,
            #                    valley=True, name=i, style="_P", path=path)
            # peak.append(tmp)





            a_data_R_fir = a_data_R[:(a_data_R.shape[0] // 10000 * 10000)].reshape(-1, 10000)
            fig3, axs3 = plt.subplots(ncols=1, nrows=17, figsize=(10, 20))
            # peak = []
            for i in range(17):
                tmp = detect_peaks(a_data_R_fir[i], mph=np.mean(a_data_R), mpd=250, threshold=0, show=True, title=False,
                                   valley=True,ax= axs3[i] )
                # peak.append(tmp)
            plt.savefig(os.path.join(path, "R_1"))
            plt.cla()
            plt.close("all")
            fig4, axs4 = plt.subplots(ncols=1, nrows=18, figsize=(10, 20))
            if a_data_R_fir.shape[0] == 34:
                for i in range(17,34,1):
                    tmp = detect_peaks(a_data_R_fir[i], mph=np.mean(a_data_R), mpd=250, threshold=0, show=True, title=False,
                                       valley=True, ax= axs4[i-17])
                tmp = detect_peaks(a_data_R_fir[i], mph=np.mean(a_data_R), mpd=250, threshold=0, show=True, title=False,
                                   valley=True, ax=axs4[17])
                plt.savefig(os.path.join(path, "R_2"))
                plt.cla()
                plt.close("all")
                # peak.append(tmp)
            # tmp = detect_peaks(a_data_R_fir, mph=np.mean(a_data_R), mpd=250, threshold=0, show=True, title=False, valley=True,
            #                    name=i, style="_R", path=path)
            # peak.append(tmp)



