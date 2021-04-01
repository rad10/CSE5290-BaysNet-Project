from Elements import Node
from copy import deepcopy


def normalize(arr: list) -> list:
    total = sum(arr)
    return list(map(lambda x: x / total, arr))


def get_roots(element: Node) -> set:
    """ Gets the roots of a given node
    @param element the element that you want to get
    @returns the set that contains all roots to the given element
    """
    results = set()
    if len(element.get_dependencies()) == 0:
        return set(element)  # return itself because it is itself a root
    for i in element.get_dependencies():
        if len(i.get_dependencies()) == 0:
            # if the element being checked has no dependencies, then it is a root
            results.add(i)
        else:
            # if not, ask the element what its roots are
            results.add(get_roots(i))
    return results


def enumeration_ask(vars, evidence, network):
    # There has to be a query variable.
    if len(vars) == 0:
        return 1.0

    query = vars[0]
    probability = []

    # Query cannot be part of evidence.
    assert query not in evidence, "Query must differ from evidence."

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
