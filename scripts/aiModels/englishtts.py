
from transformers import VitsModel, AutoTokenizer
import torch
import scipy.io.wavfile
import numpy as np

model = VitsModel.from_pretrained("facebook/mms-tts-eng")
tokenizer = AutoTokenizer.from_pretrained("facebook/mms-tts-eng")

# Save the tokenizer and model locally
tokenizer.save_pretrained("./english/tokenizer")
model.save_pretrained("./english/model")

text = "some example text in the Hausa language"
inputs = tokenizer(text, return_tensors="pt")


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
name = input("Name of the Audio File: ")
scipy.io.wavfile.write(f"{name}.wav", rate=model.config.sampling_rate, data=output_np_squeezed)

