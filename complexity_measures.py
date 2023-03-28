"""Given a syntax tree, these are implementations of the different collections of complexity measures"""

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
    # calculate percentage of difficult words


    # calculate average sentence length



def dale_chall_word_list(csv_file: str) -> set[str]:
    """
    Given a text file containing all the Dale Chall familiar words, return a set of those words.
    """



#--------------------------------------------------------------------
def flesch_complexity_score(text: TextBlock) -> float:
    """
    Return the Flesch Reading Ease Readability Formula
    RE = 206.835 – (1.015 x ASL) – (84.6 x ASW)

    RE = Readability Ease

    ASL = Average Sentence Length (i.e., the number of words divided by the number of sentences)

    ASW = Average number of syllables per word (i.e., the number of syllables divided by the number of words)
    """
    # compute average num of syllables per word.




def num_syllables(word: str) -> int:
    """Using English rules for syllabififcation:

    onset:
    root:
    coda:
    Though simple it might seem, the Flesch Reading Ease Formula has certain ambiguities.
    For instance, periods, explanation points, colons and semicolons serve as sentence delimiters;
    each group of continuous non-blank characters with beginning and ending punctuation removed counts as a word;
    each vowel in a word is considered one syllable subject to: (a) -es, -ed and -e (except -le) endings are ignored;
    (b) words of three letters or shorter count as single syllables; and (c) consecutive vowels count as one syllable
    """
