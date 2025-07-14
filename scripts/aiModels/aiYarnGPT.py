

!git clone https://github.com/saheedniyi02/yarngpt.git

pip install outetts uroman

import os
import re
import json
import torch
import inflect
import random
import uroman as ur
import numpy as np
import torchaudio
import IPython
from transformers import AutoModelForCausalLM, AutoTokenizer
from outetts.wav_tokenizer.decoder import WavTokenizer


!wget https://huggingface.co/novateur/WavTokenizer-medium-speech-75token/resolve/main/wavtokenizer_mediumdata_frame75_3s_nq1_code4096_dim512_kmeans200_attn.yaml
!gdown 1-ASeEkrn4HY49yZWHTASgfGFNXdVnLTt


from yarngpt.audiotokenizer import AudioTokenizerV2

tokenizer_path="saheedniyi/YarnGPT2"
wav_tokenizer_config_path="/content/wavtokenizer_mediumdata_frame75_3s_nq1_code4096_dim512_kmeans200_attn.yaml"
wav_tokenizer_model_path = "/content/wavtokenizer_large_speech_320_24k.ckpt"


audio_tokenizer=AudioTokenizerV2(
    tokenizer_path,wav_tokenizer_model_path,wav_tokenizer_config_path
    )


model = AutoModelForCausalLM.from_pretrained(tokenizer_path,torch_dtype="auto").to(audio_tokenizer.device)

#change the text
text="The election was won by businessman and politician, Moshood Abiola, but Babangida annulled the results, citing concerns over national security."

# change the language and voice
prompt=audio_tokenizer.create_prompt(text,lang="english",speaker_name="idera")

input_ids=audio_tokenizer.tokenize_prompt(prompt)

output  = model.generate(
            input_ids=input_ids,
            temperature=0.1,
            repetition_penalty=1.1,
            max_length=4000,
            #num_beams=5,# using a beam size helps for the local languages but not english
        )

codes=audio_tokenizer.get_codes(output)
audio=audio_tokenizer.get_audio(codes)
IPython.display.Audio(audio,rate=24000)
torchaudio.save(f"Sample.wav", audio, sample_rate=24000)
