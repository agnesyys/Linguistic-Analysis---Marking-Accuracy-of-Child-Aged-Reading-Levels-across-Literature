""""Main file for runner functions and user input"""
import pygame
import sys
import pygame_gui
import plotly.graph_objects as go

import data_processing
from data_processing import TextBlock, Sentence

import complexity_measures

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


def show_text(text_to_show):
    """after input sentence"""
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

        dc = complexity_measures.dale_chall_complexity(new_textblock)
        fc = complexity_measures.flesch_complexity_score()
        cm = get_closest_carec_score(text, )
        sd = complexity_measures.mean_dependency_distance_sentence()

        draw_text('Sentence Complextity Score-', pygame.font.SysFont('Arial', 40), 'black', 50, 30)
        draw_text('Dale-Chall:' + str(dc), text_font, 'black', 50, 100)
        draw_text('Flesch:' + str(fc), text_font, 'black', 50, 150)
        draw_text('CAREC_M:' + str(cm), text_font, 'black', 50, 200)
        draw_text('Mean Dependency Distance:' + str(sd), text_font, 'black', 50, 250)
        # run plotly
        display_reading_level_accuracy(new_textblock, dc, fc, sd)
        pygame.display.update()


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


def display_reading_level_accuracy(textblock: TextBlock, dc: float, fc: float, sd: float) -> None:
    """Display a bar graph of the reading level accuracy of a given sentence."""
    if len(textblock.excerpt) == 1:
        cm = get_closest_carec_score(textblock, csv_file)
    else:
        cm = textblock.carec_m
    fig = go.Figure(
        data=[go.Bar(y=[dc, fc, sd, cm], x=['Dale-Chall Complexity', 'Flesch Complexity',
                                            'Mean Dependency Distance', 'CAREC_M'])],
        layout_title_text="Reading Levels Accuracy Compared to CAREC M of '" + textblock.title + "'"
    )
    fig.show()


def get_closest_carec_score(text: TextBlock, csv_file: str) -> float:
    """get a CAREC_M score by comparing Dale_Chall and Flesch complexitity scores from csv_file"""
    closest_txt_blk = text
    dc = complexity_measures.dale_chall_complexity(text)
    fc = complexity_measures.flesch_complexity_score(text)

    pos_similar_txt_blk = data_processing.read_csv(csv_file)
    min_diff = 10000
    for textblock in pos_similar_txt_blk:
        diff_dc = dc - textblock.dale_chall
        diff_fc = fc - textblock.flesch_reading
        diff = diff_dc + diff_fc

        if diff <= min_diff:
            closest_txt_blk = textblock

    return closest_txt_blk.carec_m
