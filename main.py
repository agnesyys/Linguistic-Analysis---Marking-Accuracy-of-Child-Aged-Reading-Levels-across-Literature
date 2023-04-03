"""This file allows user to input a sentence, then all the complexity scores will be shown, as well as a Plotly
 graph to display the results."""
import pygame
import sys
import pygame_gui
import plotly.graph_objects as go

import data_processing
from data_processing import TextBlock, Sentence
from data_processing import read_csv

import complexity_measures
com_m = complexity_measures

pygame.init()
width = 600
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Sentence Difficulty Score")
clock = pygame.time.Clock()
manager = pygame_gui.UIManager((width, height))
text_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((120, 250), (350, 50)), manager=manager,
                                                 object_id='main_text_entry')
text_font = pygame.font.SysFont('Arial', 25)


def draw_text(text, font, text_col, x, y):
    """function for drawing text on pygame screen"""
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def get_closest_carec_score(text: TextBlock) -> float:
    """get a CAREC_M score by comparing Dale_Chall and Flesch complexitity scores from data_set_novels.csv"""
    closest_txt_blk = text
    dc = complexity_measures.dale_chall_complexity(text)
    fc = complexity_measures.flesch_complexity_score(text)

    pos_similar_txt_blk = data_processing.read_csv('data/data_set_novels.csv')
    min_diff = 10000
    for textblock in pos_similar_txt_blk:
        if (textblock.dale_chall and textblock.flesch_reading) is not None:
            diff_dc = dc - textblock.dale_chall
            diff_fc = fc - textblock.flesch_reading
            diff = diff_dc + diff_fc

            if diff <= min_diff:
                closest_txt_blk = textblock
    return closest_txt_blk.carec_m


def standardized_carec_score(score: float) -> float:
    """Standardizes carec score using the following metric, note the end points are exclusive:

        Carec Score Scale:
        4.9 and Below	Grade 4 and Below
        5.0 to 5.9	    Grades 5 - 6
        6.0 to 6.9	    Grades 7 - 8
        7.0 to 7.9	    Grades 9 - 10
        8.0 to 8.9	    Grades 11 - 12
        9.0 to 9.9	    Grades 13 - 15 (College)
        10 and Above	Grades 16 and Above (College Graduate)

        Adjusted to 1.0 Scale:
        0 - 0.2         Grade 4 and Below
        0.2 - 0.45      Grades 5 - 6
        0.45 - 0.65     Grades 7-8
        0.65 - 0.8      Grades 9 - 10
        0.8 - 0.9       Grades 11 - 12
        0.9 - 1.0       Grades 13 - 15 (College)
        1.0 +           Grades 16 and Above (College Graduate)

        """
    if score >= 1:
        return 16
    elif 0.97 <= score < 1:
        return 15
    elif 0.93 <= score < 0.97:
        return 14
    elif 0.90 <= score < 0.93:
        return 13
    elif 0.85 <= score < 0.90:
        return 12
    elif 0.8 <= score < 0.85:
        return 11
    elif 0.75 <= score < 0.8:
        return 10
    elif 0.65 <= score < 0.75:
        return 9
    elif 0.55 <= score < 0.65:
        return 8
    elif 0.45 <= score < 0.55:
        return 7
    elif 0.30 <= score < 0.45:
        return 6
    elif 0.2 <= score < 0.3:
        return 5
    else:
        return 4


def show_text(text_to_show):
    """after input sentence"""
    counter = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill("white")

        new_sentence = Sentence(text_to_show, None, None, None)
        new_sentence.phrase = text_to_show

        new_textblock = TextBlock([new_sentence], None, None, None, None, None, None, None, None, None, None)
        new_textblock.excerpt = [new_sentence]

        dc = com_m.standardized_dale_chall(com_m.dale_chall_complexity(new_textblock))
        fc = com_m.standardized_flesch_ease(com_m.flesch_complexity_score(new_textblock))
        cm = standardized_carec_score(get_closest_carec_score(new_textblock))
        sd = com_m.standardized_syntax_score(com_m.mean_dependency_distance(new_textblock, True))

        draw_text('Sentence Complextity Score', pygame.font.SysFont('Arial', 40), 'black', 50, 30)
        draw_text('Dale-Chall:' + str(dc), text_font, 'black', 50, 100)
        draw_text('Flesch: ' + str(fc), text_font, 'black', 50, 150)
        draw_text('CAREC_M: ' + str(cm), text_font, 'black', 50, 200)
        draw_text('Mean Dependency Distance: ' + str(sd), text_font, 'black', 50, 250)
        # run plotly
        if counter == 0:
            display_reading_level_accuracy(new_textblock, dc, fc, sd)
        counter += 1
        pygame.display.update()


def display_reading_level_accuracy(textblock: TextBlock, dc: float, fc: float, sd: float) -> None:
    """Display a bar graph of the reading level accuracy of a given sentence."""
    if len(textblock.excerpt) == 1:
        cm = standardized_carec_score(get_closest_carec_score(textblock))
    else:
        cm = standardized_carec_score(textblock.carec_m)
    fig = go.Figure(
        data=[go.Bar(y=[dc, fc, sd, cm], x=['Dale-Chall Complexity', 'Flesch Complexity',
                                            'Mean Dependency Distance', 'CAREC_M'])],
        layout_title_text="Reading Levels Accuracy Compared to CAREC M", )
    fig.update_layout(xaxis_title="Sentence Complexity Measures",
                      yaxis_title="Score",
                      title_x=0.5)
    fig.show()


def get_score():
    """Take in a sentence"""
    while True:
        ui_refresher_rate = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == 'main_text_entry':
                show_text(event.text)
            manager.process_events(event)
        manager.update(ui_refresher_rate)
        screen.fill("white")
        draw_text("Enter a sentence:", text_font, (0, 0, 0), 120, 200)
        manager.draw_ui(screen)
        pygame.display.update()


get_score()


def runner() -> None:
    """A runner of the data_set_novels.csv file."""
    textblocks = read_csv('data/data_set_novels.csv')
    counter = 0
    dc = []
    fc = []
    dependency = []
    carec = []
    for textblock in textblocks:
        dc.append(textblock.dale_chall)
        fc = textblock.flesch_reading
        dependency.append(com_m.mean_dependency_distance(textblock, False))
        carec.append(textblock.carec_m)
        counter += 1
    avg_dc = sum(dc) / counter
    avg_fc = sum(fc) / counter
    avg_dependency = sum(dependency) / counter
    avg_carec = sum(carec) / counter

    fig = go.Figure(
        data=[go.Bar(y=[avg_dc, avg_fc, avg_dependency, avg_carec], x=['Dale-Chall Complexity', 'Flesch Complexity',
                                                                       'Mean Dependency Distance', 'CAREC_M'])],
        layout_title_text="Reading Levels Accuracy Compared to CAREC M"
    )
    fig.show()
