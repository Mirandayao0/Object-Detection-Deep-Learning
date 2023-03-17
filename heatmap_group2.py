import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def get_seconds(time_str):
    # print('Time in hh:mm:ss:', time_str)
    # split in hh, mm, ss
    hh, mm, ss = time_str.split(':')
    return int(hh) * 3600 + int(mm) * 60 + float(ss)


data = pd.read_csv('../heatmap/Test_Group2/eye2.txt', sep=',', header=None, names=['time', 'x', 'y', 'w'])
data = data[data.w >= 0.8]
data_panel = pd.read_csv('../heatmap/Test_Group2/toggle_output.csv')
data_panel.columns = data_panel.columns.str.replace(' ', '_')
data_detection = pd.read_csv('../heatmap/Test_Group2/detection_output.csv')
data_detection.columns =  data_detection.columns.str.replace(' ', '_')
my_title = ["no target", "target on top left", "target on top right", "target on bottom left", "target on bottom right"]

count = 0
# loop over eye1.txt to check time stamp
timeList = np.array(data.time.tolist()).squeeze()
for j in range(len(timeList)):
    hh_mm_ss_timeList = timeList[j].split(' ')[1]
    timeList_eye = get_seconds(hh_mm_ss_timeList)
    timeList[j] = timeList_eye
timeList = timeList.astype(float)


timeList_detect = np.array(data_detection.Time_Stamp.tolist()).squeeze()
for j in range(len(timeList_detect)):
    hh_mm_ss_timeList = timeList_detect[j].split(' ')[1]
    s = get_seconds(hh_mm_ss_timeList)
    timeList_detect[j] = s
timeList_detect = timeList_detect.astype(float)


# loop over panel switch time, check the duration of trust changes
plt.figure(figsize=(40, 10))
for i in range(len(data_panel)-1):
    hh_mm_ss_boolTime = data_panel.iat[i, 1].split(' ')[1]
    times_start = get_seconds(hh_mm_ss_boolTime)
    hh_mm_ss_boolTime1 = data_panel.iat[i+1, 1].split(' ')[1]
    times_end = get_seconds(hh_mm_ss_boolTime1)
    if (data_panel.iat[i, 3] == False) and (data_panel.iat[i+1, 3] == True):
        # print('This is True  False transition')
        filter_time = times_end - times_start
        # count+=1
        # print(filter_time)
        # print(count)
    # find overlap time
    idx = (np.where((timeList > times_start) & (timeList < times_end))[0]).tolist()

    if len(idx) > 0:

        temp, _, _ = np.histogram2d(np.array(data.x.tolist())[idx],
                                    np.array(data.y.tolist())[idx],
                                    bins=20, range=[[-2, 2], [-2, 2]],
                                    weights=np.array(data.w.tolist())[idx])
        # find detect_output's threat position
        idx2 = -1
        idx2 = np.where((timeList_detect > times_start) & (timeList_detect < times_end))[0]
        t = data_detection.Threat_Position[idx2].tolist()

        if len(t) > 0:
            Threat_Position = t[0] + 2
            # print(Threat_Position)
            # if Threat_Position > 0:
            plt.subplot(1, 5, Threat_Position)
            plt.imshow(temp, cmap='jet', alpha=0.2)
            plt.title(str(Threat_Position-2) + "  " + my_title[Threat_Position-1]+" Eye tracking heatmap Group 2 ")

        count += 1


# plt.xlabel("X coordinate")
# plt.ylabel("Y coordinate")
# plt.colorbar(label="confidence of VR detector", orientation="vertical", shrink=0.8)
plt.savefig('group2')
