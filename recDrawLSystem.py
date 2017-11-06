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


def drawLSystem(t, points):
    """
    Given a turtle object and list of points as tuples, draw
    a curve described by an L-System.
    """
    pass


def calcPoints(size, rules):
    """
    Given a dictionary of L-System rules, calculate all points
    along a curve of a particular size. Returns a list of points
    as tuples.
    """
    pass


def getRules(ruleslist):
    """
    Takes a user-input list of strings and parses them for L-system
    rules. Returns a dictionary of rules.

    ["F: F+F--F+F, 60"] -> {"F": ("F+F--F+F", 60)}
    """
    rules = {}
    validrule = re.compile(r"^([a-zA-Z][:][ ]*){1}[a-zA-Z+-]+" +
                           "([,][ ]*[0-9]+){0,1}")
    for rule in ruleslist:
        try:
            assert re.fullmatch(validrule, rule) is not None
        except AssertionError as e:
            raise ValueError
        r = re.split(r":[ ]*", rule, maxsplit=1)
        if re.search(r",", rule):
            r[1] = re.split(r",[ ]*", r[1], maxsplit=1)
        else:
            r[1] = [r[1], "90"]
        rules[r[0]] = (r[1][0], int(r[1][1]))
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
    size = 3
    ruleslist = ["F1: F+F--F+F, 60"]
    rules = getRules(ruleslist)
    points = calcPoints(size, rules)
    t, win = setupTurtle()
    drawLSystem(t, points)
    closeTurtle(win)
