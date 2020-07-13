## Import python library
import pandas as pd
import nltk


def data_augmentation_spacy(df,short_desc_colname,desc_colname):
    df['Assignment_Group_Updated'] = df['Assignment group'].apply(str)
    df['Assignment group'] = df['Assignment group'].apply(str)
    df.sort_values(by='Assignment_Group_Updated', axis=0, inplace=True)
    df.reset_index(drop=False, inplace=True)

    df['Assignment_Group_Updated'][:800] = "GRP_00"
    df['Assignment_Group_Updated'][800:1600] = "GRP_01"
    df['Assignment_Group_Updated'][1600:2400] = "GRP_02"
    df['Assignment_Group_Updated'][2400:3200] = "GRP_03"
    df['Assignment_Group_Updated'][3200:3976] = "GRP_04"

    print(df['Assignment_Group_Updated'].value_counts())

    df['Description_updated'] = df[short_desc_colname].apply(str) + ' ' + df[desc_colname].apply(str)

    nltk.download('stopwords')
    # load nltk's English stopwords as variable called 'stop' and don't find synonym of those words.
    stop = nltk.corpus.stopwords.words('english')

    ## Tokenizing sentence into token for finding synonym.
    def make_tokenizer(texts):
        from keras.preprocessing.text import Tokenizer
        t = Tokenizer()
        t.fit_on_texts(texts)
        return t

    tokenizer = make_tokenizer(df['Description_updated'])  ## Message is column name

    X = tokenizer.texts_to_sequences(df['Description_updated'])

    from keras.preprocessing.sequence import pad_sequences
    X = pad_sequences(X, 70)

    ## Dictionary of word index
    index_word = {}
    for word in tokenizer.word_index.keys():
        index_word[tokenizer.word_index[word]] = word

    ## word list
    words = [value for key, value in index_word.items()]

    ## Function to find synonym of words
    import spacy
    nlp = spacy.load('en', parser=False)

    def check_lemma(t, w):
        r = [d for d in t if (nlp(d.text)[0].lemma_ != nlp(w.text)[0].lemma_)]
        return r

    def get_word_synonym(word):
        filtered_words = [w for w in word.vocab if (
            not w.lower_ in stop) and w.is_lower == word.is_lower and w.prob >= -15]  ## (not w.lower_ in stop) and
        similarity = sorted(filtered_words, key=lambda w: word.similarity(w), reverse=True)
        filtered_similarity = check_lemma(similarity[:30], word)
        return filtered_similarity[:3]

    ## Synonym dictionary
    synonym_dict = {}

    def check_oos(synonym_dict, key):
        if key in synonym_dict.keys():
            return True
        else:
            return False

    for word in words:
        # if (not check_oos(word)) :
        if (not check_oos(synonym_dict, word)):
            synonym_dict.update({word: tuple([w.lower_ for w in get_word_synonym(nlp.vocab[word])])})
            # print(word, " : ", [w.lower_ for w in get_word_synonym(nlp.vocab[word])])

    ## Only consider filtered synonym
    import collections
    value_occurrences = collections.Counter(synonym_dict.values())

    filtered_synonym = {key: value for key, value in synonym_dict.items() if value_occurrences[value] == 1}

    ## Function for augmenting data by replacing words with synonym using spaCy

    import re
    import random
    sr = random.SystemRandom()
    split_pattern = re.compile(r'\s+')

    def data_augmentation(message, aug_range=1):
        augmented_messages = []
        for j in range(0, aug_range):
            new_message = ""
            for i in filter(None, split_pattern.split(message)):
                new_message = new_message + " " + sr.choice(filtered_synonym.get(i, [i]))
            augmented_messages.append(new_message)
        return augmented_messages

    ## Dictionary for group count
    ## Assignment Group is column name
    group_count = df['Assignment_Group_Updated'].value_counts().to_dict()

    ## Get max intent count to match other minority classes through data augmentation
    import operator
    max_group_count = max(group_count.items(), key=operator.itemgetter(1))[1]

    ## Loop to interate all messages
    import numpy as np
    import math
    import tqdm
    newdf = pd.DataFrame()
    for group, count in group_count.items():
        count_diff = max_group_count - count  ## Difference to fill
        multiplication_count = math.ceil(
            (count_diff) / count)  ## Multiplying a minority classes for multiplication_count times
        if (multiplication_count):
            old_message_df = pd.DataFrame()
            new_message_df = pd.DataFrame()
            for message in tqdm.tqdm(df[df["Assignment_Group_Updated"] == group]["Description_updated"]):
                ## Extracting existing minority class batch
                dummy1 = pd.DataFrame([message], columns=['Description_updated'])
                dummy1["Assignment_Group_Updated"] = group
                old_message_df = old_message_df.append(dummy1)

                ## Creating new augmented batch from existing minority class
                # new_messages = data_augmentation(message, language, multiplication_count)
                new_messages = data_augmentation(message, multiplication_count)
                dummy2 = pd.DataFrame(new_messages, columns=['Description_updated'])
                dummy2["Assignment_Group_Updated"] = group
                new_message_df = new_message_df.append(dummy2)

            ## Select random data points from augmented data
            new_message_df = new_message_df.take(np.random.permutation(len(new_message_df))[:count_diff])

            ## Merge existing and augmented data points
            newdf = newdf.append([old_message_df, new_message_df])
        else:
            newdf = newdf.append(df[df["Assignment_Group_Updated"] == group])

    newdf['Assignment_Group_Updated'].replace(to_replace=["GRP_00", "GRP_01", "GRP_02", "GRP_03", "GRP_04"],
                                                     value="GRP_0", inplace=True)
    return newdf