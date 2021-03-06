# -*- coding: utf-8 -*-
"""
Copyright (C) Sun Nov  5 10:42:56 2017  Brandon C. Fry
brandoncfry@gmail.com

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


import turtle
import re
import math


class Point():
    """
    Tracks the last calculated point of an L-system. Takes updates
    as a string to move the point forward or turn it left or right.
    The angle of left and right turns is established when the
    instance is created.
    """

    def __init__(self, angle):
        self.x = 0
        self.y = 0
        self.angle = angle
        self.orientation = 0

    def update(self, move):
        if move == "F":
            self.forward()
        elif move == "+":
            self.right()
        elif move == "-":
            self.left()

    def right(self):
        self.orientation -= self.angle
        if self.orientation < 0:
            self.orientation += 360

    def left(self):
        self.orientation += self.angle
        if self.orientation >= 360:
            self.orientation -= 360

    def forward(self):
        self.x += math.cos(math.radians(self.orientation))
        self.y += math.sin(math.radians(self.orientation))


class InputError(Exception):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


def drawLSystem(t, points):
    """
    Given a turtle object and list of points as tuples, draw
    a curve described by an L-System.
    """

    t.penup()
    t.setpos(points[0])
    t.pendown()
    for point in points[1:]:
        t.setpos(point)


def recGenerateLString(size, rule, rules):
    """
    Given an L-system rule, a dictionary of L-system rules and curve size,
    generate recursively a flat L-system representation of the curve.
    Returns a single string.
    """

    s = ""
    if size == 0:
        sub_rule = ""
        aliases = rules["Alias"]
        for i in range(len(rule)):
            if rule[i] in aliases:
                sub_rule += "F"
            else:
                sub_rule += rule[i]
        return ''.join(re.findall(r"[F+-]", sub_rule))
    elif size >= 1:
        for char in rule:
            if char in rules.keys():
                s += recGenerateLString(size-1, rules[char], rules)
            elif char in "F+-":
                s += char
        return s


def calcUnityPoints(ls, angle):
    """
    Given a string of L-system commands and a default angle, calculates
    the points touched by the defined curve. Returns a list of x, y
    tuples. Absolute distance between points is 1.
    """

    point = Point(angle)
    up = [(0, 0)]
    for command in ls:
        point.update(command)
        if command == "F":
            up.append((point.x, point.y))
    return up


def scalePoints(up):
    """
    Given a list of x,y tuples of an L-system curve with an absolute
    distance between points of 1, scale the points up to fit within
    a 400 x 400 grid. Grid values range from (-200, -200) to (200, 200)
    """

    [x_max, y_max] = list(map(max, zip(*up)))
    [x_min, y_min] = list(map(min, zip(*up)))
    x_diff = x_max - x_min
    y_diff = y_max - y_min
    max_diff = max(x_diff, y_diff)
    scale = 400 // max_diff
    points = []
    for point in up:
        points.append((round(((point[0]-x_min)*scale)-(200*(x_diff/max_diff))),
                       round(((point[1]-y_min)*scale)-(200*(y_diff/max_diff)))))
    return points


def calcPoints(size, rules):
    """
    Given a dictionary of L-System rules, calculate all points
    along a curve of a particular size. Returns a list of points
    as tuples.
    """

    l_string = recGenerateLString(size, rules["Axiom"], rules)
    unity_points = calcUnityPoints(l_string, rules["Angle"])
    points = scalePoints(unity_points)
    return points


def getRules(ruleslist):
    """
    Takes a user-input list of strings and parses them for L-system
    rules. Returns a dictionary of rules.

    ["60", "F", "F: F+F--F+F, 60"] -> {"F": ("F+F--F+F", 60), "Axiom": "F",
    "Angle": 60}
    """

    rules = {}
    validangle = re.compile(r"^[0-9]+$")
    validrule = re.compile(r"^([a-zA-Z][:][ ]*){1}[a-zA-Z+-]+$")
    validaxiom = re.compile(r"^[a-zA-Z+-]+$")
    validalias = re.compile(r"^[a-zA-Z]+$")
    angle = ruleslist.pop(0)
    axiom = ruleslist.pop(0)
    alias = ruleslist.pop(0)
    try:
        assert re.fullmatch(validangle, angle) is not None
        rules["Angle"] = int(angle)
    except AssertionError as e:
        raise InputError(angle, "Angle is not valid")
    try:
        assert re.fullmatch(validaxiom, axiom) is not None
        rules["Axiom"] = axiom
    except AssertionError as e:
        raise InputError(axiom, "Axiom is not valid")
    try:
        assert re.fullmatch(validalias, alias)
        rules["Alias"] = alias
    except AssertionError as e:
        raise InputError(alias, "Alias is not valid")
    for rule in ruleslist:
        try:
            assert re.fullmatch(validrule, rule) is not None
        except AssertionError as e:
            raise InputError(rule, "Rule is not valid")
        r = re.split(r":[ ]*", rule, maxsplit=1)
        try:
            assert r[0] not in rules.keys()
        except AssertionError as e:
            raise InputError(r[0], "Variable already assigned.")
        rules[r[0]] = r[1]
    for rule in rules.values():
        for char in re.findall(r"[a-zA-Z]", str(rule)):
            try:
                assert char in [*rules.keys(), "F"]
            except AssertionError as e:
                raise InputError(char, "Variable not found in rules.")
    return rules


def get_input():
    ans = input("Would you like to input an L-System? Y/N: ").lower()
    if ans == "n":
        return None
    elif ans != "y":
        lsystem = get_input()
        return lsystem
    lsystem = []
    lsystem.append(int(input("Enter size as integer: ")))
    lsystem.append(input("Enter angle in degrees: "))
    lsystem.append(input("Enter axiom: "))
    lsystem.append(input("Enter aliases: "))
    n = int(input("Enter number of production rules: "))
    print("Enter production rules as in the following example")
    print("A: -AF+BFB+FA-")
    for i in range(1, n+1):
        lsystem.append(input("Rule {}: ".format(i)))
    return lsystem


def setupTurtle():
    t = turtle.Turtle()
    win = turtle.Screen()
    win.bgcolor("gray")
    t.speed(0)
    t.color("black")
    t.width(width=0)
    return t, win


def closeTurtle(win):
    win.exitonclick()
    turtle.done()


if __name__ == "__main__":
    # grab input for size, ruleslist
    lsystem = get_input()
    if lsystem == None:
        size = 4
        ruleslist = ["120", "F-G-G", "FG", "F: F-G+F+G-F", "G: GG"]
    else:
        size = lsystem[0]
        ruleslist = lsystem[1:]
    rules = getRules(ruleslist)
    points = calcPoints(size, rules)
    t, win = setupTurtle()
    drawLSystem(t, points)
    closeTurtle(win)