"""Document that has all of the nltk tree diagramming"""
from typing import Any

# To add to requirements, install pycorenlp & StanfordCorNLP
# from pycorenlp import StanfordCoreNLP
# nlp = StanfordCoreNLP('http://localhost:9000')

# Import required libraries
import nltk

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
from nltk import pos_tag, word_tokenize, RegexpParser
import nltk.tree

# Example text
sample_text = "The quick brown fox jumps over the lazy dog"


def tag_sentence(sentence: str) -> nltk.tree:
    """Returns a list of tuples of the form (word, word class)

    Preconditions:
    - "." in sentence only once (TODO: Python code)
    """
    # Find all parts of speech in given sentence
    return pos_tag(word_tokenize(sample_text))


def create_tree(tagged_sentence: nltk.tree) -> nltk.tree:
    """
    Using NLTK's parser, generate a syntax tree
    Note that we used NLTK's parser here since it is beyond the scope of our linguistic skills to develop code
    to create a correct syntax tree.
    """
    # Extract all parts of speech from any text
    chunker = RegexpParser("""
                        NP: {<DT>?<JJ>*<NN>} #To extract Noun Phrases
                        P: {<IN>}            #To extract Prepositions
                        V: {<V.*>}           #To extract Verbs
                        PP: {<p> <NP>}       #To extract Prepositional Phrases
                        VP: {<V> <NP|PP>*}   #To extract Verb Phrases
                        """)
    # Return tree all parts of speech in above sentence
    return chunker.parse(tagged_sentence)
