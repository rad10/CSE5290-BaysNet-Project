#!/usr/bin/python3
# -*- coding: utf-8 -*-

from .Elements import Node
from itertools import product


def normalize(arr: list) -> list:
    """Normalizes a list of numbers based on the sum of all its values
    """
    total = sum(arr)
    return list(map(lambda x: x / total, arr))


def Not(probability: float) -> float:
    """Probabilistic not function.
    @param probability a float number that represents the probability of a
    fact being true.
    @returns a float probability of a fact not being true.
    """
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


def __enum(target: Node, *given: Node, **observed: bool) -> list:
    # Get given variable that enumerate all gets probability for
    spackage = get_history(target)
    spackage.update(given)
    # include everything up to roots
    for i in given:
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
                pval = package[node](**state)[0]
            if not iters[conditional][node]:
                pval = Not(pval)

            sum_vals[conditional] *= pval

        # Getting dictionary differences for the given variable
        pstate = spackage.intersection(target.get_dependencies())
        state = dict()
        for s in pstate:
            state[s.key] = iters[conditional][package.index(s)]

        sum_vals[conditional] *= target(**state)[0]
    return sum_vals


def enumeration_all(target: Node = None, *given: Node, **observed: bool) -> float:
    """Returns the absolute probability of a node given certain environment variables.
    @param target the node that you want to get the whole probability of its success.
    @param given nodes that are given to have been used in finding the targets
    probability.
    @param observed a dictionary of values acting as the probabilities that are
    a constant chance.
    @returns a probability value of that target being true in any circumstance
    based on observed truths.
    """
    # contingency if variables is empty
    if not target:
        return 1
    return sum(__enum(target, *given, **observed))


def enumeration_ask(target: Node = None, *vars: Node, **evidence: bool) -> list:
    """Ask for all potential probabilities of a given node being true and asks
    for that distribution.
    @param target the node that you want to get the whole probability of its success.
    @param vars nodes that are given to have been used in finding the targets
    probability.
    @param evidence a dictionary of values acting as the probabilities that are
    a constant chance.
    @returns a normalized distribution of the given variable.
    """
    return normalize(__enum(target, *vars, **evidence))
