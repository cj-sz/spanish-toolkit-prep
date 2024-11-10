import re
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
        p = mx_ipas[entry]
        p = p.replace("/","").replace("ˈ", "").replace("·", "").replace("ː", "").replace("-", "").replace("ˌ", "").replace("\"", "").replace(",","").replace("'̃'", "")
        p = p.replace("r", "ɹ").replace("t̬", "t")
        p = re.sub(r'e(?!ɪ)', 'ɛ', p)
        all_mx_words.loc[len(all_mx_words)] = {
            'word': entry,
            'phonemes': phonemes,
            'mx_ipa': p
        }

# Save the resulting DataFrame to a CSV file
all_mx_words.to_csv("all_espada_mx_ipas.csv", index=False)

print("\033[33mIMPORTANT:\033[0m After running this script, all_espada_mx_ipas.csv was manually updated to include two entries for 'muy' (being the only word in the dictionary with two valid provided pronunciations). This change is not reflected in this script as of right now, I've just left this note here in the meantime.")
