""" 
This is the tests for game_engine
"""

__author__ = 'Mark Galpin'
__version__ = '0.1'

import pytest
import game_engine

NUM_ROWS = 6
NUM_COLS = 6
NUM_MINES = 3

@pytest.fixture()
def testengine() -> game_engine.Engine:
    return game_engine.Engine(NUM_ROWS, NUM_COLS, NUM_MINES)


@pytest.mark.xfail
def test_show_board(testengine):
    """This test fails just so it can print the game board to the log"""
    myengine=testengine
    myengine.ascii_game_board=myengine.grid._serialize_reveal_all()
    assert False, "\n"+str(myengine)

def test_flag(testengine):
    """Flag and unflag the board"""
    myengine=testengine
    myengine.flag_cell(2,2)
    assert myengine.grid[2][2].is_flagged
    assert myengine.mines_remaining() == (NUM_MINES-1)
    myengine.flag_cell(2,2, False)
    assert not myengine.grid[2][2].is_flagged
    assert myengine.mines_remaining() == NUM_MINES

def test_losing(testengine):
    """Attempts to lose the game by just flagging cells until the mines remaining is 0.
    NOTE: In theory we should compare the board in case the degenerate state occurs"""
    myengine=testengine
    count = 0
    for row in myengine.grid:
        for cell in row:
            count+=1
            assert count<=NUM_MINES
            myengine.flag_cell(cell.row_index, cell.col_index)
            if count==NUM_MINES:
                assert myengine.mines_remaining() == 0
                assert myengine.game_is_over
                if myengine.game_is_won:
                    assert compare_boards()
                return

def test_winning(testengine):
    """Cheats to win so it flags all the mines"""
    myengine=testengine
    count = 0
    for row in myengine.grid:
        for cell in row:
            if cell._is_mined: #pylint: disable=protected-access
                count+=1
                assert count <= NUM_MINES
                myengine.flag_cell(cell.row_index, cell.col_index)
    assert count == myengine.grid.num_mines
    assert myengine.mines_remaining() == 0
    assert myengine.game_is_over
    assert myengine.game_is_won

def compare_boards() -> bool:
    """This should compare the "play board" and the "reveal all" board and 
    get the same result -- happens when the game is won
    NOTE: if I had CI this would be unacceptable, but since I am doing it by hand, not a problem"""
    raise NotImplementedError("Degenerate state may have occurred, \
                              board comparison is necessary for test. \
                              Try re-running test!")
