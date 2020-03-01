def goSubtytor():
    import time
    import speech_recognition as sr
    from os import path
    import datetime
    import os
    from pathlib import Path
    import subprocess
    import shutil
    from distutils.dir_util import copy_tree
    from requests.exceptions import ProxyError
    from http.client import IncompleteRead
    from detectBestSilenceDuration import goAmadeus
    from convertMilliToTimeString import convertMillisecsToTimeString
    from convertMilliToTimeString import makeBetterEndingTime


    whereToLookToMatchHierarchy = r'E:\Medical\USMLE\Resources\Pathoma'                        #folder you got the videos from
    lang = 'en'                                                                                #more at:  http://stackoverflow.com/a/14302134
    silenceModifier = 0                                                                        #Percent, You Can Enter Minus Values As Well..


    def get_project_root():
        """Returns project root folder."""
        return Path(__file__).parent

    # Test Short Videos In H:/TestVideos

    rootdir = str(get_project_root()) + r'\toAnalyse\SplittedFiles'
    sourceVideosFolder = str(get_project_root()) + r'\VideosToAnalyze'
    temporaryWavFolder = str(get_project_root()) + r'\toAnalyse\wavFiles'
    outputSubtitlesFolder = str(get_project_root()) + r'\outputSubtitles'
    temporarySubtitles = str(get_project_root()) + r'\temporarySubtitles'
    FinishedSubtitles = str(get_project_root()) + r'\FinishedSubtitles'
    archiveFolder = str(get_project_root()) + r'\archiveFolder'


    global block_num
    block_num = 0




    ii = 1
    global aa
    aa = 0

    def removeFilesInAfolder(targetFolderPath):
        for the_file in os.listdir(targetFolderPath):
            file_path = os.path.join(targetFolderPath, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                #elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as ee:
                print(ee)

    if not os.path.exists(rootdir):
        os.makedirs(rootdir)
    shutil.rmtree(rootdir)
    if not os.path.exists(rootdir):
        os.makedirs(rootdir)

    removeFilesInAfolder(temporaryWavFolder)
    removeFilesInAfolder(outputSubtitlesFolder)
    removeFilesInAfolder(FinishedSubtitles)


    for fname in os.listdir(sourceVideosFolder):
        if fname.endswith(".srt"):
            filuname = os.path.join(sourceVideosFolder, fname)
            os.remove(filuname)

    for fname in os.listdir(sourceVideosFolder):
        if fname.endswith(".mp4") or fname.endswith(".m4v") or fname.endswith(".m4a")or fname.endswith(".wav"):
            input = sourceVideosFolder + r'\%s' % (str(fname))

            newName = fname.replace(" ", "-s-")
            newNameX = newName.replace("&", "-a-")

            inputNamee = sourceVideosFolder + r'\%s' % (newNameX)
            ouputNamee = temporaryWavFolder + r'\%s' % (newNameX) + '.wav'

            os.rename(input, inputNamee)


            command = "ffmpeg -i %s -ab 160k -ac 1 -ar 16000 -vn %s -f wav"%(inputNamee, ouputNamee)
            subprocess.call(command, shell=True)


    myList = []
    for fname in os.listdir(temporaryWavFolder):


    # old school chuncking ..
        if fname.endswith(".wav"):

            ffname = fname[:-4]

            newFolder = str(get_project_root()) + r'\toAnalyse\SplittedFiles\%s'%(ffname)
            if not os.path.exists(newFolder):
                os.makedirs(newFolder)
            fname = temporaryWavFolder + '\%s' % (fname)

            newData = goAmadeus(fname, newFolder, silenceModifier)
            myList.append(newData)



    for directory, dirs, files in os.walk(rootdir):
        try:
            block_num = 1
            aa = 0
            print(directory)


            for filename in os.listdir(directory):
                def writeToSrt(giveItToMe):

                    start_time = datetime.datetime(100,1,1,0,0,0)


                    def speech_to_srt(current_time, block):

                        global block_num
                        block_num += 1

                        block_str = str(block)

                        global srtFileName
                        if ii >= 0 and ii <= 9 :
                            srtFileName = '00000' + str(ii) + "-mySrt.srt"
                        if ii >= 10 and ii <= 99 :
                            srtFileName = '0000' + str(ii) + "-mySrt.srt"
                        if ii >= 100 and ii <= 999 :
                            srtFileName = '000' + str(ii) + "-mySrt.srt"
                        if ii >= 1000 and ii <= 9999 :
                            srtFileName = '00' + str(ii) + "-mySrt.srt"
                        if ii >= 10000 and ii <= 99999 :
                            srtFileName = '0' + str(ii) + "-mySrt.srt"

                        current_start_time_new = convertMillisecsToTimeString(myList[ii][block-1][0])
                        try:
                            current_end_time_new = makeBetterEndingTime(myList[ii][block-1][1], myList[ii][block][0])
                        except:
                            current_end_time_new = convertMillisecsToTimeString(myList[ii][block - 1][1])

                        xxx = outputSubtitlesFolder+'\%s'%(srtFileName)
                        with open(xxx, "a", encoding='utf-8') as f:
                            f.write(block_str)
                            f.write("\n")
                            f.write(current_start_time_new)
                            f.write(" --> ")
                            f.write(current_end_time_new)
                            f.write("\n")
                            f.write(giveItToMe)
                            f.write("\n")
                            f.write("\n")

                    speech_to_srt(start_time, block_num)

                print(filename)
                AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), directory + r'\%s'%(filename))

                # use the audio file as the audio source
                r = sr.Recognizer()
                with sr.AudioFile(AUDIO_FILE) as source:
                    audio = r.record(source)  # read the entire audio file

                def tryagain2():
                    try:
                        print("Started")
                        result = r.recognize_google(audio, language=lang)
                        print('\n')
                        writeToSrt(result)
                        global aa
                        aa += 1

                    except sr.UnknownValueError:
                        print("could not understand audio.. ")
                        result = ' '
                        writeToSrt(result)
                        aa += 1
                    except sr.RequestError as e:
                        print("error; {0}".format(e))
                        print("could not understand audio whatsoever")
                        result = ' '
                        writeToSrt(result)
                    except ConnectionError as a:
                        print("error; {0}".format(a))
                        print("CONNECTION ERROR, Trying Again..")
                        time.sleep(3)
                        tryagain2()
                    except RecursionError as b:
                        print("Recursive error; {0}".format(b))
                        print("Couldn't Do It Whatsoever".format(b))
                    except ProxyError as zz:
                        print("Proxy Error error Occured, Please Change Your Ip To Continue Translation..; {0}".format(zz))
                        time.sleep(3)
                        tryagain2()
                    except IncompleteRead as ohGodWhy:
                        print("Incomplete Read Error error Occured, Please Make Sure You're Constantly Connected To The Internet..; {0}".format(ohGodWhy))
                        time.sleep(3)
                        tryagain2()
                    except ValueError as ohGodWhyy:
                        print("Value Error error Occured, Please Make Sure You're Constantly Connected To The Internet..; {0}".format(ohGodWhyy))
                        time.sleep(3)
                        tryagain2()
                    except TimeoutError as stopIt:
                        print("Value Error error Occured, Please Make Sure You're Constantly Connected To The Internet..; {0}".format(stopIt))
                        time.sleep(3)
                        tryagain2()
                    except:
                        print("Unknown Error error Occured, Please Make Sure You're Constantly Connected To The Internet..; ")
                        time.sleep(3)
                        tryagain2()

                def tryagain1():
                    try:
                        print("Started")
                        result = r.recognize_google(audio, language=lang)
                        print('\n')
                        writeToSrt(result)
                        global aa
                        aa += 1

                    except sr.UnknownValueError:
                        # print("could not understand audio")
                        # print(2)
                        # tryagain2()
                        print("could not understand audio.. ")
                        result = ' '
                        writeToSrt(result)
                        aa += 1
                    except sr.RequestError as e:
                        print("could not understand audio ".format(e))
                        print("trying again")
                        time.sleep(3)
                        tryagain2()
                    except ConnectionError as a:
                        print("error; {0}".format(a))
                        print("CONNECTION ERROR, Trying Again..")
                        time.sleep(3)
                        tryagain1()
                    except RecursionError as b:
                        print("Recursive error; {0}".format(b))
                        time.sleep(3)
                        tryagain2()
                    except ProxyError as zz:
                        print("Proxy Error error Occured, Please Change Your Ip To Continue Translation..; {0}".format(zz))
                        time.sleep(3)
                        tryagain1()
                    except IncompleteRead as ohGodWhy:
                        print("Incomplete Read Error error Occured, Please Make Sure You're Constantly Connected To The Internet..; {0}".format(ohGodWhy))
                        time.sleep(3)
                        tryagain1()
                    except ValueError as ohGodWhyy:
                        print("Value Error error Occured, Please Make Sure You're Constantly Connected To The Internet..; {0}".format(ohGodWhyy))
                        time.sleep(3)
                        tryagain1()
                    except TimeoutError as stopIt:
                        print("Value Error error Occured, Please Make Sure You're Constantly Connected To The Internet..; {0}".format(stopIt))
                        time.sleep(3)
                        tryagain1()
                    except :
                        print("Unknown Error error Occured, Please Make Sure You're Constantly Connected To The Internet..")
                        time.sleep(3)
                        tryagain1()

                def tryagain():
                    try:
                        print("Started")
                        result = r.recognize_google(audio, language= lang)
                        # language= 'ar'
                        print('\n')
                        writeToSrt(result)
                        global aa
                        aa += 1

                    except sr.UnknownValueError:
                        # print("could not understand audio")
                        # print(1)
                        # tryagain1()
                        print("could not understand audio.. ")
                        result = ' '
                        writeToSrt(result)
                        aa += 1
                    except sr.RequestError as e:
                        print("could not understand audio {0}".format(e))
                        print("trying again")
                        time.sleep(3)
                        tryagain1()
                    except ConnectionError as a:
                        print("error; {0}".format(a))
                        print("CONNECTION ERROR, Trying Again..")
                        time.sleep(3)
                        tryagain()
                    except RecursionError as b:
                        print("Recursive error; {0}".format(b))
                        time.sleep(3)
                        tryagain1()
                    except ProxyError as zz:
                        print("Proxy Error error Occured, Please Change Your Ip To Continue Translation..; {0}".format(zz))
                        time.sleep(3)
                        tryagain()
                    except IncompleteRead as ohGodWhy:
                        print("Incomplete Read Error error Occured, Please Make Sure You're Constantly Connected To The Internet..; {0}".format(ohGodWhy))
                        time.sleep(3)
                        tryagain()
                    except ValueError as ohGodWhyy:
                        print("Value Error error Occured, Please Make Sure You're Constantly Connected To The Internet..; {0}".format(ohGodWhyy))
                        time.sleep(3)
                        tryagain()
                    except TimeoutError as stopIt:
                        print("Value Error error Occured, Please Make Sure You're Constantly Connected To The Internet..; {0}".format(stopIt))
                        time.sleep(3)
                        tryagain()
                    except :
                        print("Unknown Error error Occured, Please Make Sure You're Constantly Connected To The Internet..")
                        time.sleep(3)
                        tryagain()

                tryagain()
            ii += 1

        except PermissionError as rip:
            print('This Folder Has No mp4 {0}' .format(rip))
            print("\n")
            ii -= 1




    for fffname in os.listdir(sourceVideosFolder):
        input = sourceVideosFolder + r'\%s' % (str(fffname))
        newVideooName = fffname.replace("-s-", " ")
        newVideooNameX = newVideooName.replace("-a-", "&")
        inputNameee = sourceVideosFolder + r'\%s' % (newVideooNameX)
        os.rename(input, inputNameee)



    iii = 0
    for ffffname in os.listdir(outputSubtitlesFolder):
        videoss = os.listdir(sourceVideosFolder)
        srtts = os.listdir(outputSubtitlesFolder)
        originalSrtName = outputSubtitlesFolder + '\%s'%(srtts[iii])
        originalVideoName = videoss[iii]
        shutil.copy(originalSrtName, temporarySubtitles)
        srttss = os.listdir(temporarySubtitles)
        originalSrtName2 = temporarySubtitles + '\%s'%(srttss[0])
        newSrtName = temporarySubtitles+'\%s'%(originalVideoName[:-4]) +'.srt'
        os.rename(originalSrtName2, newSrtName)
        shutil.copy(newSrtName, FinishedSubtitles)
        os.remove(newSrtName)
        iii+=1

    copy_tree(FinishedSubtitles, sourceVideosFolder)

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

    copy_tree(archiveFolder, FinishedSubtitles)
