Terminology:
* A "live" square is a revelaed cell that has cells surrounding it which are neither revealed nor flagged.
* A "break" is when you reveal an empty square, so it goes out and reveals more squares.

For generating the grid:
Given an array of RXC, select an element randomly, and if it doesn't already have a mine, insert a mine until the total number of mines is met.

To play:
I conceive of Minesweeper as a set of pairs of inverse rules each growing in sophistication (note that the level 0 rule is deifnitely played last)
* Level 0: This rule governs what to do when you have to make a random selection.
** Terms:
*** Probability that a random cell with no information surrounding it will be a bomb:  P_Rand=Num_Unrevealed / Num_UnflaggedMines  (Note that this changes as the game evolves -- which is something the computer does more easily than a human, but a human COULD do)
*** Effective Count: Effective_Count=Revealed_value - num_surrouding_flagged
** Rule: If any live cell has Num_Surrounding_Unrevealed / Effective_Count < P_Rand, reveal an unrevealed square surrounding it, then start again.
** Inverse Rule: If no such live cell exists, reveal a random cell with no revealed squares around it.  If no such cell exists, then we are in end game rules (see level 4)
** Questions about Level 0 Rule:
*** 1.) First, when I play the "Rule" I tend to move "away" from higher numbers.  That's not included here, how much does it matter?  How would I express that?
*** 2.) Should I add in rules like "move towards the center" or "move towards known space"?
*** 3.) When starting play, should I eliminate edge cells from contention for random picks?  I believe that an edge cell should be more likely to cause a break, but also, if it doesn't, more likely to need to apply the inverse rule.
* Level 1 Rule:  The obvious picks
** Rule: For aa live cell, if the number of surrounding unrevealed squares is equal to the effective count, then flag all unrevealed squares.
** Inverse rule: For a live cell, if the number of flags is equal to the revealed number, then reveal all unrevealedd squares.
* Level 2 rule: Fully scoped sub-sets (This rule's inverse is itself because it includes rule 1)
** Rule: If all unrevealed squares of a neighboring cell are neighbors of the current cell, mark those squares temporarily out of play, and temporarily decremment your effective count by the effective count of the square.  Then run rule 1 on what's left.
** Inverse: Take mark all squares associated with a neiboring cell out of play, and decrement the effective count counter accordingly, then run flagging rule ONLY, if possible.
* Level 3: I'm pretty sure there's a level 3 rule with multiple neighbor scopes.
e.g.:
0 = = =
0 1 2 =
0 0 1 =
0 0 0 0 
you know the top right corner is empty, and I'm pretty sure the level 2 rule doesn't catch that.  This can't be combined with the level 2 rule because in some scenarios, like
0 = = = 0
0 1 2 1 0
0 0 0 0 0
this rule would mark all squares out of scope, and get nowhere, whereas the level 2 rule will correctly flag this.
* Level 4: Does such a rule exist (At least when I play), or is this when to get an AI invvolved?  Or is there nothing better except fine-tuning random?
* End_Game:  As a special rule, when there are no zero information squares left, the count of the mines may provide information.  I'm not quite sure how to express this.  But sometimes you have fewer mines than some configurations for the remaining unrevealed squares allow, and then that has to be taken into consideration, and may avoid random action.  Will think about it when I get there.
* Note: in general you apply rules 1-4 then 0, then end game?

For AI, it would be fun to try to train just to replace a level 4+ rule, or to train from scratch, and see which is better.
Also, wouuld this be good to run on a GPU?  I feel like the answer is probably yes.   Will examine later.