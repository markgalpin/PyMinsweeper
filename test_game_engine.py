""" 
This is the tests for game_engine
"""

__author__ = 'Mark Galpin'
__version__ = '0.1'

import game_engine
#import pytest

myrows = 6
mycols = 6
mymines = 20

myengine = game_engine.Engine(myrows, mycols, mymines)

def test_flag():
    """tests flagging"""
    myengine.flag_cell(2,2)
    assert myengine.grid[2][2].is_flagged
    assert myengine.mines_remaining() == (mymines-1)
    myengine.flag_cell(2,2, False)
    assert not myengine.grid[2][2].is_flagged
    assert myengine.mines_remaining() == mymines

