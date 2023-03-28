"""Document that processes each text excerpt, and stores attributes"""
import csv
from typing import Any, List, Optional, Tuple


def read_csv(csv_file: str) -> list[]:
    """Load network and packet data from a CSV file.

       Return a TODO of two values:
           - TODO

       Preconditions:
           - csv_file refers to a valid CSV file in the format described on the project handout

    """
    with open(csv_file) as csv_fle:
        reader = csv.reader(csv_fle)
        headers = next(reader)

        list_of_text_Blocks = []
        for row in reader:
            # initialize a text_block with the unique information of each text

            # assign each value to the Text Block Assignment

    return list_of_text_Blocks

def process_blocks(blocks_list: list[TextBlock]) -> list[tuple[int, list[Sentence]]]:
    """
    Processes the text_blocks returned from the csv file and returns a tuple containing an id and
    list of their sentences
    """
    # TODO: take each text block and create a list of sentences within it.


class TextBlock:
    """
    Class storing the text for each novel entry, plus associated attributes from csv

    Instance Attributes:
    TODO


    """
    sentences: list[str]
    title: str
    id: int
    category: str
    pub_year: int
    sentence_count: int

    def average_sentence_length(self) -> float:
        """Returns the average number of words in a sentence"""


class Sentence:
    """
    Class to store each sentence and its associated attributes

    Instance Attributes:
    TODO


    """
    phrase: str
    id: int
    location: str
    carec_m: float
    word_count: Optional[int]

    def __init__(self):
        """initializes the instance attributes of Sentence"""

    def word_count(self):
        """returns number of words in sentence"""


    def sentence_to_list(self):
        """Returns just the words of a sentence. """
