from pydub import AudioSegment
from pydub.silence import detect_nonsilent
from SplitToSentences import cutOnBestSilence

def match_target_amplitude(sound, target_dBFS):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)

def goAmadeus(file,targetFolder, silenceModifier):
    audio_segment = AudioSegment.from_wav(file)
    normalized_sound = match_target_amplitude(audio_segment, -20.0)
    nonsilent_data = detect_nonsilent(normalized_sound, min_silence_len=50, silence_thresh=-45, seek_step=1)

    # print("start,Stop")
    # for chunks in nonsilent_data:
    #     print([chunk / 1000 for chunk in chunks])

    activeHolder = 0
    where = 1
    howManyLoops = 0
    for i in range(len(nonsilent_data)):
        if(where-1 < 0):
            activeHolder += 0
            where += 0
        if where >= 1:
            current_silence = nonsilent_data[howManyLoops][0] - nonsilent_data[howManyLoops-1][1]
            if(current_silence >= 2000):
                activeHolder += 0
            elif current_silence <= 50 and howManyLoops < 3:
                activeHolder += 5
            elif current_silence > 50:
                activeHolder += current_silence
                where += 1
        if(where == 0):
            where += 1
        howManyLoops += 1

    allSilence = activeHolder
    print("All silence: " + str(allSilence) + " ms")

    bestSingleSilence = allSilence / where

    add = bestSingleSilence * silenceModifier/100
    bestSingleSilence = bestSingleSilence+add

    print("Best Silence: " + str(round(bestSingleSilence)) + " ms")

    print("Started Chunking..")

    cutOnBestSilence(round(bestSingleSilence), file, targetFolder)

    best_nonsilent_data = detect_nonsilent(normalized_sound, min_silence_len=round(bestSingleSilence), silence_thresh=-45, seek_step=1)

    return best_nonsilent_data

# goAmadeus("test.wav",1)