#pip install pandas

import pandas as pd

# Load CSV files into DataFrames
df1 = pd.read_csv('first.csv')
df2 = pd.read_csv('second.csv')

# Convert the 'word' column of each DataFrame to a set
words1 = set(df1['word'].dropna().str.strip())
words2 = set(df2['word'].dropna().str.strip())

# Find words present in the first CSV but not in the second
diff_words = words1 - words2

# Convert the resulting set back into a DataFrame
result_df = pd.DataFrame(list(diff_words), columns=['word'])

# Save the results to a new CSV file
result_df.to_csv('difference.csv', index=False)

print("Difference CSV created with", len(result_df), "words.")

