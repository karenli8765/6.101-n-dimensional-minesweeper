"""
6.1010 Spring '23 Lab 7: Mines
"""

#!/usr/bin/env python3

import typing
import doctest

# NO ADDITIONAL IMPORTS ALLOWED!


def dump(game):
    """
    Prints a human-readable version of a game (provided as a dictionary)
    """
    for key, val in sorted(game.items()):
        if isinstance(val, list) and val and isinstance(val[0], list):
            print(f"{key}:")
            for inner in val:
                print(f"    {inner}")
        else:
            print(f"{key}:", val)


# 2-D IMPLEMENTATION


def mine_neighbors_2d(row, col, bombs):
    """
    Given a row and column or a coordinate, this function returns the number of bombs in the neighboring spots of this coordinate.
    """
    neighbor_vectors_2d = [
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1),
        (1, 1),
        (-1, -1),
        (1, -1),
        (-1, 1),
    ]
    count = 0
    for neighbor in neighbor_vectors_2d:
        if (row + neighbor[0], col + neighbor[1]) in bombs:
            count += 1
    return count


def new_game_2d(num_rows, num_cols, bombs):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'hidden' fields adequately initialized.

    Parameters:
       num_rows (int): Number of rows
       num_cols (int): Number of columns
       bombs (list): List of bombs, given in (row, column) pairs, which are
                     tuples

    Returns:
       A game state dictionary

    >>> dump(new_game_2d(2, 4, [(0, 0), (1, 0), (1, 1)]))
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: (2, 4)
    hidden:
        [True, True, True, True]
        [True, True, True, True]
    state: ongoing
    """
    return new_game_nd((num_rows, num_cols), bombs)
    # board = []
    # hidden = []
    # for r in range(num_rows):
    #     b_row = []
    #     h_row = []
    #     for c  in range(num_cols):
    #         h_row.append(True)
    #         if (r, c) in bombs:
    #             b_row.append(".")
    #             continue
    #         b_row.append(mine_neighbors_2d(r, c, bombs))
    #     board.append(b_row)
    #     hidden.append(h_row)
    # return {'dimensions': (num_rows, num_cols), 'board': board, 'hidden': hidden, 'state': 'ongoing'}


def dig_2d(game, row, col):
    """
    Reveal the cell at (row, col), and, in some cases, recursively reveal its
    neighboring squares.

    Update game['hidden'] to reveal (row, col).  Then, if (row, col) has no
    adjacent bombs (including diagonally), then recursively reveal (dig up) its
    eight neighbors.  Return an integer indicating how many new squares were
    revealed in total, including neighbors, and neighbors of neighbors, and so
    on.

    The state of the game should be changed to 'defeat' when at least one bomb
    is revealed on the board after digging (i.e. game['hidden'][bomb_location]
    == False), 'victory' when all safe squares (squares that do not contain a
    bomb) and no bombs are revealed, and 'ongoing' otherwise.

    Parameters:
       game (dict): Game state
       row (int): Where to start digging (row)
       col (int): Where to start digging (col)

    Returns:
       int: the number of new squares revealed

    >>> game = {'dimensions': (2, 4),
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'hidden': [[True, False, True, True],
    ...                  [True, True, True, True]],
    ...         'state': 'ongoing'}
    >>> dig_2d(game, 0, 3)
    4
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: (2, 4)
    hidden:
        [True, False, False, False]
        [True, True, False, False]
    state: victory

    >>> game = {'dimensions': [2, 4],
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'hidden': [[True, False, True, True],
    ...                  [True, True, True, True]],
    ...         'state': 'ongoing'}
    >>> dig_2d(game, 0, 0)
    1
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: [2, 4]
    hidden:
        [False, False, True, True]
        [True, True, True, True]
    state: defeat
    """
    return dig_nd(game, (row, col))
    # if game['hidden'][row][col] == False or game['state'] == 'defeat' or game['state'] == 'victory':
    #     return 0
    # if game['board'][row][col] == ".":
    #     game['hidden'][row][col] = False
    #     game['state'] = 'defeat'
    #     return 1
    # if game['board'][row][col] != 0:
    #     game['hidden'][row][col] = False
    #     game['state'] = get_game_state(game)
    #     return 1

    # game['hidden'][row][col] = False
    # count = 1
    # neighbors = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    # for neighbor in neighbors:
    #     n_row = row + neighbor[0]
    #     n_col = col + neighbor[1]
    #     if 0 <= n_row < game['dimensions'][0] and 0 <= n_col < game['dimensions'][1]:
    #         if game['hidden'][n_row][n_col] == True:
    #             count += dig_2d(game, n_row, n_col)

    # game['state'] = get_game_state(game)

    # return count


def render_2d_locations(game, xray=False):
    """
    Prepare a game for display.

    Returns a two-dimensional array (list of lists) of '_' (hidden squares),
    '.' (bombs), ' ' (empty squares), or '1', '2', etc. (squares neighboring
    bombs).  game['hidden'] indicates which squares should be hidden.  If
    xray is True (the default is False), game['hidden'] is ignored and all
    cells are shown.

    Parameters:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the that are not
                    game['hidden']

    Returns:
       A 2D array (list of lists)

    >>> render_2d_locations({'dimensions': (2, 4),
    ...         'state': 'ongoing',
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'hidden':  [[True, False, False, True],
    ...                   [True, True, False, True]]}, False)
    [['_', '3', '1', '_'], ['_', '_', '1', '_']]

    >>> render_2d_locations({'dimensions': (2, 4),
    ...         'state': 'ongoing',
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'hidden':  [[True, False, True, False],
    ...                   [True, True, True, False]]}, True)
    [['.', '3', '1', ' '], ['.', '.', '1', ' ']]
    """
    return render_nd(game, xray)
    # dimensions = game['dimensions']
    # result = []

    # for row in range(dimensions[0]):
    #     new_row = []
    #     for col in range(dimensions[1]):
    #         if game['hidden'][row][col] == True and xray == False:
    #             new_row.append("_")
    #         else:
    #             if game['board'][row][col] == 0:
    #                 new_row.append(" ")
    #             else:
    #                 new_row.append(str(game['board'][row][col]))
    #     result.append(new_row)
    # return result


def render_2d_board(game, xray=False):
    """
    Render a game as ASCII art.

    Returns a string-based representation of argument 'game'.  Each tile of the
    game board should be rendered as in the function
        render_2d_locations(game)

    Parameters:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game['hidden']

    Returns:
       A string-based representation of game

    >>> render_2d_board({'dimensions': (2, 4),
    ...                  'state': 'ongoing',
    ...                  'board': [['.', 3, 1, 0],
    ...                            ['.', '.', 1, 0]],
    ...                  'hidden':  [[False, False, False, True],
    ...                            [True, True, False, True]]})
    '.31_\\n__1_'
    """
    dimensions = game["dimensions"]
    result = ""
    list_form = render_2d_locations(game, xray)

    for row in range(dimensions[0]):
        for col in range(dimensions[1]):
            result += list_form[row][col]
        result += (
            "\n"  # search how to make \\n appear as is in string and not as function
        )

    return result[:-1]


# N-D IMPLEMENTATION


def get_value(array, coordinates):
    """
    Returns the value at the given coordinates in the array.
    """
    value = array
    for index in coordinates:
        value = value[index]
    return value


def set_value(array, coordinates, value):
    """
    Replaces the value at the given coordinates in the array with the given value.
    """
    arr = array
    for index in coordinates[:-1]:
        arr = arr[index]
    arr[coordinates[-1]] = value


def create_nd_array(dimensions, value):
    """
    Creates a new N-dimensional list with the given dimensions and value.
    """
    if not dimensions:
        return []
    elif len(dimensions) == 1:
        return [value] * dimensions[0]
    else:
        return [create_nd_array(dimensions[1:], value) for _ in range(dimensions[0])]


def get_game_state(game):
    """
    Recursively loops through all coordinates of an N-dimensional array and applies the given function to each one.
    """
    coordinates = all_coordinates(game["dimensions"])
    for coordinate in coordinates:
        value = get_value(game["board"], coordinate)
        hide_value = get_value(game["hidden"], coordinate)
        if value != "." and hide_value == True:
            return "ongoing"
    return "victory"


def all_neighbors(coordinates, dimensions):
    """
    find all neighbors
    """
    # if len(coordinates) == 0:
    #     return []
    if len(coordinates) == 1:
        neighbors = []
        if 0 <= coordinates[0] - 1 < dimensions[0]:
            neighbors.append((coordinates[0] - 1,))
        if 0 <= coordinates[0] < dimensions[0]:
            neighbors.append((coordinates[0],))
        if 0 <= coordinates[0] + 1 < dimensions[0]:
            neighbors.append((coordinates[0] + 1,))
        return neighbors
    else:
        neighbors = []
        first_neighbors = all_neighbors((coordinates[0],), (dimensions[0],))
        following_neighbors = all_neighbors(coordinates[1:], dimensions[1:])
        for first_neighbor in first_neighbors:
            for following_neighbor in following_neighbors:
                neighbors.append(first_neighbor + following_neighbor)
        return neighbors


def all_coordinates(dimensions: tuple):
    """
    find all coordinates
    """
    # if len(dimensions) == 0:
    #     return []
    if len(dimensions) == 1:
        result = []
        for i in range(dimensions[0]):
            result.append((i,))
        return result
    else:
        result = []
        first_coordinates = all_coordinates((dimensions[0],))
        last_coordinates = all_coordinates(dimensions[1:])
        for first_coordinate in first_coordinates:
            for last_coordinate in last_coordinates:
                result.append(first_coordinate + last_coordinate)
        return result


def new_game_nd(dimensions, bombs):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'hidden' fields adequately initialized.


    Args:
       dimensions (tuple): Dimensions of the board
       bombs (list): Bomb locations as a list of tuples, each an
                     N-dimensional coordinate

    Returns:
       A game state dictionary

    >>> g = new_game_nd((2, 4, 2), [(0, 0, 1), (1, 0, 0), (1, 1, 1)])
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    hidden:
        [[True, True], [True, True], [True, True], [True, True]]
        [[True, True], [True, True], [True, True], [True, True]]
    state: ongoing
    """
    board = create_nd_array(dimensions, 0)
    hidden = create_nd_array(dimensions, True)

    bomb_dict = {}
    for bomb in bombs:
        bomb_neighbors = all_neighbors(bomb, dimensions)
        for neighbor in bomb_neighbors:
            if neighbor in bomb_dict:
                bomb_dict[neighbor] += 1
            else:
                bomb_dict[neighbor] = 1

    for coord in bomb_dict:
        set_value(board, coord, bomb_dict[coord])

    for bomb in bombs:
        set_value(board, bomb, ".")

    return {
        "board": board,
        "dimensions": dimensions,
        "hidden": hidden,
        "state": "ongoing",
    }


