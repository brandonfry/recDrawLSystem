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
        ruleslist = ["60", "F", "F: F+F--F+F"]
        rules = recDrawLSystem.getRules(ruleslist)
        self.assertEqual(rules, {"F": "F+F--F+F", "Axiom": "F", "Angle": 60})

    def test_ok_one_line_no_angle(self):
        ruleslist = ["60", "F", "F: F+F--F+F"]
        rules = recDrawLSystem.getRules(ruleslist)
        self.assertEqual(rules, {"F": "F+F--F+F", "Axiom": "F", "Angle": 60})

    def test_ok_two_line_with_angle(self):
        ruleslist = ["60", "F", "F: F+E--E+F", "E: E-F++F-E"]
        rules = recDrawLSystem.getRules(ruleslist)
        self.assertEqual(rules, {"F": "F+E--E+F", "E": "E-F++F-E",
                                 "Axiom": "F", "Angle": 60})

    def test_ok_two_line_no_angle(self):
        ruleslist = ["90", "A", "A: -BF+AFA+FB-", "B: +AF-BFB-FA+"]
        rules = recDrawLSystem.getRules(ruleslist)
        self.assertEqual(rules, {"A": "-BF+AFA+FB-", "B": "+AF-BFB-FA+",
                                 "Axiom": "A", "Angle": 90})

    def test_wrong_no_rule(self):
        ruleslist = [" ", " ", " "]
        self.assertRaises(recDrawLSystem.InputError, recDrawLSystem.getRules,
                          ruleslist)

    def test_wrong_no_colon(self):
        ruleslist = ["60", "A", "A -A+A"]
        self.assertRaises(recDrawLSystem.InputError, recDrawLSystem.getRules,
                          ruleslist)

    def test_wrong_variable_not_defined(self):
        ruleslist = ["90", "A", "A: -A+B"]
        self.assertRaises(recDrawLSystem.InputError, recDrawLSystem.getRules,
                          ruleslist)

    def test_wrong_reuse_variable(self):
        ruleslist = ["90", "A", "A: -BF+AFA+FB-", "A: +AF-BFB-FA+"]
        self.assertRaises(recDrawLSystem.InputError, recDrawLSystem.getRules,
                          ruleslist)

    def test_wrong_invalid_rule(self):
        ruleslist = ["90", "A", "A: A?A"]
        self.assertRaises(recDrawLSystem.InputError, recDrawLSystem.getRules,
                          ruleslist)

    def test_wrong_invalid_angle(self):
        ruleslist = ["9X", "A", "A: A+F"]
        self.assertRaises(recDrawLSystem.InputError, recDrawLSystem.getRules,
                          ruleslist)


class TestGeneratePoints(unittest.TestCase):

    def test_size_0_one_line(self):
        rules = {"F": "F+F--F+F", "Axiom": "F", "Angle": 60}
        point_string = recDrawLSystem.recGenerateLString(0, rules["Axiom"],
                                                         rules)
        self.assertEqual(point_string, "F")

    def test_size_0_one_line2(self):
        rules = {"F": "F+F--F+F", "Axiom": "F+F", "Angle": 60}
        point_string = recDrawLSystem.recGenerateLString(0, rules["Axiom"],
                                                         rules)
        self.assertEqual(point_string, "F+F")

    def test_size_0_one_line3(self):
        rules = {"F": "F+F", "Axiom": "F-G", "Angle": 90}
        point_string = recDrawLSystem.recGenerateLString(0, rules["Axiom"],
                                                         rules)
        self.assertEqual(point_string, "F-")

    def test_size_1_one_line(self):
        rules = {"F": "F+F--F+F", "Axiom": "F", "Angle": 60}
        point_string = recDrawLSystem.recGenerateLString(1, rules["Axiom"],
                                                         rules)
        self.assertEqual(point_string, "F+F--F+F")

    def test_size_1_one_line2(self):
        rules = {"A": "F+F--F+F", "Axiom": "A", "Angle": 60}
        point_string = recDrawLSystem.recGenerateLString(1, rules["Axiom"],
                                                         rules)
        self.assertEqual(point_string, "F+F--F+F")

    def test_size_2_one_line(self):
        rules = {"F": "F+F--F+F", "Axiom": "F", "Angle": 60}
        point_string = recDrawLSystem.recGenerateLString(2, rules["Axiom"],
                                                         rules)
        self.assertEqual(point_string, "F+F--F+F+F+F--F+F--F+F--F+F+F+F--F+F")

    def test_size_3_one_line(self):
        rules = {"F": "F-F", "Axiom": "F", "Angle": 60}
        point_string = recDrawLSystem.recGenerateLString(3, rules["Axiom"],
                                                         rules)
        self.assertEqual(point_string, "F-F-F-F-F-F-F-F")

    def test_size_1_two_line(self):
        rules = {"A": "-BF+AFA+FB-", "B": "+AF-BFB-FA+", "Axiom": "A",
                 "Angle": 90}
        point_string = recDrawLSystem.recGenerateLString(1, rules["Axiom"],
                                                         rules)
        self.assertEqual(point_string, "-F+F+F-")

    def test_size_2_one_line2(self):
        rules = {"F": "F+F-F-F+F", "Axiom": "F", "Angle": 90}
        point_string = recDrawLSystem.recGenerateLString(2, rules["Axiom"],
                                                         rules)
        self.assertEqual(point_string, "F+F-F-F+F+F+F-F-F+F-F+F-F-F+F-F+F-F" +
                                       "-F+F+F+F-F-F+F")

    def test_size_1_one_line3(self):
        rules = {"F": "F-F+F", "Axiom": "F+F+F", "Angle": 90}
        point_string = recDrawLSystem.recGenerateLString(1, rules["Axiom"],
                                                         rules)
        self.assertEqual(point_string, "F-F+F+F-F+F+F-F+F")


class TestCalcPoints(unittest.TestCase):
    pass


class TestDrawLSystem(unittest.TestCase):
    pass


if __name__ == "__main__":
    unittest.main()
