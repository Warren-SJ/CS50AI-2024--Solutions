import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    # corpus is a dictionary with key as page and value as set of pages linked to it
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(link for link in pages[filename] if link in pages)

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    visitprobability = dict()
    for link in corpus[page]:
        # Try to add the link to the dictionary. If it already exists, add the probability to the existing probability
        try:
            visitprobability[link] = damping_factor / len(corpus[page])
        # There might be a divison by zero error if the page has no links. In that case, add the probability to the existing probability
        except:
            visitprobability[link] = damping_factor / len(corpus)
    for link in corpus:
        if not link in visitprobability:
            visitprobability[link] = (1 - damping_factor) / len(corpus)
        else:
            visitprobability[link] += (1 - damping_factor) / len(corpus)
    return visitprobability


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank = dict()
    # Initially set all to 0
    for page in corpus.keys():
        pagerank[page] = 0
    page = random.choice(list(corpus.keys()))
    for i in range(n):
        visitprobability = transition_model(corpus, page, damping_factor)
        pagerank[page] += 1 / n
        page = random.choices(
            list(visitprobability.keys()), weights=list(visitprobability.values())
        )[0]
    return pagerank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pageranks = dict()
    for page in corpus.keys():
        pageranks[page] = 1 / len(corpus)
    while True:
        temp_pageranks = dict()
        # Iterate over all pages
        for page in corpus.keys():
            # Pick a page at random
            temp_pageranks[page] = (1 - damping_factor) / len(corpus)
            # Iterate over all the pages again
            for link in corpus.keys():
                # Check if our page is linked to the page in the second iteration or if the page in the second iteration has no links
                if page in corpus[link] or not corpus[link]:
                    # Add the pagerank of the page in the second iteration to the pagerank of our page. If no links, assume all pages are linked to it
                    temp_pageranks[page] += (
                        damping_factor 
                        * pageranks[link]
                        / (len(corpus[link]) if corpus[link] else len(corpus))
                    )
        if all(
            abs(temp_pageranks[page] - pageranks[page]) < 0.001
            for page in corpus.keys()
        ):
            return temp_pageranks    
        pageranks = temp_pageranks


if __name__ == "__main__":
    main()
