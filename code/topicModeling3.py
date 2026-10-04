import nltk
from nltk.corpus import stopwords
stopword = stopwords.words('greek')
from stopwordsiso import stopwords
isostopwords = stopwords(["el"])
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation as LDA
from gr_nlp_toolkit import Pipeline

newstopword= ['ένας', 'μια', 'ένα', 'αυτός', 'αυτή', 'αυτό', 'εγώ', 'εσύ', 'αυτούς', 'αυτών', 'εμείς', 'εσείς', 'αυτοί', 'αυτές', 'αυτά', 'έχει', 'έχω', 'έχεις', 'έχουμε', 'έχετε', 'έχουν', 'είχα', 'είχες', 'είχε', 'είχαμε', 'είναι', 'οποία', 'μου', 'συνάδελφοι', 'όπως', 'μία', 'λόγο', 'μπορεί', 'δημοκρατίας', 'εδώ', 'προεδρευων', 'δύο', 'διότι', 'πρέπει', 'στις', 'όταν', 'οποίο', 'προς', 'σήμερα', 'πω', 'λοιπόν', 'τώρα', 'πολιτική', 'γίνει', 'αθανάσιος', 'είναι', 'ότι', 'τη', 'σας', 'αλλά', 'κυβέρνηση', 'υπάρχει', 'αυτήν', 'όμως', 'εγώ', 'μόνο', 'ούτε', 'είπε', 'εσείς', 'ήθελα', 'της', 'από' 'τους', 'γιατί', 'κύριοι', 'στα', 'πολύ', 'όχι', 'μέσα', 'βουλή', 'βουλής', 'προεδρος', 'στους', 'μας', 'κύριε', 'ήταν', 'θέμα', 'ως', 'πρόεδρε', 'υπουργός', 'νέας', 'επί', 'υπάρχουν', 'άρθρο', 'μέχρι', 'υπουργό', 'δηλαδή', 'αναφορά', 'υπουργέ', 'υπ', 'κάθε', 'νομοσχέδιο', 'πρόβλημα', 'εθνικής', 'ερώτηση', 'απάντηση', 'κάνει', 'εκεί', 'λέει', 'οποίες', 'διατάξεις', 'αριθμ', 'ακόλουθη', 'αριθμό', 'έγγραφο', 'δόθηκε', 'έτσι', 'κύριος', 'σχετικά', 'όλα', 'άρθρου', 'αφορά', 'νομίζω', 'άλλο', 'οικονομικών', 'βουλευτής', 'ζητεί', 'παναγιώτης', 'χρόνια', 'συζήτηση', 'προεδρος', 'χώρα','γίνεται', 'εξής', 'επίσης', 'κατέθεσε', 'προεδρευων', 'υφυπουργός', 'χωρίς', 'νέα', 'νόμου', 'υπουργείου', 'κυβέρνησης', 'γι', 'έγινε', 'θέματα', 'τρόπο', 'προβλήματα', 'θέλω', 'επιτροπή', 'κωνσταντίνος', 'πω', 'πασοκ', 'ευρώ', 'σελ', 'ανάπτυξης', 'κυρίες', 'ευχαριστώ', 'ιωάννης', 'υγείας', 'κοινωνικής', 'γεώργιος', 'πρόεδρος', 'υπουργών', 'υπουργείο', 'ελληνικής', 'κοινωνίας', 'οικονομίας', 'δημοκρατία', 'ελληνική', 'υπουργός', 'υπουργού', 'υπουργών', 'κυβέρνηση', 'κυβέρνησης', 'κυβερνήσεως', 'κυβερνητική', 'κυβερνητικές', 'λαός', 'κύριε', 'κυρία', 'κυρίες']

allstopwords = stopword + list(isostopwords)+ newstopword

nlp = Pipeline("pos,ner")  # Instantiate the Pipeline with the POS and NER processors
with open("data/1989.txt", "r", encoding="utf-8") as f:
    text = f.read()
    chunks = text.split("\n")

#i get the error 'RuntimeError: The expanded size of the tensor (2576295) must match the existing size (512) at non-singleton dimension 1. Target sizes: [1, 2576295]. Tensor sizes: [1, 512]'
MAX_WORDS = 200

words = text.split()

chunks = []

for i in range(0, len(words), MAX_WORDS):
    chunk = " ".join(words[i:i + MAX_WORDS])
    chunks.append(chunk)

for chunk in chunks:
    if not chunk.strip():
        continue

    doc = nlp(chunk)# Process the tokenized text with the pipeline
    
    # iterate over the generated tokens
    cleantokens1989=[]
    for token in doc.tokens:
        if token.text not in allstopwords and token.text.isalpha(): #check if the token is not a stopword and is alphabetic
            if token.upos== "NOUN":
                cleantokens1989.append(token.text) #add only nouns to the tokens list

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


def modeling(text):
    # Convert lists of tokens into strings
    text = [" ".join(tokens) for tokens in text]
        # Initialise the count vectorizer with the English stop words
    count_vectorizer = CountVectorizer()
        # Fit and transform the processed data
    data = count_vectorizer.fit_transform(text)
        #each year will be modeled with 5 topics and 15 words per topic
    number_topics = 5
    number_words = 15
    lda = LDA(n_components=number_topics)
    lda.fit(data)
    print_topics(lda, count_vectorizer, number_words) 


print("Topics found via LDA:")
modeling(cleantokens1989)