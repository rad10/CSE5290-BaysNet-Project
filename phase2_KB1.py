from BaysNet.Elements import Node
from BaysNet.Functions import *

# Bayesian Network 1
NodeA = Node("A", "NodeA", 0.95)
NodeB = Node("B", "NodeB", 0.90)
NodeC = Node("C", "NodeC", 0.89, 0.11, A = NodeA)
NodeD = Node("D", "NodeD", 0.82, 0.40, B = NodeB)
NodeE = Node("E", "NodeE", 0.70, 0.55, 0.21, 0.10, B = NodeB, C = NodeC)
NodeF = Node("F", "NodeF", 0.68, 0.46, C = NodeC)

# Print tables for verification.
NodeA.print_table()
NodeB.print_table()
NodeC.print_table()
NodeD.print_table()
NodeE.print_table()
NodeF.print_table()

print(f"\nQueries: ")

# Query one: P(E | B)
print(f"P(E | B) = {enumeration_all(NodeE, NodeB, B = True)/enumeration_all(NodeB):0.4f}")

# Query two: P(E | C)
print(f"P(E | C) = {enumeration_all(NodeE, NodeC, C = True)/enumeration_all(NodeC):0.4f}")

# Query three: P(A ^ ~B ^ ~C ^ D ^ E ^ F)
print(f"P(A ^ ~B ^ ~C ^ D ^ E ^ F) = {enumeration_all(NodeA, NodeB, NodeC, NodeD, NodeE, NodeF, A= True, B = False, C = False, D = True, E = True, F = True):0.4f}")
