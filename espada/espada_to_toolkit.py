import os
import pandas as pd 
import json 
import tqdm

# Load the CSV files
df1_loaded = pd.read_csv('SpanishAnnotatedDictionary_part1.csv')
df2_loaded = pd.read_csv('SpanishAnnotatedDictionary_part2.csv')
df3_loaded = pd.read_csv('SpanishAnnotatedDictionary_part3.csv')

# Concatenate the dataframes
espada_df = pd.concat([df1_loaded, df2_loaded, df3_loaded], ignore_index=True)

# Filter the dataframe to include only rows where "MX" is not "N"
espada_df = espada_df[espada_df['MX'] != 'N']

# Load the JSON file
with open('es_MX.json', 'r', encoding="UTF-8") as file:
    mx_ipas = json.load(file)

# Create an empty DataFrame to store the results
all_mx_words = pd.DataFrame(columns=['word', 'phonemes', 'mx_ipa'])

# Iterate through each row of the filtered espada_df
for index, row in tqdm.tqdm(espada_df.iterrows(), total=espada_df.shape[0]):
    entry = row['Entry']
    phoneme_sequence = row['MainBase']
    phonemes = phoneme_sequence.split()
    
    # Check if the word exists in mx_ipas
    if entry in mx_ipas:
        all_mx_words.loc[len(all_mx_words)] = {
            'word': entry,
            'phonemes': phonemes,
            'mx_ipa': mx_ipas[entry]
        }

# Save the resulting DataFrame to a CSV file
all_mx_words.to_csv("all_espada_mx_ipas.csv", index=False)
