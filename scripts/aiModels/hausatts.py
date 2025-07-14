from transformers import VitsModel, AutoTokenizer
import torch
import scipy.io.wavfile
import numpy as np
from pydub import AudioSegment

model = VitsModel.from_pretrained("facebook/mms-tts-hau")
tokenizer = AutoTokenizer.from_pretrained("facebook/mms-tts-hau")

# Save the tokenizer and model locally
tokenizer.save_pretrained("./hausa/tokenizer")
model.save_pretrained("./hausa/model")

text = """  Gabatarwa
Ni, ɗan matashi  mai raɗaɗin zuciya,
Na fara wannan tafiya ta rayuwa a cikin gari mai birni da ƙauye;
Ina jin sauti na agogo  yana ƙararrawa,
Ina jin saƙo daga Allah, mai cewa "ka buɗe ƙofa , ka buɗe zuciyarka."
Daga Janairu zuwa Disamba, daga litinin zuwa Asabar,
Na ji kalaman malamai  sun faɗa:
"Soyayya ita ce tushen ilimi da rayuwa;
Ka koyi harshen zuciyarka, ka ƙware a cikin magana,
Saboda harshenka na ƙunshe da lafiya da arziƙi kamar zinariya 
Da karfi kamar ƙarfe  da fahimta kamar kimiyya ."""

lines = text.splitlines() 
files = []
combined = AudioSegment.empty()

for index, line in enumerate(lines):
    print(f"Index {index}: {line}")

    inputs = tokenizer(line, return_tensors="pt")

# Generate the waveform
    with torch.no_grad():
        output = model(**inputs).waveform

# Ensure the output tensor is on the CPU
    output = output.cpu()

# Convert the PyTorch tensor to a NumPy array
    output_np = output.numpy()

# Squeeze the array to remove single-dimensional entries
    output_np_squeezed = np.squeeze(output_np)

# Write the waveform to a WAV file
#    name = input("Name of the Audio File: ")
    scipy.io.wavfile.write(f"hausa{index}.wav", rate=model.config.sampling_rate, data=output_np_squeezed)
    files.append(f"hausa{index}.wav")

for file in files:
    audio = AudioSegment.from_wav(file)
    combined += audio

combined.export("finalHausa_audio.wav", format="wav")




