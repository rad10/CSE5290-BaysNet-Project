from Elements import Node
from copy import deepcopy

def normalize(arr: list) -> list:
    total = sum(arr)
    for i in range(len(arr)):
        arr[i] /= total
    return arr

def enumeration_ask(vars, evidence, network):
    # There has to be a query variable.
    if len(vars) == 0:
        return 1.0

    query = vars[0]
    probability = []

    # Query cannot be part of evidence.
    if query in evidence:
        return print("Query must differ from evidence.")
    else:   
        # For query = True, insert normal probabilistic values and enumerate.
        observed = deepcopy(evidence)
        observed.append(query)
        # TODO: enumerate here (make new function and append result to probability)

        # For query = False, insert probabilistic values - 1 and enumerate.
        observed = deepcopy(evidence)
        for x in range(0, len(query.probability_values)):
            query.probability_values[x] = 1 - query.probability_values[x]
        observed.append(query)
        # TODO: enumerate here (make new function and append result to probability)

        return normalize(probability)

# TODO: def enumerate_all