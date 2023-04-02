""""Main file for runner functions and user input"""
import pygame
import sys
import pygame_gui
import plotly.graph_objects as go
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
        dc = 'Dale-Chall:'
        fl = 'Flesch:'
        cm = 'CAREC_M:'
        mdd = 'Mean Dependency Distance:'
        draw_text('Sentence Complextity Score-', pygame.font.SysFont('Arial', 40), 'black', 50, 30)
        draw_text(dc, text_font, 'black', 50, 100)
        draw_text(fl, text_font, 'black', 50, 150)
        draw_text(cm, text_font, 'black', 50, 200)
        draw_text(mdd, text_font, 'black', 50, 250)
        # run plotly
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

    fig = go.Figure(
        data=[go.Bar(y=[dc, fc, sd, textblock.carec_m], x=['Dale-Chall Complexity', 'Flesch Complexity',
                                                           'Syntatic Difficulty', 'CAREC_M'])],
        layout_title_text="Reading Levels Accuracy Compared to CAREC M of '" + textblock.title + "'"
    )
    fig.show()
