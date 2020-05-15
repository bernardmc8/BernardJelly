import os
import subprocess
from movement_locator import allocate_frames
import time
import  sys, os, pdb, shutil, datetime as dt, pandas as pd, numpy as np

from skimage            import io, color, measure, draw, img_as_bool	#scikit-image
from scipy              import optimize, signal
from time               import sleep
from math               import cos, sin, radians, floor
from bisect             import bisect
#from ipysankeywidget    import SankeyWidget

import concurrent.futures
import time


import json

import image_fns as imgFns
import excel_fns as xlFns
from pulse_init_locator import execute_analysis

start_time = time.time()

video_dir = r"I:\Jelly_Videos_Archive_2\Jelly31or32\20200416"

video_files =  [r"F:\20200416\20200416_LT_Jelly30or31_1132pm_1.mp4",
                r"F:\20200416\20200416_LT_Jelly30or31_1132pm_1.mp4",
                r"F:\20200416\20200416_LT_Jelly30or31_1132pm_1.mp4",
                r"F:\20200416\20200416_LT_Jelly30or31_1132pm_1.mp4",
                r"F:\20200416\20200416_LT_Jelly30or31_1132pm_1.mp4",
                r"F:\20200416\20200416_LT_Jelly30or31_1132pm_1.mp4",
                r"F:\20200416\20200416_LT_Jelly30or31_1132pm_1.mp4",
                r"F:\20200416\20200416_LT_Jelly30or31_1132pm_1.mp4",
                r"F:\20200416\20200416_LT_Jelly30or31_1132pm_1.mp4",
                r"F:\20200416\20200416_LT_Jelly30or31_1132pm_1.mp4",
                r"F:\20200416\20200416_LT_Jelly30or31_1132pm_1.mp4",
                r"F:\20200416\20200416_LT_Jelly30or31_1132pm_1.mp4",
                r"F:\20200416\20200416_LT_Jelly30or31_1132pm_1.mp4",
                r"F:\20200416\20200416_LT_Jelly30or31_1132pm_1.mp4",
                r"F:\20200416\20200416_LT_Jelly30or31_1132pm_1.mp4",
                r"F:\20200416\20200416_LT_Jelly30or31_1132pm_1.mp4",
                r"F:\20200416\20200416_LT_Jelly30or31_1132pm_1.mp4",
                r"F:\20200416\20200416_LT_Jelly30or31_1132pm_1.mp4",
                r"F:\20200416\20200416_LT_Jelly30or31_1132pm_1.mp4",
                r"F:\20200416\20200416_LT_Jelly30or31_1132pm_1.mp4",
                                           ]

jpg_files = [r"I:\Jelly_Videos_Archive_2\Jelly31or32\20200416\20200416_LT_Jelly30or31_1132pm_1_00h00m00s_to_05h56m49s\%14d.jpg",
             r"I:\Jelly_Videos_Archive_2\Jelly31or32\20200416\20200416_LT_Jelly30or31_1132pm_1_05h58m19s_to_08h28m49s\%14d.jpg",
             r"I:\Jelly_Videos_Archive_2\Jelly31or32\20200416\20200416_LT_Jelly30or31_1132pm_1_08h33m25s_to_09h29m39s\%14d.jpg",
             r"I:\Jelly_Videos_Archive_2\Jelly31or32\20200416\20200416_LT_Jelly30or31_1132pm_1_09h37m53s_to_10h44m27s\%14d.jpg",
             r"I:\Jelly_Videos_Archive_2\Jelly31or32\20200416\20200416_LT_Jelly30or31_1132pm_1_10h47m57s_to_11h59m19s\%14d.jpg",
             r"I:\Jelly_Videos_Archive_2\Jelly31or32\20200416\20200416_LT_Jelly30or31_1132pm_1_14h56m07s_to_16h52m03s\%14d.jpg",
             r"I:\Jelly_Videos_Archive_2\Jelly31or32\20200416\20200416_LT_Jelly30or31_1132pm_1_16h56m03s_to_20h37m53s\%14d.jpg",
             r"I:\Jelly_Videos_Archive_2\Jelly31or32\20200416\20200416_LT_Jelly30or31_1132pm_1_20h39m23s_to_22h01m42s\%14d.jpg",
             r"I:\Jelly_Videos_Archive_2\Jelly31or32\20200416\20200416_LT_Jelly30or31_1132pm_1_22h06m42s_to_27h20m11s\%14d.jpg",
             r"I:\Jelly_Videos_Archive_2\Jelly31or32\20200416\20200416_LT_Jelly30or31_1132pm_1_34h05m09s_to_35h22m31s\%14d.jpg",
             r"I:\Jelly_Videos_Archive_2\Jelly31or32\20200416\20200416_LT_Jelly30or31_1132pm_1_37h14m01s_to_38h03m37s\%14d.jpg",
             r"I:\Jelly_Videos_Archive_2\Jelly31or32\20200416\20200416_LT_Jelly30or31_1132pm_1_38h05m37s_to_39h44m34s\%14d.jpg",
             r"I:\Jelly_Videos_Archive_2\Jelly31or32\20200416\20200416_LT_Jelly30or31_1132pm_1_39h50m34s_to_41h14m33s\%14d.jpg",
             r"I:\Jelly_Videos_Archive_2\Jelly31or32\20200416\20200416_LT_Jelly30or31_1132pm_1_41h18m33s_to_42h52m50s\%14d.jpg",
             r"I:\Jelly_Videos_Archive_2\Jelly31or32\20200416\20200416_LT_Jelly30or31_1132pm_1_44h13m50s_to_46h39m03s\%14d.jpg",
             r"I:\Jelly_Videos_Archive_2\Jelly31or32\20200416\20200416_LT_Jelly30or31_1132pm_1_48h58m45s_to_53h40m31s\%14d.jpg",
             r"I:\Jelly_Videos_Archive_2\Jelly31or32\20200416\20200416_LT_Jelly30or31_1132pm_1_53h54m03s_to_57h54m15s\%14d.jpg",
             r"I:\Jelly_Videos_Archive_2\Jelly31or32\20200416\20200416_LT_Jelly30or31_1132pm_1_63h25m13s_to_64h47m42s\%14d.jpg",
             r"I:\Jelly_Videos_Archive_2\Jelly31or32\20200416\20200416_LT_Jelly30or31_1132pm_1_64h53m13s_to_67h24m53s\%14d.jpg",
             r"I:\Jelly_Videos_Archive_2\Jelly31or32\20200416\20200416_LT_Jelly30or31_1132pm_1_67h25m53s_to_71h17m10s\%14d.jpg"
               ]

