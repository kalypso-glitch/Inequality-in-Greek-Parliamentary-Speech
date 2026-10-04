from pathlib import Path
from unittest import result
import nltk
from nltk.corpus import stopwords
stopword = stopwords.words('greek')
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation as LDA

#cleaning the data from each year
def cleaning(text):
    tokens=nltk.word_tokenize(open(text, encoding="utf-8").read())
    tokens_lower = [t.lower() for t in tokens] 
    tokens_clean = [w for w in tokens_lower if w not in stopword and w.isalpha()]
    return tokens_clean


def print_topics(model, count_vectorizer, n_top_words):
    # get the word names from the BOW count vector
    words = count_vectorizer.get_feature_names_out()
    for topic_idx, topic in enumerate(model.components_):
        print("\nTopic #%d:" % topic_idx)
        # topic is a vector of probabilities for each word from the corpus
        # .argsort() returns a list of indices to access in that order to obtain a sorted 
        # (ascending) version of the topic array
        idxs = topic.argsort()
        # reverse the list to obtain descending sort order -- the most important keywords 
        # (their indices) are now in front
        idxs = idxs[::-1]
        # get the top words for each topic from the BOW vector
        print(" ".join([words[i] for i in idxs[:n_top_words]]))



def outfile():
    for file in Path('data').glob('*.txt'):
        text=cleaning(file)
        # Initialise the count vectorizer with the English stop words
        count_vectorizer = CountVectorizer()
        # Fit and transform the processed data
        data = count_vectorizer.fit_transform(text)
        #each year will be modeled with 5 topics and 15 words per topic
        number_topics = 5
        number_words = 15
        lda = LDA(n_components=number_topics)
        lda.fit(data)

        title= f'{file}_topics'
        with open(title+'.txt', 'w', encoding="utf-8") as outfile:
            result= print_topics(lda, count_vectorizer, number_words)   
            outfile.write('Topics found via LDA')
            outfile.write(str(result))
    

outfile()
