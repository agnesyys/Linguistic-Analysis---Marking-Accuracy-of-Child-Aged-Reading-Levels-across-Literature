"""Document that processes each text excerpt, and stores attributes"""
from __future__ import annotations
import csv
from typing import Optional
import string


def read_csv(csv_file: str) -> list[TextBlock]:
    """Load network and packet data from a CSV file.

       Return a TODO of two values:
           - TODO

       Preconditions:
           - csv_file refers to a valid CSV file in the format described on the project handout

    """
    with open(csv_file) as csv_fle:
        reader = csv.reader(csv_fle)
        headers = next(reader)
        list_of_text_blocks = []

        for row in reader:
            # Turn the excerpt in each row into a list of Sentences
            counter = 0
            periods = [0]
            # Find the indices of the end of the sentences
            for x in row[7]:
                if x == '.' or x == '?' or x == '!':
                    periods.append(counter + 1)
                counter += 1
            # Create a Sentence for each sentence
            sentences = []
            for i in range(0, len(periods) - 1):
                sentences.append(Sentence(phrase=row[7][periods[i]: periods[i + 1]], id=int(row[0]), location=row[6],
                                          carec_m=float(row[8])))
                sentences[-1].word_count = sentences[-1].calculate_word_count()

            # initialize a text_block with the unique information of each text
            list_of_text_blocks.append(TextBlock(id=int(row[0]), author=row[1], title=row[2], url=row[3],
                                                 category=row[5], location=row[6], excerpt=sentences,
                                                 carec_m=float(row[8]),
                                                 sentence_count=counter))
            if row[4] != '':
                list_of_text_blocks[-1].pub_year = row[4]
    # return a list of TextBlocks
    return list_of_text_blocks


def process_blocks(blocks_list: list[TextBlock]) -> list[tuple[int, list[Sentence]]]:
    """
    Processes the text_blocks returned from the csv file and returns a tuple containing an id and
    list of their sentences

    Format: [id, [list of Sentences]]
    """
    identifier = 0
    new_lst = []
    for i in blocks_list:
        new_lst.append((identifier, i.excerpt))
        identifier += 1
    return new_lst


class TextBlock:
    """
    Class storing the text for each novel entry, plus associated attributes from csv

    Instance Attributes:
    - id: a unique identifier of a textblock
    - author: the name of the person who wrote the excerpt
    - title: the title of the book
    - url:
    - pub_year: the year of publication of the book, if pub_year = 0, then the publishing year is unknown
    - category:
    - location:
    - excerpt: a portion of the book
    - carec_m:
    - sentence_count: the number of sentences in the excerpt

    """
    id: int
    author: str
    title: str
    url: str
    pub_year: Optional[int]
    category: str
    location: str
    excerpt: list[Sentence]
    carec_m: float
    sentence_count: int

    def __init__(self, id: int, author: str, title: str, url: str, category: str, location: str,
                 excerpt: list[Sentence], carec_m: float, sentence_count: int, pub_year: Optional[int] = 0, ):
        """initializes the instance attributes of TextBlock"""
        self.id = id
        self.author = author
        self.title = title
        self.url = url
        self.pub_year = pub_year
        self.category = category
        self.location = location
        self.excerpt = excerpt
        self.carec_m = carec_m
        self.sentence_count = sentence_count

    def average_sentence_length(self) -> float:
        """Returns the average number of words in a sentence."""
        counter = 0
        sum_so_far = 0
        for i in self.excerpt:
            sum_so_far += i.word_count
            counter += 1
        return sum_so_far / counter


class Sentence:
    """
    Class to store each sentence and its associated attributes

    Instance Attributes:
    - phrase: a sentence in str form
    - word_count: the number of words in the phrase

    Preconditions:
    - self.phrase[-1] == '.' or self.phrase[-1] == '?' or self.phrase[-1] == '!'
    - len(self.phrase) > 0
    - self.word_count > 0

    """
    phrase: str
    id: int
    location: str
    carec_m: float
    word_count: Optional[int]

    def __init__(self, phrase: str, id: int, location: str, carec_m: float):
        """initializes the instance attributes of Sentence."""
        self.phrase = phrase
        self.id = id
        self.location = location
        self.carec_m = carec_m
        self.word_count = self.calculate_word_count()

    def calculate_word_count(self) -> int:
        """Returns number of words in sentence.

        Preconditions:
        - self.calculate_word_count() > 0
        """
        return len(self.phrase.split(' '))

    def sentence_to_list(self) -> list[str]:
        """Returns just the words of a sentence.

        Preconditions:
        - len(self.sentence_to_list()) > 0
        """
        # for i in '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~':
        #   temp = self.phrase.replace(i, '')
        temp = self.phrase.translate(str.maketrans('', '', string.punctuation))
        return temp.split(' ')