specific_vids = [[r"20200416_LT_Jelly30or31_1132pm_1_00h00m00s_to_05h56m49s"],
                 [r"20200416_LT_Jelly30or31_1132pm_1_05h58m19s_to_08h28m49s"],
                 [r"20200416_LT_Jelly30or31_1132pm_1_08h33m25s_to_09h29m39s"],
                 [r"20200416_LT_Jelly30or31_1132pm_1_09h37m53s_to_10h44m27s"],
                 [r"20200416_LT_Jelly30or31_1132pm_1_10h47m57s_to_11h59m19s"],
                 [r"20200416_LT_Jelly30or31_1132pm_1_14h56m07s_to_16h52m03s"],
                 [r"20200416_LT_Jelly30or31_1132pm_1_16h56m03s_to_20h37m53s"],
                 [r"20200416_LT_Jelly30or31_1132pm_1_20h39m23s_to_22h01m42s"],
                 [r"20200416_LT_Jelly30or31_1132pm_1_22h06m42s_to_27h20m11s"],
                 [r"20200416_LT_Jelly30or31_1132pm_1_34h05m09s_to_35h22m31s"],
                 [r"20200416_LT_Jelly30or31_1132pm_1_37h14m01s_to_38h03m37s"],
                 [r"20200416_LT_Jelly30or31_1132pm_1_38h05m37s_to_39h44m34s"],
                 [r"20200416_LT_Jelly30or31_1132pm_1_39h50m34s_to_41h14m33s"],
                 [r"20200416_LT_Jelly30or31_1132pm_1_41h18m33s_to_42h52m50s"],
                 [r"20200416_LT_Jelly30or31_1132pm_1_44h13m50s_to_46h39m03s"],
                 [r"20200416_LT_Jelly30or31_1132pm_1_48h58m45s_to_53h40m31s"],
                 [r"20200416_LT_Jelly30or31_1132pm_1_53h54m03s_to_57h54m15s"],
                 [r"20200416_LT_Jelly30or31_1132pm_1_63h25m13s_to_64h47m42s"],
                 [r"20200416_LT_Jelly30or31_1132pm_1_64h53m13s_to_67h24m53s"],
                 [r"20200416_LT_Jelly30or31_1132pm_1_67h25m53s_to_71h17m10s"]
                 ]

start_times = ["00:00:00",
               "05:58:19",
               "08:33:25",
               "09:37:53",
               "10:47:57",
               "14:56:07",
               "16:56:03",
               "20:39:23",
               "22:06:42",
               "34:05:09",
               "37:14:01",
               "38:05:37",
               "39:50:34",
               "41:18:33",
               "44:13:50",
               "48:58:45",
               "53:54:03",
               "63:25:13",
               "64:53:13",
               "67:25:53"
                            ]   #format is 00:00:00

