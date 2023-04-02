"""Given a syntax tree, these are implementations of the different collections of complexity measures"""
from data_processing import TextBlock, Sentence
import create_tree as ct
import csv

import nltk
# Import required libraries
import spacy
from nltk import Tree
from spacy import displacy
from pathlib import Path

# spacy.cli.download("en_core_web_sm")
nlp = spacy.load("en_core_web_sm")
from typing import Any, Optional

def dale_chall_complexity(text: TextBlock) -> float:
    """
    Returns the reading grade of a reader who can comprehend your text.

    Raw Score = 0.1579 * (PDW) + 0.0496 * ASL

    Raw Score = Reading Grade of a reader who can comprehend your text at 3rd grade or below.

    PDW = Percentage of Difficult Words

    ASL = Average Sentence Length in words

    If (PDW) is greater than 5%, then:
    Adjusted Score = Raw Score + 3.6365, otherwise Adjusted Score = Raw Score

    Adjusted Score = Reading Grade of a reader who can comprehend your text at 4th grade or above.
    """
    reading_scores_per_sent = []
    PDW_per_sentence = []
    num_diff_words = 0

    word_list = dale_chall_word_list("Dale-Chall Familiar Words")
    for sentence in text.excerpt:
        # calculate percentage of difficult words
        words = sentence.sentence_to_list()
        num_unfamiliar = 0
        for word in words:
            if word not in word_list:
                num_unfamiliar += 1

        # sentence num_unfamiliar percentage:
        PDW_per_sentence += num_unfamiliar / len(words)
        num_diff_words += num_unfamiliar

    # calculate average sentence length
    num_words = sum(len(sentence.sentence_to_list()) for sentence in text.excerpt)
    ASL = num_words / len(text.excerpt)
    PDW = num_diff_words / num_words

    # Calculate Score
    score = 0.1579 * (PDW) + 0.0496 * ASL

    if PDW > 0.05:
        score += 3.6365

    return score


def dale_chall_word_list(csv_file: str) -> set[str]:
    """
    Given a text file containing all the Dale Chall familiar words, return a set of those words.
    """
    with open(csv_file) as csv_fle:
        reader = csv.reader(csv_fle)
        headers = next(reader)

        word_set = set()
        for row in reader:
            # add to word_set
            word_set.add(str(row))

    return word_set


# --------------------------------------------------------------------
def flesch_complexity_score(text: TextBlock) -> float:
    """
    Return the Flesch Reading Ease Readability Formula
    RE = 206.835 – (1.015 x ASL) – (84.6 x ASW)

    RE = Readability Ease

    ASL = Average Sentence Length (i.e., the number of words divided by the number of sentences)

    ASW = Average number of syllables per word (i.e., the number of syllables divided by the number of words)
    """
    # compute average num of syllables per word.
    average_num_syllables = 0
    num_words = 0
    for sentence in text.excerpt:
        sentence_cleaned = sentence.sentence_to_list()
        average_num_syllables += sum(num_syllables(word) for word in sentence_cleaned)
        num_words += len(sentence_cleaned)

    ASW = average_num_syllables / num_words

    # calculate average sentence length
    num_words = sum(len(sentence.sentence_to_list()) for sentence in text.excerpt)
    ASL = num_words / len(text.excerpt)

    reading_ease = 206.835 - 1.015 * ASL - 84.6 * ASW

    return reading_ease


def num_syllables(word: str) -> int:
    """Using English rules for syllabififcation:

    each vowel in a word is considered one syllable subject to: (a) -es, -ed and -e (except -le) endings are ignored;
    (b) words of three letters or shorter count as single syllables; and (c) consecutive vowels count as one syllable

    """
    vowels = {"a", "e", "i", "o", "u"}
    length = len(word)
    if length <= 3:
        return 1

    i = 0
    syll_num = 0
    while i < length:
        # if word starts in a vowel, go until next consonant
        ending_conditions = (i == length - 2 and word[i] + word[i + 1] not in {"ed", "es"}) \
                            or (i == length - 1 and word[i] != "e") or (i < length - 2) or \
                            (i == length - 1 and word[i] == "e" and word[i-1] == "l")

        if (word[i] in vowels) and (word[i-1] not in vowels) and ending_conditions:
            syll_num += 1

        i += 1

    return syll_num

