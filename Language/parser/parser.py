import nltk
import sys
TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself" | "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she" | "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat" | "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | S Conj S | S Conj VP | S Conj NP VP | S Conj NP VP PP

NP -> N | Det N | Det AP N | Det N PP | N PP | NP Conj NP
VP -> V | V NP | V NP PP | V
PP -> P NP
AP -> Adj | Adj AP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)
    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()
        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    # Use RegexpTokenizer to tokenize the sentence
    tokenizer = nltk.RegexpTokenizer(r"[A-Za-z]+")
    return tokenizer.tokenize(sentence.lower())


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    chunks = []

    # Iterate through all subtrees in the tree:
    for subtree in tree.subtrees():
        # If subtree is labelled as a Noun Pharse
        if subtree.label() == "NP":
            # We exclude the tree itself or it will always return false
            if not any(subsubtree.label() == "NP" for subsubtree in subtree.subtrees(lambda t: t != subtree)):
                chunks.append(subtree)
    return chunks


if __name__ == "__main__":
    main()