durations = ["05:56:49",
             "02:30:30",
             "00:56:14",
             "01:06:34",
             "01:11:22",
             "01:55:56",
             "03:41:50",
             "01:22:19",
             "05:13:29",
             "01:17:22",
             "00:49:36",
             "01:38:57",
             "01:23:59",
             "01:34:17",
             "02:25:13",
             "04:41:46",
             "04:00:12",
             "01:22:29",
             "02:31:40",
             "03:51:17"
                        ]      #hours:minutes:seconds

centers = [ [370, 192],
            [356, 182],
            [377, 133],
            [309, 69],
            [382, 129],
            [217, 182],
            [259, 163],
            [262, 161],
            [360, 310],
            [407, 358],
            [500, 232],
            [415, 132],
            [471, 162],
            [487, 208],
            [423, 295],
            [237, 99],
            [419, 276],
            [320, 388],
            [431, 123],
            [403, 100]

                ]   #x, y format
#Change fps to 120 if mp4 and 60 if avi

#TEST: uncomment if you want to test
# video_dir = r"E:\AliTest"
# video_files = [r"E:\AliTest\videos\Test1.mp4", r"E:\AliTest\videos\Test2.mp4", r"E:\AliTest\videos\Test3.mp4"]
# jpg_files = [r"E:\AliTest\images1\%14d.jpg", r"E:\AliTest\images2\%14d.jpg", r"E:\AliTest\images3\%14d.jpg"]
# specific_vids = [[r"images1"], [r"images2"], [r"images3"]]
# start_times = ["00:00:00", "00:00:00", "00:00:00"]
# durations = ["00:02:11", "00:02:11", "00:02:11"]
# centers = [[297, 187], [297, 187], [297, 187]]

core2filemaps = []                #don't need to fill this in
for i in range(len(start_times)):
    core2filemaps.append(r"\core2fileMap_" + specific_vids[i][0] + ".txt")
errors = []              #don't need to fill this in

assert len(start_times) == len(durations) == len(specific_vids) == len(centers) == len(jpg_files) == len(video_files), "There should be the same number of start times, durations, specific videos, centers"


#run ffmpeg with changing parameters

# for i in range(len(start_times)):
#     try:
#         os.chdir(r"C:\Users\Mike's")
#         os.system("ffmpeg -ss " + start_times[i] + " -i " + video_files[i] + " -r 120 -q 0 -t " + durations[i] + " " + jpg_files[i])
#     except:
#         errors.append("ffmpeg error on video " + str(i))
#         continue


# # ##run movement_locator with changing parameters
# #
# for i in range(len(start_times)):
#     try:
#         if not os.path.exists(jpg_files[i][:-9] + r"\outputs"):
#             os.mkdir(jpg_files[i][:-9] + r"\outputs")
#         jpgList = os.listdir(jpg_files[i][:-9])
#         length = len(jpgList) // 4
#         core1 = []
#         core2 = []
#         core3 = []
#         core4 = []
#         for x in range(0, length):
#             core1.append(jpgList[x])
#         for x in range(length, length * 2):
#             core2.append(jpgList[x])
#         for x in range(length * 2, length * 3):
#             core3.append(jpgList[x])
#         for x in range(length * 3, len(jpgList) - 1):
#             core4.append(jpgList[x])
#         with open(r"C:\Users\Mike's\Dropbox\Fellyjish\jelly-test\core2fileMap_" + specific_vids[i][0] + ".txt", "w") as file:  #WHERE CORE2FILEMAP IS DUMPED
#             file.write(json.dumps({"1": core1, "2": core2, "3": core3, "4": core4}))
#
#     except Exception as e:
#        errors.append("Movement locator error on video " + str(i) + str(e))
#
# #import everything we need for pulse init locator

sleep(5) #DO NOT REMOVE THIS

##run pulse init locator with changing parameters
for i in range(len(start_times)):
    try:
        print("Mapping done")
        if __name__ == '__main__':
            with concurrent.futures.ProcessPoolExecutor() as executor:
                basePath = os.path.dirname(os.path.dirname(__file__)) + "\jelly-test"
                executor.map(execute_analysis, ([1, basePath + core2filemaps[i], video_dir, specific_vids[i], centers[i][0], centers[i][1]],
                                          [2, basePath + core2filemaps[i], video_dir, specific_vids[i], centers[i][0], centers[i][1]],
                                          [3, basePath + core2filemaps[i], video_dir, specific_vids[i], centers[i][0], centers[i][1]],
                                          [4, basePath + core2filemaps[i], video_dir, specific_vids[i], centers[i][0], centers[i][1]]
                ))
    except:
        errors.append("pulse init error on video " + str[i])
        continue

print("--- %s seconds ---" % (time.time() - start_time))
for error in errors:
    print(error)



