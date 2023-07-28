# Project-CSC111

**Problem Description and Research Question**
In the domain of linguistics, there are many different ways to rate the complexity and difficulty of texts. Using a
combination of factors, such as sentence length, variety of syntactic word classes, word difficulty, and the complexity
of the sentence structure, one can develop a model to rate whether a given text is appropriate for an age group, such
as the analysis which is necessary for the production of age-appropriate children’s literature, or in ensuring news
articles are readable.

With such a variety of different measures used to measure the complexity and difficulty of texts, we wanted to
compare different models and analyze their accuracy in different contexts, especially in looking at when some models
are more successful than others. We focus specifically on analysing their accuracy in regards to children’s literature
here since complexity is more so defined on syntactic and structural sentence complexity, as opposed to text targeted
at adults, where the difficulty is often measured by the use of niche terminology and uncommon vocabulary.

Ultimately, our question is: **How aligned are varying processes of measuring text difficulty and complexity of children’s literature in returning a target age group?**

The different models of measuring complexity we will be implementing in this project are:
1. Dale Chall: Compares its wordlist with a text and calculates a difficulty level based on the number of difficult
words and average sentence length.
2. Flesch Kincaid Grade Level: Uses a metric that combines a number of words, sentences, and syllables to return
a grade level.
3. Syntactic Difficulty: This uses measures of the length of a production unit, amount of subordination, amount
of coordination and degree of phrasal complexity. (Note that we will be using attributes of nodes to keep track
of each word’s class/type, and then the hierarchical structure to track dependency within a clause and phrasal
complexity)
4. CAREC (Crowdsourced Algorithm of Reading Comprehension): Grade levels as set by teachers as opposed by
an algorithm and will serve as a “control”. (Note that this can be accessed from the given dataset)


**Works Cited ---------------------------------------------------------------------------------------------------------------------------------------**
Crossley, Scott, et al. “A large-scaled corpus for assessing text readability.” Springer Nature, 16 Mar. 2022, https://doi.org/10.3758/s13428-022-01802-x. Accessed 7 Mar. 2023.

Crossley, Scott, et al. “The Commonlit Ease of Readability (CLEAR) Corpus.” https://educationaldatamining.org/EDM2021/virtual/static/pdf/EDM21_paper_35.pdf. Accessed 7 Mar. 2023.

“Flesch Reading Ease and the Flesch Kincaid Grade Level.” Readable, https://readable.com/readability/flesch-reading-ease-flesch-kincaid-grade-level/#:~:text=The%20Flesch%20Reading%20Ease%20gives,the%201940s%20by%20Rudolf%20Flesch. Accessed 7 Mar. 2023.

“Free Dale-Chall Readability Formula with Word List - Original and Revised Versions.” Readability Formulas, https://readabilityformulas.com/free-dale-chall-test.php. Accessed 7 Mar. 2023.

Hudson, Richard, “Measuring syntactic difficulty.” Sept. 1995, https://dickhudson.com/wp-content/uploads/2013/07/Difficulty.pdf. Accessed 7 Mar. 2023.
Liu, Kanglong and Mohammad Afzaal, “Syntactic complexity in translated and non-translated texts: A corpusbased study of simplification.” PLOS ONE, 24 June 2021, https://doi.org/10.1371/journal.pone.0253454. Accessed 7 Mar. 2023.
