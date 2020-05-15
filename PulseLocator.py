import os
import pathlib
import shutil

from skimage import io, filters, measure
from scipy import ndimage
import json

"""
README:
This program has two main features: 1. To filter out the frames of in which the Jellyfish is not pulsing.
2. To split up the video by the moments in which the Jellyfish is moving. Users only need to change the 5
values below to customize the logic of the program and the output will be a txt file with a mapping of all the relevant
pulses to 4-core processing. There'll be a new txt file every time program detects the Jellyfish centroid moving named
format "core2mapfile[consecutive numbering of core2mapfiles]-x[x-coordinate of centroid]-y[y-coordinate of centroid]".
For example, if the given image stack has one instance in which the Jellyfish moves with center at (0, 0) before moving
and (100, 100) after moving, then there would be two new txt files created in the MapDestination directory:
core2mapfile0-x0-y0 and core2mapfile1-x100-y100. However, the centers will usually be long float decimals. There will
also be a folder created in the mapdestination directory with the same name as the file, which has the first 500 images.
Author: Bernard Chan
"""

directory = r"C:\Users\berna_000\Desktop\Ali\20200211_218pm_1_00h00m00s_to_00h29m34s"  # directory of jpg image stack
mapdestination = r"C:\Users\berna_000\Desktop\Ali"  # directory where the coremapfiles should be created

firstframes = 1000  # Max first x number of frames averaged out to determine uncontracted size of the jellyfish
buffer = 10  # number of frames to be included x away from start and end of detected pulse
centersDistance = 10  # The distance in pixels between two centroids that constitutes movement of the jelly
recalculateCentroid = 50  # Recalculate if the Jellyfish centroid has moved every x frames
numberToFolder = 500  # Maximum number of images copied to a new folder for every stationary period of the jelly

# Note: If there are duplicate frames in the result, that means the buffer was too big
# and another pulse started within the end of another pulse's buffer.
# There should be buffer * 2 amount of frames between each pulse (which shouldn't be difficult).

# ---------------------Only need to understand above--------------------------------------------------------------------

def distanceFormula(x1, y1, x2, y2):
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5


def findArea(file):
    return findJelly(file).area

# For use with any result of findJelly(file)
# https://scikit-image.org/docs/dev/api/skimage.measure.html#regionprops

def findCentroid(file):
    return list(findJelly(file).centroid)


def findJelly(file):
    if file.is_file():
        jellyimage = io.imread(file)  # open image
        jellyimage = jellyimage[:, :, 1]  # turn rgb picture into grey image
        threshold = filters.threshold_otsu(jellyimage)  # find threshold value
        jellymasked = jellyimage > threshold  # apply threshold to Jelly image
        # io.imshow(jellymasked)            #show applied threshold on Jelly image, uncomment to see jelly
        labeledmask, numlabels = ndimage.label(jellymasked,
                                               structure=[[1, 1, 1], [1, 1, 1], [1, 1, 1]])  # separate regions
        dimensions = list(labeledmask.shape)
        height = dimensions[0]
        width = dimensions[1]
        clusters = measure.regionprops(labeledmask, jellyimage)  # create regions
        jelly = None  # the region that represents the jelly so far
        jellyarea = 0  # largest jelly area so far
        for i in range(0, numlabels):  # finds the jelly by finding which region is max area
            jellydimensions = list(clusters[i].bbox)
            minrow = jellydimensions[0]
            mincol = jellydimensions[1]
            maxrow = jellydimensions[2]
            maxcol = jellydimensions[3]
            if minrow != 0 and mincol != 0 and maxrow != height and maxcol != width:  # checks if area is touching the edges
                if clusters[i].area > jellyarea:
                    jelly = clusters[i]
                    jellyarea = jelly.area
        if jelly == None:
            print("No valid jelly found, continuing with largest mass as jelly")
            jelly = clusters[0]
        return jelly


r"""
For testing:
directory = r"C:\Users\berna_000\Desktop\Ali\20200210_Ali_437pm_2_1_00h00m00s_to_00h18m13s"
iter = pathlib.Path(directory).iterdir()
print(findCentroid(next(iter)))
"""

def pulselocator(directory, firstframes, buffer, mapdestination, centersDistance, recalculateCentroid, numToFolder):
    def centersEqual(center1, center2):
        distance = distanceFormula(center1[0], center1[1], center2[0], center2[1])
        return distance < centersDistance

    def coreMapMaker(frames, destination):
        quarterlength = len(frames) // 4
        core1 = []
        core2 = []
        core3 = []
        core4 = []
        for x in range(0, quarterlength):
            core1.append(frames[x])
        for x in range(quarterlength, quarterlength * 2):
            core2.append(frames[x])
        for x in range(quarterlength * 2, quarterlength * 3):
            core3.append(frames[x])
        for x in range(quarterlength * 3, len(frames)):
            core4.append(frames[x])
        with open(destination, "w") as file:
            file.write(json.dumps({"1": core1, "2": core2, "3": core3, "4": core4}))
        folder = destination[0:-4]
        os.mkdir(folder)
        foldercounter = 0
        for string in frames:
            if foldercounter == numToFolder:
                break
            framePath = directory + "/" + string
            shutil.copy(framePath, folder)
            foldercounter += 1

    destination = mapdestination + r"/core2mapfile"
    counter = 0
    totalarea = 0
    for file in pathlib.Path(directory).iterdir():
        if file.is_file():
            if counter == firstframes:
                break
            totalarea += findArea(file)
            counter += 1
    jellysize = totalarea / counter

    savedframes = []
    before = []
    isfirst = True  # True if the last frame was not a pulse. Starts out as True
    counter = 0
    lastcenter = findCentroid(next(pathlib.Path(directory).iterdir()))
    coremapcounter = 0
    centercheck = 0
    centerx = 0
    centery = 0

    for file in pathlib.Path(directory).iterdir():
        centercheck += 1
        center = findCentroid(file)
        if centercheck == recalculateCentroid:
            if not (centersEqual(lastcenter, center)):
                if (len(savedframes) != 0):
                    coreMapMaker(savedframes, destination + str(coremapcounter) + "-x" + str(center[1]) + "-y" + str(
                        center[0]) + ".txt")
                    coremapcounter += 1
                    savedframes.clear()
            centercheck = 0
            lastcenter = center
        if len(before) == buffer:
            before.pop(0)
        before.append(file)
        if not findArea(file) > (jellysize * 0.9):
            if isfirst:
                for frame in before:
                    bpath = str(frame).split("\\")
                    savedframes.append(bpath[len(bpath) - 1])
                before.clear()
            isfirst = False
            path = str(file).split("\\")
            savedframes.append(path[len(path) - 1])
        else:
            if isfirst == False:  # if last frame was a pulse and this frame is not a pulse
                counter = buffer
            if counter:
                apath = str(file).split("\\")
                savedframes.append(apath[len(apath) - 1])
                counter -= 1
            isfirst = True
        centerx = center[1]
        centery = center[0]

    if len(savedframes) != 0:
        coreMapMaker(savedframes,
                     destination + str(coremapcounter) + "-x" + str(centerx) + "-y" + str(centery) + ".txt")


pulselocator(directory, firstframes, buffer, mapdestination, centersDistance, recalculateCentroid, numberToFolder)
