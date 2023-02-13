import os, matplotlib, sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def detect_peaks(x, mph=None, mpd=1, threshold=0, edge='rising',
                 kpsh=False, valley=False, show=False, ax=None, title=True, subject_id='#Data'):
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
        _plot(x, mph, mpd, threshold, edge, valley, ax, ind, title, subject_id)

    return ind


def _plot(x, mph, mpd, threshold, edge, valley, ax, ind, title, subject_id):
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
        ax.set_xlabel(subject_id, fontsize=10)
        ax.set_ylabel('Amplitude', fontsize=10)
        if title:
            if not isinstance(title, str):
                mode = 'Valley detection' if valley else 'Peak detection'
                title = "%s (mph=%s, mpd=%d, threshold=%s, edge='%s')" % \
                        (mode, str(mph), mpd, str(threshold), edge)
            ax.set_title(title)
        # plt.grid()
        if no_ax:
            plt.show()

path = "D:/Research/UI_Physio/Oct_2022/"
image_path = "D:/Research/UI_Physio/image/"
for root, dirs, files in os.walk(path):
    for name in files:
        if name == "pulse.csv":
            data = pd.read_csv(os.path.join(root,name), usecols=["Data"])
            data_P = data.Data
            a_data_P = np.array(data_P)  # 将dataframe格式转为arry格式
            a_data_P = a_data_P.flatten()  # 将二维数组转为一维数组
            xlable = root.split("\\")
            xlable = xlable[0][-17:]+"_" + xlable[2]+"_"+xlable[3]+ "_P"
            try:
                if len(a_data_P)>10000:
                    a_data_P_fir = a_data_P[:(a_data_P.shape[0] // 10000 * 10000)].reshape(-1, 10000)
                    fig1, axs1 = plt.subplots(ncols=1, nrows=a_data_P_fir.shape[0], figsize=(15, 20))
                    for i in range(a_data_P_fir.shape[0]):
                        tmp = detect_peaks(a_data_P_fir[i], mph=100000, mpd=200, threshold=0, show=True, title=False,
                                         ax= axs1[i], subject_id= xlable)
                    # plt.show()
                    plt.savefig(os.path.join(image_path, xlable+".png"))
                    plt.cla()
                    plt.close("all")
            except Exception as e:
                print(e)
        if name == "resp.csv":
            data = pd.read_csv(os.path.join(root, name), usecols=["Data"])
            data_R = data.Data
            a_data_R = np.array(data_R)  # 将dataframe格式转为arry格式
            a_data_R = a_data_R.flatten()  # 将二维数组转为一维数组
            xlable = root.split("\\")
            xlable = xlable[0][-17:] +"_"+ xlable[2] + "_" + xlable[3]+"_R"
            try:
                if len(a_data_R)>10000:
                    a_data_R_fir = a_data_R[:(a_data_R.shape[0] // 10000 * 10000)].reshape(-1, 10000)
                    fig1, axs1 = plt.subplots(ncols=1, nrows=a_data_R_fir.shape[0], figsize=(15, 20))
                    for i in range(a_data_R_fir.shape[0]):
                        tmp = detect_peaks(a_data_R_fir[i], mph=100000, mpd=200, threshold=0, show=True, title=False,
                                           ax=axs1[i], subject_id= xlable)
                    # plt.show()
                    plt.savefig(os.path.join(image_path, xlable+".png"))
                    plt.cla()
                    plt.close("all")
            except Exception as e:
                print(e)
        if name == "mmwr.csv":
            data = pd.read_csv(os.path.join(root, name), usecols=["Data"])
            data_M = data.Data
            a_data_M = np.array(data_M)  # 将dataframe格式转为arry格式
            a_data_M = a_data_M.flatten()  # 将二维数组转为一维数组
            xlable = root.split("\\")
            xlable = xlable[0][-17:] +"_"+ xlable[2]+"_"+xlable[3]+"_M"
            try:
                if len(a_data_M)>10000:
                    a_data_M_fir = a_data_M[:(a_data_M.shape[0] // 10000 * 10000)].reshape(-1, 10000)
                    fig1, axs1 = plt.subplots(ncols=1, nrows=a_data_M_fir.shape[0], figsize=(15, 20))
                    for i in range(a_data_M_fir.shape[0]):
                        tmp = detect_peaks(a_data_M_fir[i], mph=100000, mpd=200, threshold=0, show=True, title=False,
                                           ax=axs1[i], subject_id= xlable)
                    # plt.show()
                    plt.savefig(os.path.join(image_path, xlable+".png"))
                    plt.cla()
                    plt.close("all")
            except Exception as e:
                print(e)