def dig_nd(game, coordinates, done=False):
    """
    Recursively dig up square at coords and neighboring squares.

    Update the hidden to reveal square at coords; then recursively reveal its
    neighbors, as long as coords does not contain and is not adjacent to a
    bomb.  Return a number indicating how many squares were revealed.  No
    action should be taken and 0 returned if the incoming state of the game
    is not 'ongoing'.

    The updated state is 'defeat' when at least one bomb is revealed on the
    board after digging, 'victory' when all safe squares (squares that do
    not contain a bomb) and no bombs are revealed, and 'ongoing' otherwise.

    Args:
       coordinates (tuple): Where to start digging

    Returns:
       int: number of squares revealed

    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'hidden': [[[True, True], [True, False], [True, True],
    ...                [True, True]],
    ...               [[True, True], [True, True], [True, True],
    ...                [True, True]]],
    ...      'state': 'ongoing'}
    >>> dig_nd(g, (0, 3, 0))
    8
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    hidden:
        [[True, True], [True, False], [False, False], [False, False]]
        [[True, True], [True, True], [False, False], [False, False]]
    state: ongoing
    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'hidden': [[[True, True], [True, False], [True, True],
    ...                [True, True]],
    ...               [[True, True], [True, True], [True, True],
    ...                [True, True]]],
    ...      'state': 'ongoing'}
    >>> dig_nd(g, (0, 0, 1))
    1
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    hidden: 
        [[True, False], [True, False], [True, True], [True, True]]
        [[True, True], [True, True], [True, True], [True, True]]
    state: defeat   
    """
    if (
        get_value(game["hidden"], coordinates) == False
        or game["state"] == "defeat"
        or game["state"] == "victory"
    ):
        return 0

    if get_value(game["board"], coordinates) == ".":
        set_value(game["hidden"], coordinates, False)
        game["state"] = "defeat"
        return 1

    if get_value(game["board"], coordinates) != 0:
        set_value(game["hidden"], coordinates, False)
        if done == False:
            game["state"] = get_game_state(game)
        return 1

    set_value(game["hidden"], coordinates, False)
    count = 1
    neighbors = all_neighbors(coordinates, game["dimensions"])
    for neighbor in neighbors:
        count += dig_nd(game, neighbor, True)

    if done == False:
        game["state"] = get_game_state(game)
    return count


