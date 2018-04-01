from nltk.stem.snowball import RussianStemmer
import pymorphy2 as morph

adj_endings_male_hard = ['ый', 'ого', 'ому', 'ым', 'ом', 'ой']
adj_endings_male_soft = ['ий', 'его', 'ему', 'им', 'ем']
adj_endings_female_hard = ['ая', 'ой', 'ую']
adj_endings_female_soft = ['яя', 'ей', 'юю']
adj_endings_neuter_hard = ['ое', 'ого', 'ому', 'ым']
adj_endings_neuter_soft = ['ее', 'его', 'ему', 'им', 'ем']


def adj_to_gender(adjective, gender):
    stemmer = RussianStemmer()
    stem = stemmer.stem(adjective)
    ending = adjective[len(stem):]
    if gender == 'м':
        return adjective
    if ending in adj_endings_male_hard:
        if gender == 'ж':
            return stem + adj_endings_female_hard[0]
        return stem + adj_endings_neuter_hard[0]
    if ending in adj_endings_male_soft:
        if stem[-1:] in ['г', 'к', 'х', 'ц']:
            if gender == 'ж':
                return stem + adj_endings_female_hard[0]
            return stem + adj_endings_neuter_hard[0]
        if gender == 'ж':
            return stem + adj_endings_female_soft[0]
        return stem + adj_endings_neuter_soft[0]


def noun_to_genitive(noun, gender):
    stem = noun[:-1]
    ending = noun[-1:]
    if ending == 'ь':
        if gender == 'м':
            return stem + 'я'
        if gender == 'ж':
            return stem + 'и'
    if ending == 'а':
        if stem[-1:] in ['г', 'к', 'х']:
            return stem + 'и'
        return stem + 'ы'
    if ending == 'я':
        return stem + 'и'
    if ending == 'е' or ending == 'й':
        return stem + 'я'
    if ending == 'о':
        return stem + 'а'
    return noun + 'а'


def adj_to_genitive(adjective, gender):
    stemmer = RussianStemmer()
    stem = stemmer.stem(adjective)
    ending = adjective[len(stem):]
    if ending in adj_endings_male_hard:
        if gender == 'м':
            return stem + adj_endings_male_hard[1]
        elif gender == 'ж':
            return stem + adj_endings_female_hard[1]
        return stem + adj_endings_neuter_hard[1]
    if ending in adj_endings_male_soft:
        if stem[-1:] in ['г', 'к', 'х', 'ц']:
            if gender == 'м':
                return stem + adj_endings_male_hard[1]
            elif gender == 'ж':
                return stem + adj_endings_female_hard[1]
            return stem + adj_endings_neuter_hard[1]
        if gender == 'м':
            return stem + adj_endings_male_soft[1]
        elif gender == 'ж':
            return stem + adj_endings_female_soft[1]
        return stem + adj_endings_neuter_soft[1]


def build_noun_dictionary(filename):
    dict = {}
    file = open(file=filename, encoding='utf-8').readlines()
    for str in file:
        str = str.strip('\n')
        str = str.split('=')
        lemma = str[0]
        info = str[1]
        if 'S' in info:
            if 'муж' in info:
                dict[lemma] = 'м'
            if 'жен' in info:
                dict[lemma] = 'ж'
            if 'сред' in info:
                dict[lemma] = 'с'
    return dict


dictionary = build_noun_dictionary('test_out.txt')

ngrams = open(file='test_bigrams.txt', encoding='utf-8').read().split('\n')
adapted_ngrams = []

for ngram in ngrams:
    ngram = ngram.split('|')[0]
    if ngram.count(' ') == 1:
        word1 = ngram.split(' ')[0]
        word2 = ngram.split(' ')[1]
        if word1 in dictionary and word2 in dictionary:
            word2 = noun_to_genitive(word2, dictionary[word2])
        elif word2 in dictionary:
            word1 = adj_to_gender(word1, dictionary[word2])
        adapted_ngrams.append(word1 + ' ' + word2)
    if ngram.count(' ') == 2:
        word1 = ngram.split(' ')[0]
        word2 = ngram.split(' ')[1]
        word3 = ngram.split(' ')[2]
        if word1 in dictionary and word2 in dictionary and word3 in dictionary:
            word2 = noun_to_genitive(word2, dictionary[word2])
            word3 = noun_to_genitive(word3, dictionary[word3])
        if word1 in dictionary and word3 in dictionary:
            word2 = adj_to_genitive(word2, dictionary[word3])
            word3 = noun_to_genitive(word3, dictionary[word3])
        adapted_ngrams.append(word1 + ' ' + word2 + ' ' + word3)


for w in adapted_ngrams:
    print(w)




# print(adj_to_genitive('синий', 'м'))
# print(adj_to_genitive('синий', 'ж'))
# print(adj_to_genitive('синий', 'с'))
# print(adj_to_genitive('красный', 'м'))
# print(adj_to_genitive('красный', 'ж'))
# print(adj_to_genitive('красный', 'с'))
# print(adj_to_genitive('яркий', 'м'))
# print(adj_to_genitive('яркий', 'ж'))
# print(adj_to_genitive('яркий', 'с'))
# print(adj_to_genitive('рыжий', 'м'))
# print(adj_to_genitive('рыжий', 'ж'))
# print(adj_to_genitive('рыжий', 'с'))

#.\mystem.exe -indl  .\test_origin.txt .\test_out.txt

# print(noun_to_genitive('страна', 'ж'))
# print(noun_to_genitive('земля', 'ж'))
# print(noun_to_genitive('дядя', 'м'))
# print(noun_to_genitive('Юра', 'м'))
# print(noun_to_genitive('стол', 'м'))
# print(noun_to_genitive('герой', 'м'))
# print(noun_to_genitive('конь', 'м'))
# print(noun_to_genitive('окно', 'с'))
# print(noun_to_genitive('поле', 'с'))
# print(noun_to_genitive('сирень', 'ж'))
# print(noun_to_genitive('моделирование', 'с'))