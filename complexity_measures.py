"""Given a syntax tree, these are implementations of the different collections of complexity measures"""
from data_processing import TextBlock
import csv


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
