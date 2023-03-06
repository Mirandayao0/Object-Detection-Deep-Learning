import imageio.v2 as imageio
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def generate_animation(path, num):
    images = []
    for e in range(num):
        img_name = str(e)+'.png'
        images.append(imageio.imread(img_name))
    imageio.mimsave(path + '_generate_animation.gif', images, fps=2)
#  fps  frame per second

def get_seconds(time_str):
    # print('Time in hh:mm:ss:', time_str)
    # split in hh, mm, ss
    hh, mm, ss = time_str.split(':')
    return int(hh) * 3600 + int(mm) * 60 + float(ss)

# ___________________________________________________________________next will be main
sample_rate = ''
data = pd.read_csv('../heatmap/Test_Group1/eye1.txt', sep=',', header=None, names=['time','x','y','w'])
# print(max(data.x))
# print(min(data.x))
# print(max(data.y))
# print(min(data.y))
# plt.hist(data.x, bins=20, range=[-2, 2])
# plt.show()
# check distribution
hh_mm_ss1 = data.time[0].split(' ')[1]
hh_mm_ss2 = data.time[len(data.time)-1].split(' ')[1]
start_time = get_seconds(hh_mm_ss1)
end_time = get_seconds(hh_mm_ss2)
total_eyeMoveTimes = len(data.x)
sample_rate = total_eyeMoveTimes/(end_time-start_time)
data_panel = pd.read_csv('../heatmap/Test_Group1/toggle_output.csv')
data_panel.columns = data_panel.columns.str.replace(' ', '_')

# loop over eye1.txt to check time stamp
timeList = np.array(data.time.tolist()).squeeze()
for j in range(len(timeList)):
    hh_mm_ss_timeList = timeList[j].split(' ')[1]
    timeList_eye = get_seconds(hh_mm_ss_timeList)
    timeList[j] = timeList_eye
timeList = timeList.astype(float)
count = 0
# loop over panel switch time, check the duration of trust changes
for i in range(len(data_panel)-1):
    hh_mm_ss_boolTime = data_panel.iat[i, 1].split(' ')[1]
    times_start = get_seconds(hh_mm_ss_boolTime)
    hh_mm_ss_boolTime1 = data_panel.iat[i+1, 1].split(' ')[1]
    times_end = get_seconds(hh_mm_ss_boolTime1)
    if data_panel.iat[i, 3] != data_panel.iat[i+1,3]:
        # print('This is True  False transition')
        filter_time = times_end - times_start
        print(filter_time)
# find overlap time
    idx = np.where((timeList>times_start)&(timeList<times_end))[0]
    if len(idx)>0:
        temp, _, _ = np.histogram2d(data.x[idx], data.y[idx].astype(float), bins=50, range=[[-2, 2], [-2, 2]], weights=data.w[idx])
        plt.figure(figsize=(10,10))
        plt.title("No. "+str(i)+"Eye tracking heatmap Group 1 " +" "+str(round(filter_time,2)))
        plt.xlabel("X coordinate")
        plt.ylabel("Y coordinate")
        plt.imshow(temp, cmap='jet')
        plt.colorbar(label="confidence of VR detector", orientation="vertical", shrink=0.8)
        plt.savefig(str(i))
        count += 1

generate_animation('', count)



# print eye tracking heatmap

# with imageio.get_writer('mygif.gif', mode='I') as writer:
#     for i in range(20):
#         image = imageio.imread(str(i)+'.png')
#         writer.append_data(image,duration = 1)
