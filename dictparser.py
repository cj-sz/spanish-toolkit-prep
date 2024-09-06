import os

words = []

# collect words and their pronunciations
with open("cmudict_es.txt", encoding='utf-8') as file:
    for line in file.readlines():
        parts = line.strip().split()
        word = parts[0]
        pronunciation = ''.join(parts[1:])
        words.append((word, pronunciation))

output_dir = 'wordonly'
os.makedirs(output_dir, exist_ok=True)

# chunks of 5,000
max_lines_per_file = 5000
num_files = (len(words) + max_lines_per_file - 1) // max_lines_per_file

for i in range(num_files):
    start_index = i * max_lines_per_file
    end_index = min(start_index + max_lines_per_file, len(words))
    
    output_file = os.path.join(output_dir, f"cmudict_es_wordonly_part{i+1}.txt")
    
    with open(output_file, 'w', encoding='utf-8') as file:
        for word, _ in words[start_index:end_index]:
            file.write(word + "\n")
