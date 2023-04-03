"""Storage for Mikayla in case of Git Shenanigans"""
import plotly.graph_objects as go
import nltk
import courseProject.data_processing as data
from courseProject.data_processing import read_csv
from courseProject.data_processing import TextBlock, Sentence
from courseProject.complexity_measures import mean_dependency_distance


# from courseProject import complexity_measures as complex


# def display_reading_levels(book: TextBlock) -> None:
#     """Display a bar graph of the reading levels of a given novel."""
#     dc = complex.dale_chall_complexity(book)
#     fc = complex.flesch_complexity_score(book)
#     fig = go.Figure(
#         data=[go.Bar(y=[dc, fc, book.carec_m], x=['Dale-Chall Complexity', 'Flesch Complexity', 'CAREC'])],
#         layout_title_text="Reading Levels Computed by Different Algorithms"
#     )
#     fig.show()
#
#
# def display_reading_level_accuracy(textblock, dc: float, fc: float, sd: float) -> None:
#     """Display a bar graph of the reading level accuracy of a given sentence."""
#
#     fig = go.Figure(
#         data=[go.Bar(y=[dc, fc, sd, textblock.carec_m], x=['Dale-Chall Complexity', 'Flesch Complexity',
#                                                           'Syntatic Difficulty', 'CAREC_M'])],
#         layout_title_text="Reading Levels Accuracy Compared to CAREC M of '" + textblock.title + "'"
#     )
#     fig.show()

def runner() -> None:
    """A runner of the data_set_novels.csv file."""
    textblocks = read_csv('data/data_set_novels.csv')
    counter = 0
    dc = []
    fc = []
    dependency = []
    CAREC = []
    for textblock in textblocks:
        dc.append(textblock.dale_chall)
        fc = textblock.flesch_reading
        dependency.append(mean_dependency_distance(textblock, False))
        CAREC.append(textblock.carec_m)
        counter += 1
    avg_dc = sum(dc) / counter
    avg_fc = sum(fc) / counter
    avg_dependency = sum(dependency) / counter
    avg_CAREC = sum(CAREC) / counter

    fig = go.Figure(
        data=[go.Bar(y=[avg_dc, avg_fc, avg_dependency, avg_CAREC], x=['Dale-Chall Complexity', 'Flesch Complexity',
                                                                       'Mean Dependency Distance', 'CAREC_M'])],
        layout_title_text="Reading Levels Accuracy Compared to CAREC M"
    )
    fig.show()
