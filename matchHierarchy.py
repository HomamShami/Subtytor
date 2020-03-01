import os
from pathlib import Path
import shutil

def get_project_root() -> Path:
    """Returns project root folder."""
    return Path(__file__).parent




whereToLookToMatchHierarchy = r'E:\Medical\USMLE\Resources\Pathoma'




FinishedSubtitles = str(get_project_root())  + r'\matchHierarchyForLater\Subs'
sourceVideosFolder = str(get_project_root()) + r'\matchHierarchyForLater\Vids'

for fffname in os.listdir(sourceVideosFolder):
    input = sourceVideosFolder + r'\%s' % (str(fffname))
    newVideooName = fffname.replace("-s-", " ")
    newVideooNameX = newVideooName.replace("-a-", "&")
    inputNameee = sourceVideosFolder + r'\%s' % (newVideooNameX)
    os.rename(input, inputNameee)

iii = 0
for ffffname in os.listdir(FinishedSubtitles):
    videoss = os.listdir(sourceVideosFolder)
    srtts = os.listdir(FinishedSubtitles)
    originalSrtName = FinishedSubtitles + '\%s'%(srtts[iii])
    originalVideoName = videoss[iii]
    srttss = os.listdir(FinishedSubtitles)
    originalSrtName2 = FinishedSubtitles + '\%s'%(srttss[0])
    newSrtName = FinishedSubtitles+'\%s'%(originalVideoName[:-4]) +'.srt'
    os.rename(originalSrtName2, newSrtName)
    iii+=1

def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root) # return os.path.join(root, name)

def getVideoExtension():
    videoSample = os.listdir(sourceVideosFolder)
    videoSample = videoSample[0]
    videoSample = videoSample[-4:]
    return videoSample

iii = 0
for ffffname in os.listdir(FinishedSubtitles):
    srtts = os.listdir(FinishedSubtitles)
    originalSrtName = FinishedSubtitles + '\%s'%(srtts[iii])
    name = srtts[iii]
    name = name[:-4]
    shutil.copy(originalSrtName, str(find(name+str(getVideoExtension()), whereToLookToMatchHierarchy)))
    iii+=1