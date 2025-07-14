import os
os.environ["NNPACK_DISABLE"] = "1"

from transformers import VitsModel, AutoTokenizer
import torch
torch.backends.nnpack.enabled = False
import scipy.io.wavfile
import numpy as np
from pydub import AudioSegment

# Load the model and tokenizer
model = VitsModel.from_pretrained("facebook/mms-tts-yor")
tokenizer = AutoTokenizer.from_pretrained("facebook/mms-tts-yor")

# Optionally, save them locally
# tokenizer.save_pretrained("./yoruba/tokenizer")
# model.save_pretrained("./yoruba/model")

# Read the text file and split into lines
with open('20%Yoruba.txt', 'r', encoding='utf-8') as file:
    lines = file.read().splitlines()

# Remove empty lines (and strip any extra spaces)
lines = [line.strip() for line in lines if line.strip() != '']

# Initialize an empty AudioSegment for combining outputs
combined_audio = AudioSegment.empty()

# Process each non-empty line individually
for idx, line in enumerate(lines):
    print(f"Processing line {idx}: {line}")
    # Tokenize the line
    inputs = tokenizer(line, return_tensors="pt")
    
    # Generate the waveform with no gradient tracking
    with torch.no_grad():
        output = model(**inputs).waveform

    # Ensure the output is on CPU, convert to NumPy, and squeeze extra dimensions
    output = output.cpu()
    output_np = output.numpy()
    output_np_squeezed = np.squeeze(output_np)
    
    # Write the waveform to a WAV file
    wav_filename = f"yoruba_Story_Line{idx}.wav"
    scipy.io.wavfile.write(wav_filename, rate=model.config.sampling_rate, data=output_np_squeezed)
    
    # Load the generated WAV file with pydub and append to combined audio
    audio_segment = AudioSegment.from_wav(wav_filename)
    combined_audio += audio_segment

# Export the final combined audio file
combined_audio.export("Yoruba_Story_Combined.wav", format="wav")

print("All audio files have been combined into 'Yoruba_Story_Combined.wav'")

