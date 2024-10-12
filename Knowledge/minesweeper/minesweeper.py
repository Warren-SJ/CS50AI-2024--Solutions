import itertools
import random


class Minesweeper:
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):
        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence:
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # When a sentence is given, the only way to properly know if a cell is a mine is if the count of the sentence is equal to the number of cells in the sentence
        if len(self.cells) == self.count and self.count != 0:
            return self.cells
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # When a sentence is given, the only way to properly know if a cell is safe is if the count of the sentence is equal to 0
        if self.count == 0:
            return self.cells
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # First check if the cell specified is in the sentence. If so, remove it from the sentence and decrement the count by 1
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # First check if the cell specified is in the sentence. If so, remove it from the sentence. In the case of a safe cell, there is no need to update the count   
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI:
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):
        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        self.moves_made.add(cell)
        self.mark_safe(cell)
        neighbours = set()
        # Loop through all cells in the 3x3 grid around the cell given
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                # Check if the cell is in bounds and not the cell given
                if (
                    (i, j) != cell 
                    and i >= 0 
                    and i < self.height 
                    and j >= 0 
                    and j < self.width
                ):
                    # If the cell is a mine, we can ignore it from the sentence
                    if (i, j) in self.mines:
                        count -= 1
                    else:
                        # If the cell is not in safes, we can add it to the sentence
                        if not (i, j) in self.safes:
                            neighbours.add((i, j))
        # Create a new sentence with the neighbours set and the count given
        if len(neighbours) > 0:
            new_sentence = Sentence(neighbours, count)
            # Add the new sentence to the knowledge base
            self.knowledge.append(new_sentence)

        # Loop through all sentences in the knowledge base and infer new mines and new safes
        for sentence in self.knowledge:
            if sentence.known_mines():
                # copy() is needed as the known_mines() and known_safes() functions remove cells from the sentence
                for cell in sentence.known_mines().copy():
                    self.mark_mine(cell)
            if sentence.known_safes():
                for cell in sentence.known_safes().copy():
                    self.mark_safe(cell)

        # Loop through all combinations of sentences in the knowledge base and infer new sentences
        for sentence1, sentence2 in itertools.combinations(self.knowledge, 2):
            if sentence1.cells.issubset(sentence2.cells):
                new_cells = sentence2.cells - sentence1.cells
                new_count = sentence2.count - sentence1.count
                new_sentence = Sentence(new_cells, new_count)
                if new_sentence not in self.knowledge:
                    self.knowledge.append(new_sentence)
            elif sentence2.cells.issubset(sentence1.cells):
                new_cells = sentence1.cells - sentence2.cells
                new_count = sentence1.count - sentence2.count
                new_sentence = Sentence(new_cells, new_count)
                if new_sentence not in self.knowledge:
                    self.knowledge.append(new_sentence)
            if new_sentence.known_mines():
                # copy() is needed as the known_mines() and known_safes() functions remove cells from the sentence
                for cell in new_sentence.known_mines().copy():
                    self.mark_mine(cell)
            if new_sentence.known_safes():
                for cell in new_sentence.known_safes().copy():
                    self.mark_safe(cell)

        # Loop through all sentences in the knowledge base and remove empty sentences
        for sentence in self.knowledge.copy():
            if len(sentence.cells) == 0:
                self.knowledge.remove(sentence)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for cell in self.safes:
            if not cell in self.moves_made:
                return cell
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        possible_moves = []
        # Go through entire board and see if the cell is in the moves made or mines list. If not, add it to the list of possible moves
        for i in range(self.height):
            for j in range(self.width):
                if not (i, j) in self.moves_made and not (i, j) in self.mines:
                    possible_moves.append((i, j))
        # Try and except block to return a random move from the list of possible moves. If there are no possible moves, random.choice will throw an error, so return None
        try:
            return random.choice(possible_moves)
        except:
            return None
