import unittest
import sys
import os

sys.path.append(os.path.abspath(os.getcwd()))
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '../..')))

from splines import Splines

A2 = Splines('INT 25z x 1,0m x 30P x 5H - ISO 4156', None)
A3 = Splines('INT 25z x 1,0m x 30R x 7H - ISO 4156', 25)
A4 = Splines('EXT 25z x 1,0m x 30P x 4h - ISO 4156', None)
A5 = Splines('EXT 25z x 1,0m x 30R x 6e - ISO 4156', None)
A6 = Splines('EXT 25z x 1,0m x 30P x 5js - ISO 4156', None)

B1 = Splines('EXT FLAT ROOT SIDE FIT 12/24 30T 30 CLASS 5 ANSI B92', None)


class ExampleA2(unittest.TestCase):
    def test_pitch_dia(self):
        self.assertEqual(round(A2.pitch_dia, ndigits=4), 25.0000)

    def test_base_dia(self):
        self.assertEqual(round(A2.base_dia, ndigits=4), 21.6506)

    def test_max_major_int_dia(self):
        self.assertEqual(round(A2.max_major_int_dia, ndigits=2), 26.74)

    def test_min_form_int_dia(self):
        self.assertEqual(round(A2.min_form_int_dia, ndigits=2), 26.20)

    def test_min_minor_int_dia(self):
        self.assertEqual(round(A2.min_minor_int_dia, ndigits=2), 24.09)

    def test_max_act_space_width(self):
        self.assertEqual(round(A2.max_act_width, ndigits=3), 1.626)

    def test_max_eff_space_width(self):
        self.assertEqual(round(A2.max_eff_width, ndigits=3), 1.603)

    def test_min_act_space_width(self):
        self.assertEqual(round(A2.min_act_width, ndigits=3), 1.593)

    def test_min_eff_space_width(self):
        self.assertEqual(round(A2.min_eff_width, ndigits=3), 1.571)


class ExampleA3(unittest.TestCase):
    def test_pitch_dia(self):
        self.assertEqual(round(A3.pitch_dia, ndigits=4), 25.0000)

    def test_base_dia(self):
        self.assertEqual(round(A3.base_dia, ndigits=4), 21.6506)

    def test_max_major_int_dia(self):
        self.assertEqual(round(A3.max_major_int_dia, ndigits=2), 27.04)

    def test_min_form_int_dia(self):
        self.assertEqual(round(A3.min_form_int_dia, ndigits=2), 26.20)

    def test_min_minor_int_dia(self):
        self.assertEqual(round(A3.min_minor_int_dia, ndigits=2), 24.09)

    def test_max_act_space_width(self):
        self.assertEqual(round(A3.max_act_width, ndigits=3), 1.708)

    def test_max_eff_space_width(self):
        self.assertEqual(round(A3.max_eff_width, ndigits=3), 1.660)

    def test_min_act_space_width(self):
        self.assertEqual(round(A3.min_act_width, ndigits=3), 1.620)

    def test_min_eff_space_width(self):
        self.assertEqual(round(A3.min_eff_width, ndigits=3), 1.571)


class ExampleA4(unittest.TestCase):
    def test_pitch_dia(self):
        self.assertEqual(round(A4.pitch_dia, ndigits=4), 25.0000)

    def test_base_dia(self):
        self.assertEqual(round(A4.base_dia, ndigits=4), 21.6506)

    def test_max_major_ext_dia(self):
        self.assertEqual(round(A4.max_major_ext_dia, ndigits=2), 26.00)

    def test_max_form_ext_dia(self):
        self.assertEqual(round(A4.max_form_dia, ndigits=2), 23.89)

    def test_min_minor_ext_dia(self):
        self.assertEqual(round(A4.min_minor_ext_dia, ndigits=2), 23.26)

    def test_max_eff_thickness(self):
        self.assertEqual(round(A4.max_eff_thickness, ndigits=3), 1.571)

    def test_max_act_thickness(self):
        self.assertEqual(round(A4.max_act_thickness, ndigits=3), 1.555)

    def test_min_eff_thickness(self):
        self.assertEqual(round(A4.min_eff_thickness, ndigits=3), 1.552)

    def test_min_act_thickness(self):
        self.assertEqual(round(A4.min_act_thickness, ndigits=3), 1.536)


class ExampleA5(unittest.TestCase):
    def test_pitch_dia(self):
        self.assertEqual(round(A5.pitch_dia, ndigits=4), 25.0000)

    def test_base_dia(self):
        self.assertEqual(round(A5.base_dia, ndigits=4), 21.6506)

    def test_max_major_ext_dia(self):
        self.assertEqual(round(A5.max_major_ext_dia, ndigits=2), 25.93)

    def test_max_form_ext_dia(self):
        self.assertEqual(round(A5.max_form_dia, ndigits=2), 23.83)

    def test_min_minor_ext_dia(self):
        self.assertEqual(round(A5.min_minor_ext_dia, ndigits=2), 22.89)

    def test_max_eff_thickness(self):
        self.assertEqual(round(A5.max_eff_thickness, ndigits=3), 1.531)

    def test_max_act_thickness(self):
        self.assertEqual(round(A5.max_act_thickness, ndigits=3), 1.498)

    def test_min_eff_thickness(self):
        self.assertEqual(round(A5.min_eff_thickness, ndigits=3), 1.477)

    def test_min_act_thickness(self):
        self.assertEqual(round(A5.min_act_thickness, ndigits=3), 1.445)


class ExampleA6(unittest.TestCase):
    def test_pitch_dia(self):
        self.assertEqual(round(A6.pitch_dia, ndigits=4), 25.0000)

    def test_base_dia(self):
        self.assertEqual(round(A6.base_dia, ndigits=4), 21.6506)

    def test_max_major_ext_dia(self):
        self.assertEqual(round(A6.max_major_ext_dia, ndigits=2), 26.00)

    def test_max_form_ext_dia(self):
        self.assertEqual(round(A6.max_form_dia, ndigits=2), 23.93)

    def test_min_minor_ext_dia(self):
        self.assertEqual(round(A6.min_minor_ext_dia, ndigits=2), 23.31)

    def test_max_eff_thickness(self):
        self.assertEqual(round(A6.max_eff_thickness, ndigits=3), 1.599)

    def test_max_act_thickness(self):
        self.assertEqual(round(A6.max_act_thickness, ndigits=3), 1.576)

    def test_min_eff_thickness(self):
        self.assertEqual(round(A6.min_eff_thickness, ndigits=3), 1.566)

    def test_min_act_thickness(self):
        self.assertEqual(round(A6.min_act_thickness, ndigits=3), 1.544)


class ExampleB1(unittest.TestCase):
    def test_pitch_dia(self):
        self.assertEqual(round(B1.pitch_dia, ndigits=6), 2.500000)

    def test_base_dia(self):
        self.assertEqual(round(B1.base_dia, ndigits=6), 2.165064)


if __name__ == '__main__':
    unittest.main(verbosity=2)