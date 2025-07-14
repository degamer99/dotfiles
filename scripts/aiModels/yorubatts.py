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

# Save the tokenizer and model locally
tokenizer.save_pretrained("./yoruba/tokenizer")
model.save_pretrained("./yoruba/model")



# Open the file in read mode and extract its content as a string
with open('20%yoruba.txt', 'r') as file:
    yoruba20 = file.read()
    print(yoruba20)
    inputs = tokenizer(yoruba20, return_tensors="pt")

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
    scipy.io.wavfile.write(f"yoruba20.wav", rate=model.config.sampling_rate, data=output_np_squeezed)





# # Define the text input
# #text = "Emi, ọmọkùnrin ọkan tí ó ní ọkàn gíga àti ẹ̀mí tuntun, Ní ọ̀nà tí ń dùn, pípẹ̀ àtàwọn ìtàn ìbẹ̀rẹ̀,"
# for position, text in enumerate(poem):
#     print(text)
#     lines = text.splitlines() 
#     print(lines)
#     files = []
#     combined = AudioSegment.empty()
#
#     for index, line in enumerate(lines):
#         print(f"Index {index}: {line}")
#
#         inputs = tokenizer(line, return_tensors="pt")
#
# # Generate the waveform
#         with torch.no_grad():
#             output = model(**inputs).waveform
#
# # Ensure the output tensor is on the CPU
#         output = output.cpu()
#
# # Convert the PyTorch tensor to a NumPy array
#         output_np = output.numpy()
#
# # Squeeze the array to remove single-dimensional entries
#         output_np_squeezed = np.squeeze(output_np)
#
# # Write the waveform to a WAV file
# #    name = input("Name of the Audio File: ")
#         scipy.io.wavfile.write(f"yoruba{index}.wav", rate=model.config.sampling_rate, data=output_np_squeezed)
#         files.append(f"yoruba{index}.wav")
#
#     for file in files:
#         audio = AudioSegment.from_wav(file)
#         combined += audio
#
#     combined.export(f"YorubaPoem_Stanza{position}.wav", format="wav")
#
#
