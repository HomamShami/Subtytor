from pydub import AudioSegment
from pydub.silence import split_on_silence

def match_target_amplitude(aChunk, target_dBFS):
    ''' Normalize given audio chunk '''
    change_in_dBFS = target_dBFS - aChunk.dBFS
    return aChunk.apply_gain(change_in_dBFS)

def cutOnBestSilence(bestSilence, file, targetFolder):
    song = AudioSegment.from_wav(file)
    normalized_sound = match_target_amplitude(song, -20.0)

    chunks = split_on_silence (normalized_sound, min_silence_len=bestSilence, silence_thresh=-45)

    # print(str(len(chunks)) + " Chunks")
    # print("Exporting Chuncks....")
    # print("\n")

    for i, chunk in enumerate(chunks):
        normalized_chunk = chunk

        if i >= 0 and i <= 9:
            normalized_chunk.export(targetFolder +'/chunk00000' + str(i) + '.wav', format="wav")
        if i >= 10 and i <= 99 :
            normalized_chunk.export(targetFolder + '/chunk0000' + str(i) + '.wav', format="wav")
        if i >= 100 and i <= 999 :
            normalized_chunk.export(targetFolder + '/chunk000' + str(i) + '.wav', format="wav")
        if i >= 1000 and i <= 9999 :
            normalized_chunk.export(targetFolder + '/chunk00' + str(i) + '.wav', format="wav")
        if i >= 10000 and i <= 99999 :
            normalized_chunk.export(targetFolder + '/chunk0' + str(i) + '.wav', format="wav")



# cutOnBestSilence(222, "test.wav", r"C:\Pro\Py\MySpeechRecognizer\toAnalyse\SplittedFiles\out")