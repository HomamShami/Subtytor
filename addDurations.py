import soundfile as sf
import os

def getFileDuration(wavPath):
    f = sf.SoundFile(wavPath)

    lenInSecs = len(f) / f.samplerate
    return lenInSecs
# lengthHolder = 0
# howManyChuncks = 0
# sourceAudiosFolder = r'.\out'
# for fname in os.listdir(sourceAudiosFolder):
#     if fname.endswith(".wav"):
#         print(fname)
#         fileName = os.path.join(sourceAudiosFolder, fname)
#         ff = sf.SoundFile(fileName)
#         print(ff)
#         lenInSecss = len(ff) / ff.samplerate
#         lengthHolder += lenInSecss
#         howManyChuncks += 1
# silence = lenInSecs - lengthHolder
# print("All Chuncks Length: " + str(lengthHolder))
# print("Chuncks: " + str(howManyChuncks))
# singlesilence = silence/howManyChuncks
# print("Single Silence: " + str(singlesilence*1000))