# -----------------------------------------
def mean_dependency_distance(sentence: str):
    """Calculates the mean_dependency_distance given a sentence

    The Mean Dependency Distance (MDD) is:
    MDD(the sentence) = 1/(n-1) * summation of |D*Di| from i = 1 to n-1

    where DDi is the DD (dependency distance) of the ith syntactic link in the sentence.
    Note that the root of the sentence does not have a governor, and so will have a DD of 0.

    The dependency distance of adjacent words is 1, and dependency distance is defined
    as the (absolute) distance between the governor word and its dependent.

    Example:
        "The girl ate an apple" has dependencies:
        The: 1 (dependent of girl, dist 1)
        girl: 1 (dependent of ate, dist 1)
        ate: 0 (verb, has no governer, not dependent of anything)
        an: 1 (dependent of apple, dist 1)
        apple: 2 (dependent of ate, distance 2)
    """
    # Generally: this function calculates the distance between each word and its dependent in the sentence,
    # by traversing through the tree.
    # to calculate MDD, we begin with creating a dependency tree.
    tree = nltk_spac_tree(sentence, False)
    # tree.pretty_print()

    # Then, for each word in the tree, which we refer to as the ith word based on sentence position
    # we need to get, for every subtree, the distance between root and children if there is only one child.

    dependents = []
    flatten(get_dependents(tree), dependents)
    # we can now take every pair to get their distances, by finding their position in the sentence.
    # Since dependency tree is formed left to right, going from i =0  to i = len(sentence) - 1
    # will maintain the order in case of duplicates
    distances = []
    for i in range(0, len(sentence), 2):
        distances.append(abs(sentence.index(dependents[i], i - 1) - sentence.index(dependents[i + 1], i - 1)))

    # lastly, summ all DDs and divide by num of words in sentence
    return sum(distances) / len(sentence)


def get_dependents(tree: nltk.tree) -> list[list[nltk.tree]] | None:
    """Get dependents in pairs

    Note that the NLTK built-in methods for nltk.tree in this function add the following conditions:
    tree.subtrees() returns ALL the constituent trees, this includes the subtrees of its subtrees (and so on).
    It does not return ANY leaves, even those which are direct children of the tree's root.
    It also returns itself as one of the listed subtrees.

    tree.leaves() returns ALL the leaves across the full tree, i.e all the descendants which are leaves

    tree.label() is analogous to the in-class tree.root, and returns the root value of the tree
    """
    # Then, for each word in the tree, which we refer to as the ith word based on sentence position,
    tree_root = tree.label()
    dependents = []

    # we need to get, for every subtree, the distance between root and children if there is a direct child leaf.
    if len(tree.leaves()) >= 1:
        # all leaves, direct subs are not included
        for leaf in tree.leaves():
            subtrees_sans_original = [subtree for subtree in tree.subtrees() if subtree.label() != tree.label()]
            direct_leaf_condition = not any(leaf in subtree.leaves() for subtree in subtrees_sans_original)
            if direct_leaf_condition:
                dependents.append([tree_root, leaf])

    for subtree in tree.subtrees():
        if subtree.label() != tree_root:
            # create a pair with root and every child, confirm that the subtree is a direct child of tree
            subtree_direct_child_of_tree_root = []
            if subtree_direct_child_of_tree_root:
                dependents.append([subtree.label(), tree_root])
            print([subtree.label(), tree_root])
            dependents.append(get_dependents(subtree))

    return dependents

def is_empty(tree) -> bool:
    """Return whether this tree is empty.
    """
    return tree.label() is None

def len_tree(tree: nltk.tree):
    if tree.leaves() == []:
        return 0
    else:
        size = 1  # count the root
        for subtree in tree.subtrees():
            size += len_tree(subtree)  # could also write len(subtree)
        return size

def flatten(nested_list: str | list, unnested: list) -> None:
    """Return the items of the given nested list.

    This version uses a comprehension and the built-in sum aggregation function.
    """
    if isinstance(nested_list, str):
        unnested.append(nested_list)
    else:
        unnested.append(flatten(sublist, []) for sublist in nested_list)


def nltk_spac_tree(sentence: str, attr_included: Optional[bool] = False) -> nltk.tree:
    """
    Visualize the SpaCy dependency tree with nltk.tree
    """
    # gets all the tokenized info
    doc = nlp(sentence)
    tree = [to_nltk_tree(sentence.root, attr_included) for sentence in doc.sents]
    # The first item in the list is the full tree
    return tree[0]
    # tree[0].draw()

def to_nltk_tree(node, attri_included):
    """Return its tokenized format"""
    if node.n_lefts + node.n_rights > 0:
        return Tree(token_format(node, attri_included), [to_nltk_tree(child, attri_included) for child in node.children])
    else:
        return token_format(node, attri_included)

def token_format(token, attrib_included):
    """return its tokenized format as a continuous string with all info
    token.orth_: word (string representation)
    token.tag_: part of speech
    token.dep_: dependancy
    """
    if attrib_included:
        return "_".join([token.orth_, token.tag_, token.dep_])
    else:
        return token.orth_



# TODO: standardize complexity measures scale
def standardized_dale_chall(dc_score: float) -> float:
    """Standardizes DC score using the following metric:





    """
    return dc_score


def standardized_flesch_kincaid(fk_score: float) -> float:
    """Standardizes FK score using the following metric:





    """
    return fk_score


def standardized_syntax_score(syn_score: float) -> float:
    """Standardizes FK score using the following metric:





    """
    return syn_score
