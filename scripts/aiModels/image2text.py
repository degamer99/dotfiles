import easyocr

reader = easyocr.Reader(['en', 'es'], gpu=False)  # English, Yoruba, Hausa, Spanish
result = reader.readtext('./hausa sentence.png')
for (bbox, text, prob) in result:
    print(f"Detected text: {text}, Confidence: {prob}")
