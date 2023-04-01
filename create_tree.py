"""Creating a tree from a sentence using spacy"""
import nltk
# Import required libraries
import spacy
from nltk import Tree
from spacy import displacy
from pathlib import Path

# spacy.cli.download("en_core_web_sm")
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
    # displacy.serve(doc, style='dep')


def nltk_spacy_tree(sentence: str) -> nltk.tree:
    """
    Visualize the SpaCy dependency tree with nltk.tree
    """
    doc = nlp(sentence)

    def token_format(token):
        return "_".join([token.orth_, token.tag_, token.dep_])

    def to_nltk_tree(node):
        if node.n_lefts + node.n_rights > 0:
            return Tree(token_format(node), [to_nltk_tree(child) for child in node.children])
        else:
            return token_format(node)

    tree = [to_nltk_tree(sent.root) for sent in doc.sents]
    # The first item in the list is the full tree
    return tree[0]
    # tree[0].draw()
