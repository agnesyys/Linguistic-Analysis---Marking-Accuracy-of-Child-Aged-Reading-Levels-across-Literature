"""Storage for Mikayla in case of Git Shenanigans"""
import plotly.graph_objects as go
from courseProject.data_processing import TextBlock
from courseProject import complexity_measures as complex
# import pygame
# pygame.init()
#
# size = width, height = 320, 240
#
# screen = pygame.display.set_mode(size)
#
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False


def display_reading_levels(book: TextBlock) -> None:
    """Display a bar graph of the reading levels of a given novel."""
    dc = complex.dale_chall_complexity(book)
    fc = complex.flesch_complexity_score(book)
    fig = go.Figure(
        data=[go.Bar(y=[dc, fc, book.carec_m], x=['Dale-Chall Complexity', 'Flesch Complexity', 'CAREC'])],
        layout_title_text="Reading Levels Computed by Different Algorithms"
    )
    fig.show()
