import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

# Define the test size
TEST_SIZE = 0.4


def main():
    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    # Create lists for evidence and labels
    evidence = []
    labels = []
    with open(filename, newline="") as csvfile:
        reader = csv.reader(csvfile)
        # Store the first row to be used as labels
        row1 = next(reader)
        for row in reader:
            evidence_row = []
            for i in range(len(row) - 1):
                # Call label_to_evidence to convert the evidence to the correct type
                evidence_row.append(label_to_evidence(row1[i], row[i]))
            if row[-1] == "TRUE":
                labels.append(1)
            else:
                labels.append(0)
            evidence.append(evidence_row)
    return (evidence, labels)


def label_to_evidence(label, evidence):
    """
    Takes in the label and evidence and returns the evidence in the correct type"""
    # Check the label and return the evidence that should be in integers
    if (
        label == "Administrative" 
        or label == "Informational" 
        or label == "ProductRelated" 
        or label == "OperatingSystems" 
        or label == "Browser" 
        or label == "Region" 
        or label == "TrafficType"
    ):
        return int(evidence)
    # Check the label and return the evidence that should be in floats
    if (
        label == "Administrative_Duration" 
        or label == "Informational_Duration" 
        or label == "ProductRelated_Duration" 
        or label == "BounceRates" 
        or label == "ExitRates" 
        or label == "PageValues" 
        or label == "SpecialDay"
    ):
        return float(evidence)
    # Convert the month name to an integer
    if label == "Month":
        if evidence == "Jan":
            return 0
        if evidence == "Feb":
            return 1
        if evidence == "Mar":
            return 2
        if evidence == "Apr":
            return 3
        if evidence == "May":
            return 4
        if evidence == "June":
            return 5
        if evidence == "Jul":
            return 6
        if evidence == "Aug":
            return 7
        if evidence == "Sep":
            return 8
        if evidence == "Oct":
            return 9
        if evidence == "Nov":
            return 10
        if evidence == "Dec":
            return 11
    if label == "VisitorType":
        if evidence == "Returning_Visitor":
            return 1
        else:
            return 0
    if label == "Weekend":
        if evidence:
            return 1
        else:
            return 0
        

def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    # Create and train the model using the scikit-learn KNeighborsClassifier
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)
    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    # Specify variables for number of true positives, true negatives, false positives, and false negatives
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    # Check for true positives, true negatives, false positives, and false negatives
    for i in range(len(labels)):
        if predictions[i] == 1:
            if labels[i] == 1:
                tp += 1
            else:
                fp += 1
        else:
            if labels[i] == 0:
                tn += 1
            else:
                fn += 1
    # Calculate sensitivity and specificity
    sensitivity = tp / (tp + fn)
    specificity = tn / (tn + fp)
    return (sensitivity, specificity)


if __name__ == "__main__":
    main()
