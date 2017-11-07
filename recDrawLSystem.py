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
        pass


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

    pass


def recGenerateLString(size, rule, rules):
    """
    Given an L-system rule, a dictionary of L-system rules and curve size,
    generate recursively a flat L-system representation of the curve.
    Returns a single string.
    """

    s = ""
    if size == 0:
        return ''.join(re.findall(r"[F+-]", rule))
    elif size >= 1:
        for char in rule:
            if char in rules.keys():
                s += recGenerateLString(size-1, rules[char], rules)
            elif char in "F+-":
                s += char
        return s


def calcUnityPoints(ls, angle):
    pass


def scalePoints(up):
    pass


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
    validaxiom = re.compile(r"^[a-z-A-Z+-]+$")
    angle = ruleslist.pop(0)
    axiom = ruleslist.pop(0)
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


def setupTurtle():
    t = turtle.Turtle()
    win = turtle.Screen()
    win.bgcolor("gray")
    t.speed(0)
    t.penup()
    t.setposition(-200, -200)
    t.pendown()
    t.color("black")
    t.width(width=0)
    return t, win


def closeTurtle(win):
    win.exitonclick()
    turtle.done()


if __name__ == "__main__":
    # grab input for size, ruleslist
    size = 1
    ruleslist = ["90", "A", "A: -BF+AFA+FB-", "B: +AF-BFB-FA+"]
    rules = getRules(ruleslist)
    points = calcPoints(size, rules)
    t, win = setupTurtle()
    drawLSystem(t, points)
    closeTurtle(win)
