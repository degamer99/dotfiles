import pandas as pd 
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


# Path to the local directory where the model is saved
# model_path = './my_model/ar-en/'  # Path where you saved the model

# Load the model and tokenizer from the local directory

# tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-ar-en", cache_dir=model_path)
# model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-ar-en", cache_dir=model_path)

# tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-ar-en")
# tokenizer.save_pretrained("./tokenizer")
# model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-ar-en")
# model.save_pretrained("./model")

# Load the model and tokenizer from the local directory
# model_path="./model_opus-mt-ar-en"
# tokenizer_path="./tokenizer_opus-mt-ar-en"
model_path="./model"
tokenizer_path="./tokenizer"
model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)

# Function to translate a single sentence
def translate_sentence(sentence):
    # Tokenize the sentence
    tokens = tokenizer.encode(sentence, return_tensors='pt')

    # Generate the translation
    translation = model.generate(tokens, max_length=512)

    # Decode the translated sentence
    translated_text = tokenizer.decode(translation[0], skip_special_tokens=True)
    return translated_text


def translate_word_by_word(sentence):
    words = sentence.split()  # Split the Arabic sentence into words
    print(words)
    translations = []

    for word in words:
        # Encode the word in the context of the entire sentence
        input_ids = tokenizer.encode(word, return_tensors="pt", add_special_tokens=True)
        
        # Generate translation
        output_ids = model.generate(input_ids, max_length=10, num_beams=5, early_stopping=True)
        
        # Decode the output to get the translated text
        translated_word = tokenizer.decode(output_ids[0], skip_special_tokens=True)
        translations.append(translated_word)

    return " ".join(translations)

# Example usage
# arabic_sentence = "هل هذا يعني أنكم ستدعمون موقف سوريا؟"
# translated_word_by_word = translate_word_by_word(arabic_sentence)
# print("Translated Word By Word:", translated_word_by_word)
# print("Translated Sentence", translate_sentence(arabic_sentence))


# Function to align Arabic words with their English translations
def align_words(arabic_sentence, english_sentence):
    arabic_words = arabic_sentence.split()
    english_words = english_sentence.split()

    aligned_translation = {}
    for i, arabic_word in enumerate(arabic_words):
        aligned_translation[arabic_word] = english_words[i] if i < len(english_words) else "N/A"

    return aligned_translation

# Example usage
arabic_sentence = "يأتي إلينا السواح من مختلف دول العالم، إلا أن أعلى نسبة منهم تأتي من أوروبا"
translated_sentence = translate_sentence(arabic_sentence)
print("Full Sentence Translation:", translated_sentence)
translated_word_by_word = translate_word_by_word(arabic_sentence)
print("Translated Word By Word:", translated_word_by_word)


# Align the words
alignment = align_words(arabic_sentence, translated_sentence)
print("\nWord-by-Word Alignment:")
for arabic_word, english_word in alignment.items():
    print(f"{arabic_word} -> {english_word}")

# Load your CSV file with Arabic sentences (update file path)
# df = pd.read_csv('arabic column.csv')  # Make sure to replace 'arabic_sentences.csv' with your file path

# # Prepare a list to store the translations
# translations = []

# # Translate each Arabic sentence in the DataFrame
# for sentence in df['Arabic Sentence']:  # Adjust this to your actual column name
#     translated_sentence = translate_sentence(sentence)
#     translations.append(translated_sentence)

# # Add the translations to the DataFrame
# df['English Translation'] = translations

# # Save the results to a new CSV file
# df.to_csv('translated_output.csv', index=False)

# print("Translation complete. Output saved to 'translated_output.csv'.")
