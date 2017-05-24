# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: While searching for the solution to a problem, in this case Sudoku, efficiency of solving  
the problem increases if the solution process is made aware of certain constraints that it is  
not supposed to violate. The constraints get propagated and limit the explosion of number of  
iterations before a solution is reached. In the case of Sudoku solving, one such strategy is  
naked twins. Within the same unit (a row, a column or a square) of a Sudoku if there exist two  
boxes with 2 possible digits each, such that the 2 digits in box-1 are same as the 2 digits in       box-2, we can readily deduce that no other box in the same unit should have these 2 digits as their     possible  solution (the constraint). Making the search algorithm aware of this deduction at every     iteration will propagate the constraint and reduce the computational complexity of the algorithm.     Implementation of naked twins strategy involves first catching hold of the 2 boxes     
with identical values inside every unit. Once the boxes (twin boxes) are identified, use the     
value in any(identical) of the boxes and see if any other box (except for the twin boxes themselves)   
in the same unit has that as a possible value. If yes, remove the identical value from the box.
  
# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: Adding diagonal units as a constraint is a way of restricting any number between 1 and 9 to  
appear more than once on the two possible diagonals. Implementation is fairly simple. First  
the two diagonals are stored in dictionary form and added to the grand list of all other  
units already containing row units, column units and square units.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Submission
Before submitting your solution to a reviewer, you are required to submit your project to Udacity's Project Assistant, which will provide some initial feedback.  

The setup is simple.  If you have not installed the client tool already, then you may do so with the command `pip install udacity-pa`.  

To submit your code to the project assistant, run `udacity submit` from within the top-level directory of this project.  You will be prompted for a username and password.  If you login using google or facebook, visit [this link](https://project-assistant.udacity.com/auth_tokens/jwt_login for alternate login instructions.

This process will create a zipfile in your top-level directory named sudoku-<id>.zip.  This is the file that you should submit to the Udacity reviews system.

