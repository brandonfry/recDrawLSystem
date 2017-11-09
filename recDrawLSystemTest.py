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
import timeit


class TestGetRules(unittest.TestCase):

    def test_ok_one_line_with_angle(self):
        ruleslist = ["60", "F", "F", "F: F+F--F+F"]
        rules = recDrawLSystem.getRules(ruleslist)
        self.assertEqual(rules, {"F": "F+F--F+F", "Axiom": "F", "Angle": 60,
                                 "Alias": "F"})

    def test_ok_one_line_no_angle(self):
        ruleslist = ["60", "F", "F", "F: F+F--F+F"]
        rules = recDrawLSystem.getRules(ruleslist)
        self.assertEqual(rules, {"F": "F+F--F+F", "Axiom": "F", "Angle": 60,
                                 "Alias": "F"})

    def test_ok_two_line_with_angle(self):
        ruleslist = ["60", "F", "F", "F: F+E--E+F", "E: E-F++F-E"]
        rules = recDrawLSystem.getRules(ruleslist)
        self.assertEqual(rules, {"F": "F+E--E+F", "E": "E-F++F-E",
                                 "Axiom": "F", "Angle": 60, "Alias": "F"})

    def test_ok_two_line_no_angle(self):
        ruleslist = ["90", "A", "F", "A: -BF+AFA+FB-", "B: +AF-BFB-FA+"]
        rules = recDrawLSystem.getRules(ruleslist)
        self.assertEqual(rules, {"A": "-BF+AFA+FB-", "B": "+AF-BFB-FA+",
                                 "Axiom": "A", "Angle": 90, "Alias": "F"})

    def test_wrong_no_rule(self):
        ruleslist = [" ", " ", " ", " "]
        self.assertRaises(recDrawLSystem.InputError, recDrawLSystem.getRules,
                          ruleslist)

    def test_wrong_no_colon(self):
        ruleslist = ["60", "A", "F", "A -A+A"]
        self.assertRaises(recDrawLSystem.InputError, recDrawLSystem.getRules,
                          ruleslist)

    def test_wrong_variable_not_defined(self):
        ruleslist = ["90", "A", "F", "A: -A+B"]
        self.assertRaises(recDrawLSystem.InputError, recDrawLSystem.getRules,
                          ruleslist)

    def test_wrong_reuse_variable(self):
        ruleslist = ["90", "A", "F", "A: -BF+AFA+FB-", "A: +AF-BFB-FA+"]
        self.assertRaises(recDrawLSystem.InputError, recDrawLSystem.getRules,
                          ruleslist)

    def test_wrong_invalid_rule(self):
        ruleslist = ["90", "A", "F", "A: A?A"]
        self.assertRaises(recDrawLSystem.InputError, recDrawLSystem.getRules,
                          ruleslist)

    def test_wrong_invalid_angle(self):
        ruleslist = ["9X", "A", "F", "A: A+F"]
        self.assertRaises(recDrawLSystem.InputError, recDrawLSystem.getRules,
                          ruleslist)


class TestGeneratePoints(unittest.TestCase):

    def test_size_0_one_line(self):
        rules = {"F": "F+F--F+F", "Axiom": "F", "Angle": 60, "Alias": "F"}
        point_string = recDrawLSystem.recGenerateLString(0, rules["Axiom"],
                                                         rules)
        self.assertEqual(point_string, "F")

    def test_size_0_one_line2(self):
        rules = {"F": "F+F--F+F", "Axiom": "F+F", "Angle": 60, "Alias": "F"}
        point_string = recDrawLSystem.recGenerateLString(0, rules["Axiom"],
                                                         rules)
        self.assertEqual(point_string, "F+F")

    def test_size_0_one_line3(self):
        rules = {"F": "F+F", "Axiom": "F-G", "Angle": 90, "Alias": "F"}
        point_string = recDrawLSystem.recGenerateLString(0, rules["Axiom"],
                                                         rules)
        self.assertEqual(point_string, "F-")

    def test_size_1_one_line(self):
        rules = {"F": "F+F--F+F", "Axiom": "F", "Angle": 60, "Alias": "F"}
        point_string = recDrawLSystem.recGenerateLString(1, rules["Axiom"],
                                                         rules)
        self.assertEqual(point_string, "F+F--F+F")

    def test_size_1_one_line2(self):
        rules = {"A": "F+F--F+F", "Axiom": "A", "Angle": 60, "Alias": "F"}
        point_string = recDrawLSystem.recGenerateLString(1, rules["Axiom"],
                                                         rules)
        self.assertEqual(point_string, "F+F--F+F")

    def test_size_2_one_line(self):
        rules = {"F": "F+F--F+F", "Axiom": "F", "Angle": 60, "Alias": "F"}
        point_string = recDrawLSystem.recGenerateLString(2, rules["Axiom"],
                                                         rules)
        self.assertEqual(point_string, "F+F--F+F+F+F--F+F--F+F--F+F+F+F--F+F")

    def test_size_3_one_line(self):
        rules = {"F": "F-F", "Axiom": "F", "Angle": 60, "Alias": "F"}
        point_string = recDrawLSystem.recGenerateLString(3, rules["Axiom"],
                                                         rules)
        self.assertEqual(point_string, "F-F-F-F-F-F-F-F")

    def test_size_1_two_line(self):
        rules = {"A": "-BF+AFA+FB-", "B": "+AF-BFB-FA+", "Axiom": "A",
                 "Angle": 90, "Alias": "F"}
        point_string = recDrawLSystem.recGenerateLString(1, rules["Axiom"],
                                                         rules)
        self.assertEqual(point_string, "-F+F+F-")

    def test_size_2_one_line2(self):
        rules = {"F": "F+F-F-F+F", "Axiom": "F", "Angle": 90, "Alias": "F"}
        point_string = recDrawLSystem.recGenerateLString(2, rules["Axiom"],
                                                         rules)
        self.assertEqual(point_string, "F+F-F-F+F+F+F-F-F+F-F+F-F-F+F-F+F-F" +
                                       "-F+F+F+F-F-F+F")

    def test_size_1_one_line3(self):
        rules = {"F": "F-F+F", "Axiom": "F+F+F", "Angle": 90, "Alias": "F"}
        point_string = recDrawLSystem.recGenerateLString(1, rules["Axiom"],
                                                         rules)
        self.assertEqual(point_string, "F-F+F+F-F+F+F-F+F")

    def test_size_2_two_line(self):
        rules = {"A": "-BF+AFA+FB-", "B": "+AF-BFB-FA+", "Axiom": "A",
                 "Angle": 90, "Alias": "F"}
        point_string = recDrawLSystem.recGenerateLString(2, rules["Axiom"],
                                                         rules)
        self.assertEqual(point_string, "-+F-F-F+F+-F+F+F-F-F+F+F-+F+F-F-F+-")


