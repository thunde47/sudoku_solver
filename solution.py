import logging
from utils import *

logging.basicConfig(filename='debug_log.txt',level=logging.DEBUG)
logger=logging.getLogger(__name__)
assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """    
    for unit in unitlist:
    # Find all instances of naked twins in a unit
        naked_twins=[] #contains boxes with naked twin values
        twin_value='' #contains the actual twin value
        for boxi in unit: #loop over the boxes in a unit
            if len(values[boxi]) == 2: #only boxes with 2 digit long values considered
                for boxj in unit: #loop over the boxes in a unit to compare with the boxi
                    #compare a box in a unit with another box in the same unit
                    #string values converted to sets because order of string characters (digits)
                    #does not matter
                    if set(list(values[boxi])) == set(list(values[boxj])) and (boxi != boxj):
                        naked_twins.append(boxi)
                        twin_value=values[boxi] 
        
        if len(naked_twins)==0: #continue back to loop if no naked twin found in the unit
            continue
        logger.debug("naked twins: %s", naked_twins)
        logger.debug("sudoku after naked twin strategy: %s", values)
        # Eliminate the naked twins, if found, as possibilities in the unit                         
        for box in unit:
            if box not in naked_twins: #avoid removing a twin digit in the naked twin box itself   
                for digit in values[box]:
                    if digit in twin_value:
                        #remove naked twin value from non-naked twin boxes
                        assign_value(values,box,values[box].replace(digit,''))
        
        
    return values     

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    
    grid_dict=dict()
    all_digits='123456789'
    for location, value in zip(boxes,grid):
        if value=='.':
            grid_dict[location]=all_digits
        else:
            grid_dict[location]=value
    return grid_dict 

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    """Eliminate values using the elimination strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with eliminated values.
    """
    for box in values:
        if len(values[box])==1:
            for peer in peers[box]: 
                #if a box has a value assigned, then none of the peers of this box can have this value
                assign_value(values,peer,values[peer].replace(values[box],''))
               
    return values 

def only_choice(values):
    """Eliminate values using the only choice strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the only possible choices
    """
    for unit in unitlist:
        for digit in '123456789':
            counter=[]
            for box in unit:
                if digit in values[box]:
                    counter.append(box)
            if len(counter)==1:
                #if there is only one box in a unit which would allow a certain digit,
                # then the box must be assigned that digit
                assign_value(values, counter[0],digit)
    return values 

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        
        
        # Use the Eliminate Strategy
        values=eliminate(values)
        
        # Use the Only Choice Strategy
        values=only_choice(values)
        
        # Use the Naked Twins Strategy
        values=naked_twins(values)
        
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    values=reduce_puzzle(values)
    
    if values is False:
        return False
    # Choose one of the unfilled squares with the fewest possibilities    
    min_possibilities=10
    optimum_box='A1'
    for box in values.keys():
        if len(values[box])>1 and len(values[box])<=min_possibilities:
            optimum_box=box
            min_possibilities=len(values[box])
    
    # Use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!

    solved_values=0
    for box in values.keys():
        solved_values+=len(values[box])
    if solved_values==81: #each box has 1 digit, indicating puzzle solved
        return values
    # DFS using recursion
    for digit in values[optimum_box]:
        child_sudoku=values.copy() #to avoid overrides. deepcopy() not valid for dictionaries
        child_sudoku[optimum_box]=digit
        solution = search(child_sudoku)
        if solution:
            return solution

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    
    values=grid_values(grid)
    return search(values)

if __name__ == '__main__':

    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    
    solution=solve(diag_sudoku_grid)
    if not solution:
        logger.error("Sudoku could not be solved")
    display(solution) 
    """   
    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
        """
