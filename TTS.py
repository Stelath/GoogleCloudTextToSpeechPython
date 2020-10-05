from google.cloud import texttospeech as tts
import os

import time
from datetime import datetime
import textwrap

import wave

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "GoogleCloudAuthKey.json"

def text_to_wav(voice_name, text, outputFile, filename):
    language_code = '-'.join(voice_name.split('-')[:2])
    text_input = tts.SynthesisInput(text=text)
    voice_params = tts.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name)
    audio_config = tts.AudioConfig(
        audio_encoding=tts.AudioEncoding.LINEAR16, speaking_rate=1.0)

    client = tts.TextToSpeechClient()
    response = client.synthesize_speech(
        input=text_input,
        voice=voice_params,
        audio_config=audio_config)
    if outputFile:
        filename = f'{filename}.wav'
        with open(filename, 'wb') as out:
            out.write(response.audio_content)
            print(f'Audio content written to "{filename}"')
    else:
        return response.audio_content

inputTextFile = open("input-text.txt", 'r', encoding="utf8")
text = inputTextFile.read()

lines = textwrap.wrap(text, width=2000, break_long_words=False)

speakingRate = float(input("Enter the Speaking Rate: "))

n = 0
for line in lines:
    n = n + 1
    text_to_wav('en-AU-Wavenet-D', line, True, "temp/File_" + str(n))
    print("Got Audio, (" + str(round(((n / len(lines)) * 100))) + "%) done.")

outputFileName = 'Output/Output_' + str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")) + '.wav'
infiles = []
data = []

for i in range(len(lines)):
    infiles.append("temp/File_" + str(i + 1) + ".wav")

for infile in infiles:
    w = wave.open(infile, 'rb')
    data.append([w.getparams(), w.readframes(w.getnframes())])
    w.close()
    
output = wave.open(outputFileName, 'wb')
output.setparams(data[0][0])
for i in range(len(data)):
    output.writeframes(data[i][1])
output.close()
print('Audio content written to', outputFileName + ".")

# audioContentArray = []

# n = 0
# for line in lines:
#     n = n + 1
#     audioContentArray.append(text_to_wav('en-AU-Wavenet-D', line, False, "_"))
#     print("Got Audio, (" + str(round(((n / len(lines)) * 100))) + "%) done.")


# fullAudio = None
# for audio in audioContentArray:
#     if fullAudio == None:
#         fullAudio = audio
#     else:
#         fullAudio = fullAudio + audio

# outputFileName = 'Output/Output_' + str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")) + '.wav'
# output = open(outputFileName, 'wb')
# output.write(fullAudio)
# print('Audio content written to', outputFileName + ".")