class TestPointClass(unittest.TestCase):

    def test_init(self):
        point = recDrawLSystem.Point(90)
        self.assertEqual((0, 0, 90), (point.x, point.y, point.angle))

    def test_update_F(self):
        point = recDrawLSystem.Point(90)
        point.update("F")
        self.assertEqual((1, 0), (point.x, point.y))

    def test_update_plus(self):
        point = recDrawLSystem.Point(90)
        point.update("+")
        self.assertEqual(270, point.orientation)

    def test_update_minus(self):
        point = recDrawLSystem.Point(90)
        point.update("-")
        self.assertEqual(90, point.orientation)

    def test_update_FpF(self):
        point = recDrawLSystem.Point(90)
        point.update("F")
        point.update("+")
        point.update("F")
        self.assertAlmostEqual(1, point.x)
        self.assertAlmostEqual(-1, point.y)

    def test_update_FpFmF(self):
        point = recDrawLSystem.Point(90)
        point.update("F")
        point.update("+")
        point.update("F")
        point.update("-")
        point.update("F")
        self.assertAlmostEqual(2, point.x)
        self.assertAlmostEqual(-1, point.y)

    def test_update_mF_45d(self):
        point = recDrawLSystem.Point(45)
        point.update("-")
        point.update("F")
        self.assertAlmostEqual(0.7071068, point.x)
        self.assertAlmostEqual(0.7071068, point.y)

    def test_update_mFpF_45d(self):
        point = recDrawLSystem.Point(45)
        point.update("-")
        point.update("F")
        point.update("+")
        point.update("F")
        self.assertAlmostEqual(1.7071068, point.x)
        self.assertAlmostEqual(0.7071068, point.y)

    def test_update_mmmmF(self):
        point = recDrawLSystem.Point(90)
        point.update("-")
        point.update("-")
        point.update("-")
        point.update("-")
        point.update("F")
        self.assertAlmostEqual(1, point.x)
        self.assertAlmostEqual(0, point.y)


class TestCalcUnityPoints(unittest.TestCase):

    def test_F(self):
        angle = 90
        ls = "F"
        up = recDrawLSystem.calcUnityPoints(ls, angle)
        self.assertEqual([(0, 0), (1, 0)], up)

    def test_FmF(self):
        angle = 90
        ls = "F-F"
        up = recDrawLSystem.calcUnityPoints(ls, angle)
        self.assertEqual([(0, 0), (1, 0), (1, 1)], up)

    def test_FmF_45(self):
        angle = 45
        ls = "F-F"
        up = recDrawLSystem.calcUnityPoints(ls, angle)
        ans = [(0, 0), (1, 0), (1.7071068, 0.7071068)]
        for i, item in enumerate(ans):
            for j, _ in enumerate(item):
                self.assertAlmostEqual(ans[i][j], up[i][j])


class TestScalePoints(unittest.TestCase):

    def test_1(self):
        up = [(0, 0), (1, 0), (1, 1)]
        points = recDrawLSystem.scalePoints(up)
        ans = [(-200, -200), (200, -200), (200, 200)]
        for i, item in enumerate(ans):
            for j, _ in enumerate(item):
                self.assertEqual(ans[i][j], points[i][j])

    def test_2(self):
        up = [(0, 0), (0.7071068, 0.7071068), (1.7071068, 0.7071068)]
        points = recDrawLSystem.scalePoints(up)
        ans = [(-200, -83), (-35, 83), (199, 83)]
        for i, item in enumerate(ans):
            for j, _ in enumerate(item):
                self.assertEqual(ans[i][j], points[i][j])

    def test_3(self):
        up = [(0, 0), (-1, 0), (1, 1)]
        points = recDrawLSystem.scalePoints(up)
        ans = [(0, -100), (-200, -100), (200, 100)]
        for i, item in enumerate(ans):
            for j, _ in enumerate(item):
                self.assertEqual(ans[i][j], points[i][j])


class TestCalcPoints(unittest.TestCase):
    pass


if __name__ == "__main__":
    unittest.main()
