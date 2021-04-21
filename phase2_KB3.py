from BaysNet.Elements import Node
from BaysNet.Functions import *

# Bayesian Network 3
NodeV = Node("V", "NodeV", 0.31)
NodeW = Node("W", "NodeW", 0.73, 0.55, V = NodeV)
NodeX = Node("X", "NodeX", 0.83, 0.43, V= NodeV)
NodeY = Node("Y", "NodeY", 0.62, 0.23, W = NodeW)
NodeZ = Node("Z", "NodeZ", 0.99, 0.91, 0.90, 0.86, 0.89, 0.72, 0.83, 0.20, W = NodeW, X = NodeX, Y = NodeY)

# Print tables for verification.
NodeV.print_table()
NodeW.print_table()
NodeX.print_table()
NodeY.print_table()
NodeZ.print_table()

print(f"\nQueries: ")

# Query one: P(Y | V, X)
print(f"P(Y | V, X) = {enumeration_all(NodeY, NodeX, NodeV, X = True, V = True)/enumeration_all(NodeX, NodeV, X = True, V = True):0.4f}")

# Query two: P(Z | W)
print(f"P(Z | W) = {enumeration_all(NodeZ, NodeW, W = True)/enumeration_all(NodeW):0.4f}")

# Query three: P(Z | W, X, Y)
print(f"P(Z | W, X, Y) = {enumeration_all(NodeZ, NodeY, NodeW, NodeX, W = True, X = True, Y = True)/enumeration_all(NodeY, NodeW, NodeX, W = True, X = True, Y = True):0.4f}")
