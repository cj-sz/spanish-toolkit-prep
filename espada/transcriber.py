import sys
import pandas as pd

mx_df = pd.read_csv("all_espada_mx_ipas.csv")
prons = mx_df['mx_ipa']

tdf = pd.read_csv("../transcriptions/english_transcriptions.csv")
t_dict = dict(zip(tdf['IPA'], tdf['Toolkit']))
t_dict.pop("ɝ or ɚ")
t_dict.pop("ɑ~ɒ")
t_dict["ɑ"] = "a"
t_dict["ɒ"] = "a"
t_dict["ɚ"] = "3r"
t_dict["ɝ"] = "3r"
# Add eɪ -> 8 as a special transcription
_long = [[("eɪ", "8")]]
# Create a list of tuples for two-character transcriptions
for k, v in t_dict.items():
    if len(k) >= 2:
        _long.append((k, v))

def toolkit_transcribe(p):
    tp = ""
    i = 0
    while i < len(p):
        found = False
        if i < len(p) - 1:
            for lt in _long:
                if p[i:i+2] == lt[0]:
                    tp += lt[1]
                    i += 2
                    found = True
                    break
        if not found:
            try:
                tp += t_dict[p[i]]
            except KeyError:
                return None, p[i]  # Return None and the problematic character
            i += 1
    return tp, None

# Initialize variables to collect failure information
toolkit_pronunciations = []
unique_failures = {}
first_failure = None
valid_rows = []  # Store valid transcriptions for output

# Loop through each row, transcribe, and record failures
for index, row in mx_df.iterrows():
    word = row['word']
    pronunciation = row['mx_ipa']
    toolkit_pron, failed_char = toolkit_transcribe(pronunciation)
    
    if toolkit_pron is None:  # Transcription failed
        if failed_char not in unique_failures:
            unique_failures[failed_char] = (word, pronunciation)  # Store the first example word and its pronunciation for this failure
        if first_failure is None:  # Record first failure if not already set
            first_failure = (word, pronunciation, failed_char)
        toolkit_pronunciations.append("")  # Append empty string for failed transcriptions
    else:
        # Collect valid transcription data
        valid_rows.append((word, pronunciation, toolkit_pron))
        toolkit_pronunciations.append(toolkit_pron)

# Add the transcriptions to the dataframe
mx_df["toolkit_pron"] = toolkit_pronunciations

# Print information on failures
if first_failure:
    print(f"First transcription failure occurred for word '{first_failure[0]}' with pronunciation '{first_failure[1]}'. Failed on character '{first_failure[2]}'")

print("Unique characters that caused transcription failures with example words and pronunciations:")
for char, (example_word, example_pron) in unique_failures.items():
    print(f"Character '{char}' failed in word '{example_word}' with pronunciation '{example_pron}'")

# Print the count of non-empty transcriptions
print((mx_df['toolkit_pron'] != "").sum())

# Export the valid transcriptions to a new CSV file
valid_mx_df = pd.DataFrame(valid_rows, columns=["word", "mx_ipa", "toolkit_pron"])
valid_mx_df.to_csv("valid_mx_transcriptions.csv", index=False)

# Export the dataframe with all words to a CSV file called mx_with_toolkit.csv
mx_df.to_csv("mx_with_toolkit.csv", index=False)
