# -*- coding: utf-8 -*-
"""
Copyright (C) Sun Nov  5 10:56:31 2017  Brandon C. Fry
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


import unittest
import recDrawLSystem


class TestGetRules(unittest.TestCase):

    def test_ok_one_line_with_angle(self):
        ruleslist = ["F: F+F--F+F, 60"]
        rules = recDrawLSystem.getRules(ruleslist)
        self.assertEqual(rules, {"F": ("F+F--F+F", 60)})

    def test_ok_one_line_no_angle(self):
        ruleslist = ["F: F+F--F+F"]
        rules = recDrawLSystem.getRules(ruleslist)
        self.assertEqual(rules, {"F": ("F+F--F+F", 90)})

    def test_ok_two_line_with_angle(self):
        ruleslist = ["F: F+E--E+F, 60", "E: E-F++F-E, 70"]
        rules = recDrawLSystem.getRules(ruleslist)
        self.assertEqual(rules, {"F": ("F+E--E+F", 60),
                                 "E": ("E-F++F-E", 70)})

    def test_ok_two_line_no_angle(self):
        ruleslist = ["A: -BF+AFA+FB-", "B: +AF-BFB-FA+"]
        rules = recDrawLSystem.getRules(ruleslist)
        self.assertEqual(rules, {"A": ("-BF+AFA+FB-", 90),
                                 "B": ("+AF-BFB-FA+", 90)})

    def test_wrong_one_line1(self):
        ruleslist = [" "]
        self.assertRaises(recDrawLSystem.InputError, recDrawLSystem.getRules,
                          ruleslist)

    def test_wrong_one_line2(self):
        ruleslist = ["A: -A+A60"]
        self.assertRaises(recDrawLSystem.InputError, recDrawLSystem.getRules,
                          ruleslist)

    def test_wrong_one_line3(self):
        ruleslist = ["A: -A+B"]
        self.assertRaises(recDrawLSystem.InputError, recDrawLSystem.getRules,
                          ruleslist)

    def test_wrong_reuse_variable(self):
        ruleslist = ["A: -BF+AFA+FB-", "A: +AF-BFB-FA+"]
        self.assertRaises(recDrawLSystem.InputError, recDrawLSystem.getRules,
                          ruleslist)


class TestCalcPoints(unittest.TestCase):
    pass


class TestDrawLSystem(unittest.TestCase):
    pass


if __name__ == "__main__":
    unittest.main()

