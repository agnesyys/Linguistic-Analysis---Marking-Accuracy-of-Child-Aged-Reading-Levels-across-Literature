"""Creating a tree from a sentence using spacy"""
import nltk
import spacy
from nltk import Tree
from spacy import displacy
from pathlib import Path

spacy.cli.download("en_core_web_sm")
nlp = spacy.load("en_core_web_sm")


def dependency_diagram(sentence: str) -> None:
    """Takes in a sentence and returns its dependecies diagram.

    Text: The original word text.
    Lemma: The base form of the word.
    POS: The simple UPOS part-of-speech tag.
    Tag: The detailed part-of-speech tag.
    Dep: Syntactic dependency, i.e. the relation between tokens.
    Shape: The word shape – capitalization, punctuation, digits.
    is alpha: Is the token an alpha character?
    is stop: Is the token part of a stop list, i.e. the most common words of the language?
    """
    doc = nlp(sentence)
    for token in doc:
        print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
              token.shape_, token.is_alpha, token.is_stop)

def nltk_spacy_tree(sentence: str, attr_included: bool) -> nltk.tree:
    """
    Visualize the SpaCy dependency tree with nltk.tree
    """
    # gets all the tokenized info
    doc = nlp(sentence)

    def token_format(token, attrib_included):
        """return its tokenized format, continuous string with all info
        token.orth_: word (string representation)
        token.tag_: part of speech
        token.dep_: dependancy
        """
        if attrib_included:
            return "_".join([token.orth_, token.tag_, token.dep_])
        else:
            return token.orth_

    def to_nltk_tree(node, attri_included):
        """Return its tokenized format"""
        if node.n_lefts + node.n_rights > 0:
            return Tree(token_format(node, attri_included), [to_nltk_tree(child, attr_included) for child in node.children])
        else:
            return token_format(node, attri_included)

    tree = [to_nltk_tree(sent.root, attr_included) for sent in doc.sents]
    # The first item in the list is the full tree
    return tree[0]
    # tree[0].draw()