def render_nd(game, xray=False):
    """
    Prepare the game for display.

    Returns an N-dimensional array (nested lists) of '_' (hidden squares), '.'
    (bombs), ' ' (empty squares), or '1', '2', etc. (squares neighboring
    bombs).  The game['hidden'] array indicates which squares should be
    hidden.  If xray is True (the default is False), the game['hidden'] array
    is ignored and all cells are shown.

    Args:
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game['hidden']

    Returns:
       An n-dimensional array of strings (nested lists)

    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'hidden': [[[True, True], [True, False], [False, False],
    ...                [False, False]],
    ...               [[True, True], [True, True], [False, False],
    ...                [False, False]]],
    ...      'state': 'ongoing'}
    >>> render_nd(g, False)
    [[['_', '_'], ['_', '3'], ['1', '1'], [' ', ' ']],
     [['_', '_'], ['_', '_'], ['1', '1'], [' ', ' ']]]

    >>> render_nd(g, True)
    [[['3', '.'], ['3', '3'], ['1', '1'], [' ', ' ']],
     [['.', '3'], ['3', '.'], ['1', '1'], [' ', ' ']]]
    """
    result = create_nd_array(game["dimensions"], None)
    all_coords = all_coordinates(game["dimensions"])
    for coord in all_coords:
        value = get_value(game["board"], coord)
        hide = get_value(game["hidden"], coord)
        if xray == True:
            hide = False
        if hide == True:
            set_value(result, coord, "_")
        else:
            if value == 0:
                set_value(result, coord, " ")
            else:
                set_value(result, coord, str(value))
    return result


