from BaysNet import Node, Graph
from BaysNet.Elements import *
from BaysNet.Functions import *

# Create graph.
testGraph = Graph()

# Create nodes.
Burglary = Node("B", "Burglary", 0.001)
Earthquake = Node("E", "Earthquake", 0.002)
Alarm = Node("A", "Alarm", 0.95, 0.94, 0.29, 0.001, B=None, E=None)
JohnCall = Node("J", "John", 0.90, 0.05, A=None)
MaryCall = Node("M", "Mary", 0.70, 0.01, A=None)

# Add nodes to the graph.
testGraph.add_node(Burglary)
testGraph.add_node(Earthquake)
testGraph.add_node(Alarm)
testGraph.add_node(JohnCall)
testGraph.add_node(MaryCall)

# Creates arcs.
# Burglary + Earthquake = source nodes.
testGraph.set_arc(Burglary, Alarm)
testGraph.set_arc(Earthquake, Alarm)
testGraph.set_arc(Alarm, JohnCall)
testGraph.set_arc(Alarm, MaryCall)

# Print tables.
# Burglary.print_table()
# Earthquake.print_table()
Alarm.print_table()
# JohnCall.print_table()
# MaryCall.print_table()


# print(Alarm())
# print(Alarm(B=False, E=True))

print(enumeration_all(MaryCall, M=True))
print(enumeration_all(JohnCall, MaryCall, M=True))
print(enumeration_ask(MaryCall))


# My tests on special args
# def func(**args: bool):
#     print(type(args))
#     print(args)
#     print(len(args))
#     print(bool(args))


# def sfunc(query: str, *given: str, **observed: bool):
#     print(query, given, observed)
#     print(type(given), type(observed))
#     print(bool(given), bool(observed))


# func()
# sfunc("A")
# func(A=True, B=False, C="Hello", D=None)
# sfunc("A", "B", "C", "D", B=True, C=True, D=False)
