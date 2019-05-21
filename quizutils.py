import string, copy

ukrainian_lowercase_vowels = "аоуеиіяюєї"
ukrainian_uppercase_vowels = "АОУЕИІЯЮЄЇ"

def make_lower(word):
    word = list(word)
    for i in range(len(word)):
        if word[i] in ukrainian_uppercase_vowels:
            word[i] = ukrainian_lowercase_vowels[ukrainian_uppercase_vowels.index(word[i])]
    return ''.join(word)

def load_questions():
    f = open("questions.txt","r")
    questions = dict()
    for word in f:
        word = word.strip()
        if word == '#':
            break
        q = make_lower(word)
        questions[q] = [[],[]]
        if word.find(' (') != -1: word = word[:word.find(' (')]
        correct = word
        word = make_lower(word)
        for i in range(len(word)):
            if correct[i] in ukrainian_uppercase_vowels:
                questions[q][1].append(word[:i] + correct[i] + word[i+1:])
        bal = 0
        for i in range(len(word)):
            if bal == 0 and word[i] in ukrainian_lowercase_vowels:
                idx = ukrainian_lowercase_vowels.index(word[i])
                temp = word[:i] + ukrainian_uppercase_vowels[idx] + word[i+1:]
                questions[q][0].append(temp)
            elif word[i] == '(': bal += 1
    f.close()
    print("skidish")
    return questions
    #print(questions)