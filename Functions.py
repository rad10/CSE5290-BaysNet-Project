from Elements import Node
from copy import deepcopy
from itertools import product


def normalize(arr: list) -> list:
    total = sum(arr)
    return list(map(lambda x: x / total, arr))


def Not(probability: float) -> float:
    return 1 - probability


def get_node(label: str, arr: list) -> Node:
    """This function gets the node that belongs to the given label
    in a given array
    @param label the label of the element desired
    @param arr the list of nodes to search for
    @returns the Node with the given label or None if it is not present
    """
    for i in arr:
        if i.key == label:
            return i
    return None


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
            results.update(get_roots(i))
    return results


def get_history(element: Node) -> set:
    """ This function gets all of the dependencies of the given node, and
    the dependencies of those all the way to the roots
    @param element the node that you want to get the entire history of
    @returns a set of all the nodes that the element remotely depends on
    """
    results = set(element.get_dependencies())
    for elm in element.get_dependencies():
        results.update(get_history(elm))
    return results


def enumeration_all(variables: list, observed: dict) -> float:
    # contingency if variables is empty
    if len(variables) == 0:
        return 1

    # Get given variable that enumerate all gets probability for
    given: Node = variables[0]
    spackage = set()
    if len(variables) > 1:
        spackage.update(variables[1:])
    # include everything up to roots
    for i in variables:
        spackage.update(get_history(i))

    # convert back to list to keep indexes
    package = list(spackage)

    # making table of conditions
    conditions = [[True, False] for a in package]

    # Changing boolean sets based on observed
    for key in observed.keys():
        if get_node(key, package):
            conditions[package.index(get_node(key, package))] = [observed[key]]
    iters = list(product(*conditions))
    sum_vals = [1 for a in iters]

    for conditional in range(len(sum_vals)):
        for node in range(len(package)):
            # making dict to get what values both have in common
            pstate = spackage.intersection(package[node].get_dependencies())
            state = dict()
            for s in pstate:
                state[s.key] = iters[conditional][package.index(s)]

            pval = float()
            if (len(pstate) == 0):
                pval = package[node]()[0]
            else:
                pval = package[node](state)[0]
            if not iters[conditional][node]:
                pval = Not(pval)

            sum_vals[conditional] *= pval

        # Getting dictionary differences for the given variable
        pstate = spackage.intersection(given.get_dependencies())
        state = dict()
        for s in pstate:
            state[s.key] = iters[conditional][package.index(s)]

        sum_vals[conditional] *= given(state)[0]
    return sum(sum_vals)


def enumeration_ask(vars: list, evidence: dict):
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
