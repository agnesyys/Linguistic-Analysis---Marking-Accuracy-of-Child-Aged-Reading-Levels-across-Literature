"""CSC111 Winter 2023

Instructions (READ THIS FIRST!)
===============================
This file contains the implementations for the nltk implementation of creating a tree, using nlp's tokenizers

Copyright and Usage Information
===============================

This file is Copyright (c) 2023 Lana Wehbeh, Mikayla Pradeepan, and Agnimport nltk
"""
import nltk
import spacy
from nltk import Tree
from typing import Any

spacy.cli.download("en_core_web_sm")
nlp = spacy.load("en_core_web_sm")

def nltk_spacy_tree(sentence: str, attr_included: bool) -> nltk.tree:
    """Visualize the SpaCy dependency tree with nltk.tree

    if attr_included is True, then part of speech and syntactic dependency are included
    if attr_included is False, then only the words is included in the nltk.tree
    """
    # gets all the tokenized info
    doc = nlp(sentence)
    tree = [to_nltk_tree(sent.root, attr_included) for sent in doc.sents]
    # The first item in the list is the full tree
    return tree[0]


def token_format(token, attr_included) -> Any:
    """Return its tokenized format, continuous string with all info

    token.orth_: word (string representation)
    token.tag_: part of speech
    token.dep_: dependancy
    """
    if attr_included:
        return "_".join([token.orth_, token.tag_, token.dep_])
    else:
        return token.orth_


def to_nltk_tree(node, attr_included) -> Any:
    """Return nltk tree of the sentence
    If there's no subtrees, then return itself (the node)
    """
    if node.n_lefts + node.n_rights > 0:
        return Tree(token_format(node, attr_included), [to_nltk_tree(child, attr_included) for child in node.children])
    else:
        return token_format(node, attr_included)
