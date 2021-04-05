from BaysNet.Elements import Node
from BaysNet.Functions import *

Burglary = Node("B", "Burglary", 0.001)
Earthquake = Node("E", "Earthquake", 0.002)
Alarm = Node("A", "Alarm", 0.95, 0.94, 0.29, 0.001, B=Burglary, E=Earthquake)
JohnCall = Node("J", "John", 0.90, 0.05, A=Alarm)
MaryCall = Node("M", "Mary", 0.70, 0.01, A=Alarm)

print(
    f"P(J|M) = {enumeration_all(JohnCall, MaryCall, M=True)/enumeration_all(MaryCall):0.4f}")
