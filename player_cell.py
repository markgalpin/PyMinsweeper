""" 
This will be the utility classes for player cells
"""
__author__ = 'Mark Galpin'
__version__ = '0.1'

from play_grid import VisibleValue

class PlayerCell:
    """This class reflects the player's thoughts on the cell"""
    value: VisibleValue = None
    row_index: int = None
    col_index: int = None
    hypothetical_value: int = None
    is_active: bool = None
    hypothetical_active: bool = None

    def __init__(self, value: VisibleValue, row_index: int, column_index: int):
        self.value = value
        self.row_index = row_index
        self.col_index = column_index
        if(self.value.is_revealed):
            if not self.value.is_flagged:
                assert self.value.value is not None
                self.hypothetical_value=self.value.value
        self.is_cell_active()
    
    def is_cell_active(self) -> bool:
        """This function updates the is_active state of the cell and returns it"""
        if not self.value.is_revealed or self.value.is_flagged:
            self.is_active=False
        else:
            assert self.hypothetical_value is not None
            if self.hypothetical_value > 0:
                self.is_active=True
            else:
                self.is_active=False
        self.hypothetical_active=self.is_active
        return self.is_active