import sys

from crossword import *


class CrosswordCreator:
    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy() for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont

        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size, self.crossword.height * cell_size),
            "black",
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                rect = [
                    (j * cell_size + cell_border, i * cell_size + cell_border),
                    (
                        (j + 1) * cell_size - cell_border,
                        (i + 1) * cell_size - cell_border,
                    ),
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (
                                rect[0][0] + ((interior_size - w) / 2),
                                rect[0][1] + ((interior_size - h) / 2) - 10,
                            ),
                            letters[i][j], 
                            fill="black", 
                            font=font,
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # Unary constraint in this case is the length of the word
        for var in self.crossword.variables:
            for word in self.domains[var].copy():
                if len(word) != var.length:
                    self.domains[var].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # domains has the set of possible words for each variable
        # a variable is a blank space in a crossword
        # x and y are variables and to be arc consistent, wherever x and y overlap, the letters must be the same
        # crossword overlaps have 2 variables as a key and a tuple of the indices of the overlap as the value
        removed = False
        # if there is no overlap, then there is no need to revise
        if self.crossword.overlaps[x, y] is None:
            return False
        for word in self.domains[x].copy():
            if not any(
                word[self.crossword.overlaps[x, y][0]]
                == y_word[self.crossword.overlaps[x, y][1]]
                for y_word in self.domains[y]
            ):
                self.domains[x].remove(word)
                removed = True
        return removed

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if ( 
            arcs is None
        ):  # if arcs is None, begin with initial list of all arcs in the problem
            while True:
                revised = False
                for x in self.crossword.variables:
                    for y in self.crossword.variables:
                        if x != y:
                            if self.revise(x, y):
                                revised = True
                if not revised:
                    break
        else:
            for arc in arcs:
                self.revise(arc[0], arc[1])
        return not any(len(self.domains[var]) == 0 for var in self.crossword.variables)

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for var in self.crossword.variables:
            # Check if all variables are in assignment
            if var not in assignment.keys():
                return False
            # Check if all variables have a value
            elif not (assignment[var]):
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        words = set()
        for var, value in assignment.items():
            # Check if all values are distinct
            if value in words:
                return False
            words.add(value)

            # Check unary constraints
            if len(value) != var.length:
                return False

            # Check binary constraints
            for neighbor in self.crossword.neighbors(var):
                overlaps = self.crossword.overlaps[var, neighbor]
                # Check if neighbor is in assignment, here we don't need to check if the assignment is complete
                if neighbor in assignment.keys():
                    if value[overlaps[0]] != assignment[neighbor][overlaps[1]]:
                        return False
        return True
    
    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        removed_values = dict()
        neighbors = self.crossword.neighbors(var)
        for value in self.domains[var]:
            removed_values[value] = 0
            for neighbor in neighbors:
                overlaps = self.crossword.overlaps[var, neighbor]
                for neighbor_value in self.domains[neighbor]:
                    if value[overlaps[0]] != neighbor_value[overlaps[1]]:
                        removed_values[value] += 1
        return sorted(removed_values, key=removed_values.get)
            
    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        possiblevariables = dict()
        for variable in self.crossword.variables:
            if variable not in assignment.keys():
                possiblevariables[variable] = len(self.domains[variable])
        # count number of times the max value appears
        min_value = min(possiblevariables.values())
        for key in possiblevariables.copy():
            if possiblevariables[key] != min_value:
                possiblevariables.pop(key)
        # if there is only one max value, return the only remaining variable
        if len(possiblevariables) == 1:
            return next(iter(possiblevariables))
        # if there are multiple max values, return the variable with the highest degree
        max_degree = 0
        for variable in possiblevariables.keys():
            if len(self.crossword.neighbors(variable)) > max_degree:
                max_degree = len(self.crossword.neighbors(variable))
                max_variable = variable
        return max_variable

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            assignment[var] = value
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result is not None:
                    return result
            assignment.pop(var)
        return None


def main():
    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
