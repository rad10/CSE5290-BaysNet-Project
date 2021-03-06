"""The Elements module is where all element classes are stored.
Mostly holds the Node and Graph classes.

@author Nicholas Cottrell
@author Justyn Diaz
@date 2021-04-05
"""


class Node:
    ...


class Node:
    """A Neural Node for maintaining probability statistice
    @param key the Label that the node goes by
    @param probability_values, the values that the node is equal to based on its dependencies
    @param probability_dependents the nodes that this node depends on
    @author Nicholas Cottrell
    @author Justyn Diaz
    @date 2021-02-25
    """

    def __init__(self, key: str, name: str, *probability_values: float, **probability_dependents: Node) -> None:
        """Initiate a Node Object
        @param key A Character that represents that node within the network.
        This is very important is its how dependents recognize the Node.
        @param name The official name of the node. Can be used for description and clarification
        @param probability_values specify in order what probability the node is
        equal to based on its given values. there must be a specific amount of values based on
        the given dependencies.
        @param probability_dependents the node keys that can be paired with their respective nodes.
        @asserts that len(probability_values) = 2^len(probability_dependents)
        """
        if probability_dependents:
            assert len(probability_values) >= 2 ** len(probability_dependents.keys()
                                                       ), f"Not enough truth table values given for amount of dependencies: {len(probability_values)} of {2 ** len(probability_dependents.keys())}"
        self.key = key
        self.name = name
        self.probability_links = probability_dependents
        self.probability_values = probability_values
        self.used_by = list()

    def __str__(self):
        return self.key

    def __call__(self, **constant_deps: bool) -> tuple:
        """Calculates the possible probabilities based on given truths. The truths
        are based on node keys and setting what they are as a constant.
        @param constant_deps a dictionary of nodes with their keys matched with
        their boolean constant values.
        @returns a tuple that contains all possible probabilities based on the
        dependencies given.
        @asserts that all dependencies given are actual dependencies of this node.
        """
        # Checking if constants has vars that dont exist
        if (constant_deps):
            for c in constant_deps:
                assert c in self.probability_links.keys(
                ), f"{c} is not a dependency of {self}, {set(self.probability_links.keys())}"
        # check if there are no constant dependencies
        else:
            return self.probability_values
        # now to iterate through all items

        # making copy of values to figure out final result via process of elimination
        results = list(self.probability_values)
        headers = list(self.probability_links.keys())

        def elimination(ind: int, adjust: int = 0) -> None:
            if ind == len(headers):
                return
            # Does a binary search and sets nontrue to None
            if headers[ind] in constant_deps.keys():
                if constant_deps[headers[ind]]:
                    for i in range(adjust + len(results) // 2 ** (ind + 1), adjust + len(results) // 2 ** ind):
                        results[i] = None
                    elimination(ind + 1)
                else:
                    for i in range(adjust + 0, adjust + len(results) // 2 ** (ind + 1)):
                        results[i] = None
                    elimination(ind + 1, len(results) // 2 ** (ind + 1))
            else:
                elimination(ind + 1)
                elimination(ind + 1, len(results) // 2 ** (ind + 1))

        # Eliminate values that are not used due to constants
        elimination(0)

        # Removing Nones from remainder of the list
        while results.count(None) > 0:
            results.remove(None)

        return tuple(results)

    def link_source(self, node: Node) -> None:
        """Sets a node to be a source for a given value
        """
        self.probability_links[node.key] = node

    def link_dependent(self, node: Node) -> None:
        """Adds a node as a dependency"""
        self.used_by.append(node)

    def get_dependencies(self) -> tuple:
        """Gets a list of all dependencies"""
        if self.probability_links:
            return tuple(self.probability_links.values())
        return tuple()

    def get_dependency(self, label: str) -> Node:
        """Gets the node that this node depends on
        @param label the label of the depended on node
        @returns a node that this node depends on
        """
        return self.probability_links[label]

    def get_dependents(self) -> tuple:
        """Gives a list of all nodes that depend on this node"""
        return tuple(self.used_by)

    def print_table(self) -> None:
        """Prints a formatted table of all the stats of the given node"""
        if (self.probability_links == None):
            print("+--------+")
            print(f"| P({self.key:1s})   |")
            print("+--------+")
            print(f"| {self.probability_values[0]:0.04f} |")
            print("+--------+")
        else:
            arg_len = 2 + len(' '.join(self.probability_links.keys()))
            param_len = 2 + \
                max(6, len("P(A|)" + ",".join(self.probability_links.keys())))
            print(f"+{'-'*arg_len}+{'-'*param_len}+")
            print(
                f"| {' '.join(self.probability_links.keys())} | P({self.key}|{','.join(self.probability_links.keys())}) |")
            print(f"+{'-'*arg_len}+{'-'*param_len}+")
            for i in range(2**len(self.probability_links.keys())):
                # Gives us a string binary value to make truth table off of
                bool_key = f"{i:0{len(self.probability_links.keys())}b}"
                print(
                    f"| {' '.join(['T' if bool_key[j] == '0' else 'F' for j in range(len(self.probability_links.keys()))])} | {f'{self.probability_values[i]:0.04f}':<{param_len-1}s}|")
            print(f"+{'-'*arg_len}+{'-'*param_len}+")


class Graph:
    """Creates a graph that contains all nodes.
    Currently deprecated.
    """

    def __init__(self) -> None:
        """Initialize a graph. Takes no parameters
        """
        self.network: list = list()
        self.arcs = 0

    def __call__(self) -> list:
        """gives the container for the nodes"""
        return self.network

    def find_independent(self) -> list:
        """Gets a list of independent nodes
        @returns a list of nodes that have no dependencies
        """
        results = list()  # our results list that
        for node in self.network:
            # Checks if the dependencies actually doesnt exist
            if (node.get_dependencies() in [None, list(), tuple(), set()]):
                results.append(node)
        return results

    def add_node(self, node: Node) -> None:
        """Adds a node to the network
        @param node the node to add
        """
        assert len(
            self.network) <= 10, "Too many nodes attempted to be placed in network"
        self.network.append(node)

    def replace_node(self, network_node: Node, node: Node) -> None:
        """Replaces a given node with another node
        @param network_node the node to replace within the network
        @param node the new node to add to the network
        """
        index = self.network.index(network_node)
        self.network[index] = node

    def set_arc(self, parent: Node, child: Node) -> None:
        """Set the arc between the given parent and child nodes
        @param parent the node that should be a source of data for the child
        @param child the node that depends on parent
        """
        # First check that there arent too many arcs currently
        assert self.arcs <= 15, "Too many arcs in the current network. Max: 15"
        # Check that adding this arc wont make network cyclic
        assert len(self.find_independent()
                   ) > 1, "Cannot add this arc as it would make network cyclic"
        parent = self.network[self.network.index(parent)]
        child = self.network[self.network.index(child)]
        parent.link_dependent(child)
        child.link_source(parent)