if __name__ == "__main__":
    # Test with doctests. Helpful to debug individual lab.py functions.
    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    doctest.testmod(optionflags=_doctest_flags)  # runs ALL doctests

    doctest.run_docstring_examples(
        render_2d_locations, globals(), optionflags=_doctest_flags, verbose=False
    )

    # Define a game dictionary for testing purposes
    # game = {'dimensions': (2, 4),
    #          'board': [['.', 3, 1, 0],
    #                    ['.', '.', 1, 0]],
    #          'hidden': [[True, False, True, True],
    #                   [True, True, True, True]],
    #          'state': 'ongoing'}
    # print(new_game_nd((2, 4, 2), []))
    # g = {
    #     "dimensions": (2, 4, 2),
    #     "board": [
    #         [[3, "."], [3, 3], [1, 1], [0, 0]],
    #         [[".", 3], [3, "."], [1, 1], [0, 0]],
    #     ],
    #     "hidden": [
    #         [[True, True], [True, False], [True, True], [True, True]],
    #         [[True, True], [True, True], [True, True], [True, True]],
    #     ],
    #     "state": "ongoing",
    # }
    # render_nd(g, False)

    n = 3
    class Foo:
        n = 0
    
    class Bar(Foo):
        n = 2
        def __init__(self) -> None:
            self.n = n

    class Baz(Bar):
        n = 5

    baz = Baz()
    print(baz.n)
