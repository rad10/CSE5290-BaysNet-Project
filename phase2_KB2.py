from BaysNet.Elements import Node
from BaysNet.Functions import *

# Bayesian Network 2
NodeA = Node("A", "NodeA", 0.53)
NodeB = Node("B", "NodeB", 0.009)
NodeC = Node("C", "NodeC", 0.99, 0.89, 0.63, 0.13, A = NodeA, B = NodeB)
NodeD = Node("D", "NodeD", 0.78)
NodeE = Node("E", "NodeE", 0.64, 0.30, 0.12, 0.02, C = NodeC, D = NodeD)

# Print tables for verification.
NodeA.print_table()
NodeB.print_table()
NodeC.print_table()
NodeD.print_table()
NodeE.print_table()

print(f"\nQueries: ")

# Query one: P(D | C)
print(f"P(D | C) = {enumeration_all(NodeD, NodeC, C = True)/enumeration_all(NodeC):0.4f}")

# Query two: P(E | A, C)
print(f"P(E | A, C) = {enumeration_all(NodeE, NodeC, NodeA, C = True, A = True)/enumeration_all(NodeC, NodeA, C = True, A = True):0.4f}")

# Query three: P(E | A, B)
print(f"P(E | A, B) = {enumeration_all(NodeE, NodeA, NodeB, A = True, B = True)/enumeration_all(NodeA, NodeB, A = True, B = True):0.4f}")
