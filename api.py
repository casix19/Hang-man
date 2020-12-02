import os, json, random

#links
dictionaries_path = r"sources\\dict"
dictionaries = os.listdir(dictionaries_path)


rand_word = ""


def random_word():
    random_dictionary = random.choice(dictionaries)
    random_dictionary_path = os.path.join(dictionaries_path, random_dictionary)
    with open(random_dictionary_path, 'r') as f:
        f.seek(0)
        content = json.load(f)
        words = list(content.keys())
        rand_word = random.choice(words)
    return rand_word


def get_definition(word):
    letter = word[0]
    for i in dictionaries:
        if i[1] == letter:
            dictionary_path = os.path.join(dictionaries_path, i)
            with open(dictionary_path, 'r') as f:
                content = json.load(f)
                f.seek(0)
                definition = content[word]["MEANINGS"]
                definition_2 = 'Sorry... no definition'
                for d in definition:
                    if d == '1':
                        definition_2 = ". ".join(content[word]["MEANINGS"][d][:2])

            display = f"Definition: {definition_2}"
            return display


def get_synonyms(word):
    letter = word[0]
    for i in dictionaries:
        if i[1] == letter:
            dictionary_path = os.path.join(dictionaries_path, i)
            with open(dictionary_path, 'r') as f:
                f.seek(0)
                content = json.load(f)
                synonyms = content[word]['SYNONYMS']
                synonyms = ', '.join(synonyms)

            display = f"Synomyms: {synonyms}"
            return display


if __name__ == '__main__':
    word = random_word()
    print(word)
    definition = get_definition(word)
    print(definition)
    synonyms = get_synonyms(word)
    print(synonyms)
