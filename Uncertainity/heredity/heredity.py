import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])
    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }
    # probabilities is now a dictionary. The dictionary contains the name of each person and the probabilities
    # of finding 0, 1, or 2 genes and the probabilities of finding the trait or not finding the trait.
    # Loop over all sets of people who might have the trait
    names = set(people)
    # names contains the keys of the dictionary people which are the names of the people
    for have_trait in powerset(names):
        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue
        # people is a dictionary contaiining the names of all the people, their mother, father and whether or not the trait is presentin them
        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):
                # Update probabilities with new joint probability
                # Loops and gets probabilities where each person is checked for having 1 or 2 genes.
                # Those not in one_genes or two_genes should be tested for having 0 genes.
                # have_trait is a set of people who we want to calculate have the trait. It starts with an empty set and then adds people to it. 
                # Initially 1 person, then 2 and so on until we have to calculate the probability that all exhibit the trait
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)
    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    # People is a dictionary containing the names of all the people, their mother, father and whether or not the trait is present in them
    # one_gene is a set of people who we want to calculate have 1 gene.
    # two_genes is a set of people who we want to calculate have 2 genes.
    # have_trait is a set of people who we want to calculate have the trait.
    probability = 1
    # passingprobability is the probability that given a person has 0,1 or 2 genes, they will pass 0,1 or 2 genes to their child
    passingprobability = {
        0: {
            0: 1 - PROBS["mutation"],
            1: PROBS["mutation"]
        },
        1: {
            0: 0.5,
            1: 0.5
        },
        2: {
            0: PROBS["mutation"],
            1: 1 - PROBS["mutation"]
        }
    }
    transferprobability = {
        0: {
            0: passingprobability[0][0] * passingprobability[0][0],
            1: passingprobability[0][0] * passingprobability[0][1] * 2,
            2: passingprobability[0][1] * passingprobability[0][1]
        },
        1: {
            0: passingprobability[1][0] * passingprobability[0][0],
            1: passingprobability[1][0] * passingprobability[0][1] + passingprobability[1][1] * passingprobability[0][0],
            2: passingprobability[1][1] * passingprobability[0][1]
        },
        2: {
            0: passingprobability[1][0] * passingprobability[1][0],
            1: passingprobability[1][0] * passingprobability[1][1] * 2,
            2: passingprobability[1][1] * passingprobability[1][1]
        },
        3: {
            0: passingprobability[2][0] * passingprobability[0][0],
            1: passingprobability[2][0] * passingprobability[0][1] + passingprobability[2][1] * passingprobability[0][0],
            2: passingprobability[2][1] * passingprobability[0][1]
        },
        4: {
            0: passingprobability[2][0] * passingprobability[1][0],
            1: passingprobability[2][0] * passingprobability[1][1] + passingprobability[2][1] * passingprobability[1][0],
            2: passingprobability[2][1] * passingprobability[1][1]
        },
        6: {
            0: passingprobability[2][0] * passingprobability[2][0],
            1: passingprobability[2][0] * passingprobability[2][1] * 2,
            2: passingprobability[2][1] * passingprobability[2][1]
        }
    }
    # transferprobability is a dictionary mapping parent score to the probability that the child will have 0, 1 or 2 genes
    # Scores are as follows:
    # 0 -> Both parents don't have the gene
    # 1 -> One parent has one gene
    # 2 -> Both parents have one gene
    # 3 -> One parent has two genes and the other has no genes
    # 4 -> One parent has one gene and the other has two genes
    # 6 -> Both parents have two genes
    for person in people:
        mother, father = people[person]["mother"], people[person]["father"]
        if mother is None and father is None:
            probability *= PROBS["gene"][2 * (person in two_genes) + (person in one_gene)]
        else:
            score = 0
            if mother in two_genes:
                score += 3
            elif mother in one_gene:
                score += 1
            if father in two_genes:
                score += 3
            elif father in one_gene:
                score += 1
            probability *= transferprobability[score][2 * (person in two_genes) + (person in one_gene)]
        # Multiply by probability of showing trait given number of genes
        probability *= PROBS["trait"][2 * (person in two_genes) + (person in one_gene)][person in have_trait]
    return probability 


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        probabilities[person]["gene"][2 * (person in two_genes) + (person in one_gene)] += p
        probabilities[person]["trait"][person in have_trait] += p
    

def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        gene_sum = 0
        # Add up all the probabilities of having a certain number of genes
        gene_sum += probabilities[person]["gene"][0] + probabilities[person]["gene"][1] + probabilities[person]["gene"][2]
        # Divide by the total sum
        probabilities[person]["gene"][0] /= gene_sum
        probabilities[person]["gene"][1] /= gene_sum
        probabilities[person]["gene"][2] /= gene_sum
        trait_sum = 0
        # Add up all the probabilities of having a certain trait
        trait_sum += probabilities[person]["trait"][True] + probabilities[person]["trait"][False]
        # Divide by the total sum
        probabilities[person]["trait"][True] /= trait_sum  
        probabilities[person]["trait"][False] /= trait_sum


if __name__ == "__main__":
    main()
