""" 
This is the tests for game_engine
"""

__author__ = 'Mark Galpin'
__version__ = '0.1'

import game_engine
#import pytest

NUM_ROWS = 6
NUM_COLS = 6
NUM_MINES = 20

myengine = game_engine.Engine(NUM_ROWS, NUM_COLS, NUM_MINES)

def test_flag():
    """tests flagging"""
    myengine.flag_cell(2,2)
    assert myengine.grid[2][2].is_flagged
    assert myengine.mines_remaining() == (NUM_MINES-1)
    myengine.flag_cell(2,2, False)
    assert not myengine.grid[2][2].is_flagged
    assert myengine.mines_remaining() == NUM_MINES

def test_losing():
    """Attempts to lose the game by just flagging cells until the mines remaining is 0.
    NOTE: In theory we should compare the board in case the degenerate state occurs"""
    count = 0
    for row_index, row in enumerate(myengine.grid):
        for col_index, cell in enumerate(row): #pylint: disable=unused-variable
            count+=1
            myengine.flag_cell(row_index, col_index)
            if count==NUM_MINES:
                assert myengine.mines_remaining() == 0
                assert myengine.game_is_over
                if myengine.game_is_won:
                    assert compare_boards()

def compare_boards() -> bool:
    """This should compare the "play board" and the "reveal all" board and 
    get the same result -- happens when the game is won
    NOTE: if I had CI this would be unacceptable, but since I am doing it by hand, not a problem"""
    raise NotImplementedError("Degenerate state may have occurred, \
                              board comparison is necessary for test. \
                              Try re-running test!")
