import re
from math import ceil, cos, sin, tan, pi, radians, sqrt, degrees
from renard import R40, find_greater_than_or_equal

# See table 5 ISO 4156-1:2005
FUNDAMENTAL_DEVIATIONS = {
    range(1, 4): {
        'd': -20,
        'e': -14,
        'f': -6,
        'h': 0,
        'H': 0,
    },
    range(3, 7): {
        'd': -30,
        'e': -20,
        'f': -10,
        'h': 0,
        'H': 0,
    },
    range(7, 10): {
        'd': -40,
        'e': -25,
        'f': -13,
        'h': 0,
        'H': 0,
    },
    range(10, 18): {
        'd': -50,
        'e': -32,
        'f': -16,
        'h': 0,
        'H': 0,
    },
    range(18, 30): {
        'd': -65,
        'e': -40,
        'f': -20,
        'h': 0,
        'H': 0,
    },
    range(30, 50): {
        'd': -80,
        'e': -50,
        'f': -25,
        'h': 0,
        'H': 0,
    },
    range(50, 80): {
        'd': -100,
        'e': -60,
        'f': -30,
        'h': 0,
        'H': 0,
    },
    range(80, 120): {
        'd': -120,
        'e': -72,
        'f': -36,
        'h': 0,
        'H': 0,
    },
    range(120, 180): {
        'd': -145,
        'e': -85,
        'f': -43,
        'h': 0,
        'H': 0,
    },
    range(180, 250): {
        'd': -170,
        'e': -100,
        'f': -50,
        'h': 0,
        'H': 0,
    },
    range(250, 315): {
        'd': -190,
        'e': -110,
        'f': -56,
        'h': 0,
        'H': 0,
    },
    range(315, 400): {
        'd': -210,
        'e': -125,
        'f': -62,
        'h': 0,
        'H': 0,
    },
    range(400, 500): {
        'd': -230,
        'e': -135,
        'f': -68,
        'h': 0,
        'H': 0,
    },
    range(500, 630): {
        'd': -260,
        'e': -145,
        'f': -76,
        'h': 0,
        'H': 0,
    },
    range(630, 800): {
        'd': -290,
        'e': -160,
        'f': -80,
        'h': 0,
        'H': 0,
    },
    range(800, 1000): {
        'd': -320,
        'e': -170,
        'f': -86,
        'h': 0,
        'H': 0,
    },
}

# See table 11 ISO 4156-1:2005
MAJOR_MINOR_DIA_TOLERANCES = {
    range(1, 4): {
        10: 40
    },
    range(4, 7): {
        10: 48,
        11: 75
    },
    range(7, 11): {
        10: 58,
        11: 90
    },
    range(11, 19): {
        10: 70,
        11: 110,
        12: 180
    },
    range(19, 31): {
        10: 84,
        11: 130,
        12: 210
    },
    range(31, 51): {
        10: 100,
        11: 160,
        12: 250
    },
    range(51, 81): {
        10: 120,
        11: 190,
        12: 300
    },
    range(81, 121): {
        11: 200,
        12: 350
    },
    range(121, 181): {
        11: 250,
        12: 400
    },
    range(181, 251): {
        12: 460
    },
    range(251, 316): {
        12: 520
    },
    range(316, 401): {
        12: 570
    },
    range(401, 501): {
        12: 630
    },
    range(501, 631): {
        12: 700
    },
    range(631, 801): {
        12: 800
    },
    range(801, 1001): {
        12: 900
    },
}

# see table 107 ANSI B92.1-1996
maj_min_dia_tolerances_dict = {
    range(1, 3): {
        'TAB': 0.0200,
        'FN': lambda P: round((2000 / P + 250) * 1e-4, ndigits=4)
    },
    range(3, 4): {
        'TAB': 0.0150,
        'FN': lambda P: round((2000 / P + 200) * 1e-4, ndigits=4)
    },
    range(4, 5): {
        'TAB': 0.0100,
        'FN': lambda P: round((2000 / P + 150) * 1e-4, ndigits=4)
    },
    range(5, 6): {
        'TAB': 0.0080,
        'FN': lambda P: round((2000 / P + 130) * 1e-4, ndigits=4)
    },
    range(6, 32): {
        'TAB': 0.0050,
        'FN': lambda P: round((2000 / P + 100) * 1e-4, ndigits=4)
    },
    range(32, 64): {
        'TAB': 0.0030,
        'FN': lambda P: round((2000 / P + 80) * 1e-4, ndigits=4)
    },
    range(64, 160): {
        'TAB': 0.0020,
        'FN': lambda P: round((2000 / P + 70) * 1e-4, ndigits=4)
    },
}

# see table 106 ANSI B92.1-1996
allowances_class5 = {
    range(1, 4): {
        'machining': lambda N: round((0.18 * N + 15) * 1e-4, ndigits=4),
        'variations': lambda N: round((0.35 * N + 20) * 1e-4, ndigits=4),
    },
    range(4, 6): {
        'machining': lambda N: round((0.15 * N + 13) * 1e-4, ndigits=4),
        'variations': lambda N: round((0.23 * N + 18) * 1e-4, ndigits=4),
    },
    range(6, 10): {
        'machining': lambda N: round((0.15 * N + 11) * 1e-4, ndigits=4),
        'variations': lambda N: round((0.20 * N + 15) * 1e-4, ndigits=4),
    },
    range(10, 16): {
        'machining': lambda N: round((0.10 * N + 11) * 1e-4, ndigits=4),
        'variations': lambda N: round((0.17 * N + 14) * 1e-4, ndigits=4),
    },
    range(16, 24): {
        'machining': lambda N: round((0.07 * N + 11) * 1e-4, ndigits=4),
        'variations': lambda N: round((0.12 * N + 13) * 1e-4, ndigits=4),
    },
    range(24, 49): {
        'machining': lambda N: round((0.07 * N + 11) * 1e-4, ndigits=4),
        'variations': lambda N: round((0.12 * N + 11) * 1e-4, ndigits=4),
    },
    range(64, 81): {
        'machining': lambda N: round((0.06 * N + 9) * 1e-4, ndigits=4),
        'variations': lambda N: round((0.10 * N + 10) * 1e-4, ndigits=4),
    },
    range(128, 256): {
        'machining': lambda N: round((0.05 * N + 9) * 1e-4, ndigits=4),
        'variations': lambda N: round((0.08 * N + 9) * 1e-4, ndigits=4),
    },
}

involute = lambda alpha: tan(radians(alpha)) - radians(alpha)
sevolute = lambda phi: 1 / cos(radians(phi)) - involute(phi)
inverse_involute = lambda x: x**(1 / 3) / (.693357 + .192484 * x**(2 / 3))


class Splines:
    """
    A splines class

    Attributes
    ----------
    spec: str
        A formatted string according to either the designation section in section 12.3 ISO 4156-1:2005, or ANSI B92.
    length: float
        The splines length, default None.
    
    Methods
    -------
    calculate_spline_sizes()
        Calculates the spline sizes to the given specification
    print_drawing_data()
        Prints the list of sizes required on the splined component drawing.
    """
    def __init__(self, spec: str, length=None):
        self.spec = spec
        self.length = length
        self.calculate_spline_sizes()

    def calculate_spline_sizes(self):
        """Calculates the sizes according to the methodology either in ISO 4156:1-2001, or in , or ANSI B92, stores the key sizes in the class attributes."""
        spec_list = [
            i for i in re.split(
                r'x| |/|-|ISO|4156|ANSI|B92|ROOT|FIT|BS|3550|CLASS', self.spec)
            if bool(i)
        ]
        if 'ANSI' in self.spec:
            self.spline_type, self.spline_root, self.spline_fit, self.diametral_pitch, self.stub_pitch, self.teeth, self.pressure_angle, self.tol_class = spec_list
            self.diametral_pitch = float(
                self.diametral_pitch) if '.' in self.diametral_pitch else int(
                    self.diametral_pitch)
            self.pressure_angle = float(self.pressure_angle)
            self.stub_pitch = int(self.stub_pitch)
            self.teeth = int(self.teeth[:-1])
            self.tol_class = int(self.tol_class)

            self.pitch_dia = self.teeth / self.diametral_pitch
            self.base_dia = self.pitch_dia * cos(radians(self.pressure_angle))
            self.circular_pitch = pi / float(self.diametral_pitch)

            for pitch_range in maj_min_dia_tolerances_dict:
                if self.diametral_pitch in pitch_range:
                    self.dia_tolerance = maj_min_dia_tolerances_dict[
                        pitch_range]

            for pitch_range in allowances_class5:
                if self.diametral_pitch in pitch_range:
                    self.tolerances_class5 = allowances_class5[pitch_range][
                        'machining'](self.teeth) + allowances_class5[
                            pitch_range]['variations'](self.teeth)
            if self.tol_class == 4:
                self.total_tolerance = 0.71 * self.tolerances_class5
            elif self.tol_class == 5:
                self.total_tolerance = self.tolerances_class5
            elif self.tol_class == 6:
                self.total_tolerance = 1.40 * self.tolerances_class5
            elif self.tol_class == 7:
                self.total_tolerance = 2.00 * self.tolerances_class5

            # see table 2 ANSI B92.1-1996
            self.rad_form_clearance = min(max(0.001 * self.pitch_dia, 0.002),
                                          0.01)

            # see table 2 ANSI B92.1-1996
            form_dia_dict = {
                'EXT': {
                    30.0: lambda N, P:
                    (N - 1) / P - 2 * self.rad_form_clearance,
                    37.5: lambda N, P:
                    (N - 0.8) / P - 2 * self.rad_form_clearance,
                    45.0: lambda N, P:
                    (N - 0.6) / P - 2 * self.rad_form_clearance,
                },
                'INT': {
                    'SIDE':
                    lambda N, P: (N + 1) / P + 2 * self.rad_form_clearance,
                    'DIA':
                    lambda N, P:
                    (N + 0.8) / P + 2 * self.rad_form_clearance - 0.004,
                },
            }
            # see table 2 ANSI B92.1-1996
            min_minor_dia_dict = {
                'INT': {
                    30.0: lambda N, P: (N - 1) / P,
                    37.5: lambda N, P: (N - 0.8) / P,
                    45.0: lambda N, P: (N - 0.6) / P,
                },
                'EXT': {
                    30.0: {
                        'FLAT':
                        lambda N, P: (N - 1.35) / P - 0.004 - 2 * self.
                        total_tolerance / tan(radians(self.pressure_angle)),
                        'FILLET': {
                            range(1, 12 + 1):
                            lambda N, P:
                            (N - 1.9) / P - 2 * self.total_tolerance / tan(
                                radians(self.pressure_angle)),
                            range(16, 160):
                            lambda N, P:
                            (N - 2.1) / P - 2 * self.total_tolerance / tan(
                                radians(self.pressure_angle)),
                        },
                    },
                    37.5:
                    lambda N, P:
                    (N - 1.4) / P - 2 * self.total_tolerance / tan(
                        radians(self.pressure_angle)),
                    45.0:
                    lambda N, P:
                    (N - 1.1) / P - 2 * self.total_tolerance / tan(
                        radians(self.pressure_angle)),
                },
            }
            # see table 107a ANSI B92.1-1996
            eff_clearance_dia_fit_dict = {
                range(1, 4): lambda N: round(
                    (0.20 * N + 18) * 1e-4, ndigits=4),
                range(4, 6): lambda N: round(
                    (0.15 * N + 16) * 1e-4, ndigits=4),
                range(6, 10): lambda N: round(
                    (0.10 * N + 14) * 1e-4, ndigits=4),
                range(10, 16): lambda N: round(
                    (0.07 * N + 14) * 1e-4, ndigits=4),
            }
            for pitch_range in eff_clearance_dia_fit_dict:
                if self.diametral_pitch in pitch_range:
                    self.eff_clearance_dia_fit = eff_clearance_dia_fit_dict[
                        pitch_range](self.teeth)
                elif self.diametral_pitch >= 16:
                    self.eff_clearance_dia_fit = 15 * 1e-4

            if self.spline_type == 'EXT':
                self.form_dia = form_dia_dict[self.spline_type][
                    self.pressure_angle](self.teeth, self.diametral_pitch)
                self.min_form_ext_dia = sqrt(3 * self.teeth**2 + (
                    self.teeth - 0.016 * self.diametral_pitch - 4.5)**2) / (
                        2 * self.diametral_pitch
                    ) if self.spline_root == 'FLAT' else sqrt(
                        3 * self.teeth**2 +
                        (self.teeth - 5.359)**2) / (2 * self.diametral_pitch)
                if self.pressure_angle == 30.0:
                    if self.spline_fit == 'SIDE':
                        self.max_eff_thickness = 0.5 * self.circular_pitch
                    elif self.spline_fit == 'DIA':
                        self.max_eff_thickness = 0.5 * self.circular_pitch - self.eff_clearance_dia_fit
                    if self.spline_root == 'FILLET':
                        for pitch_range in min_minor_dia_dict[
                                self.spline_type][self.pressure_angle][
                                    self.spline_root]:
                            if self.diametral_pitch in pitch_range:
                                self.min_minor_ext_dia = self.min_minor_ext_dia[
                                    self.spline_type][self.pressure_angle][
                                        self.spline_root][pitch_range](
                                            self.teeth, self.diametral_pitch)
                    elif self.spline_root == 'FLAT':
                        self.min_minor_ext_dia = min_minor_dia_dict[
                            self.spline_type][self.pressure_angle][
                                self.spline_root](self.teeth,
                                                  self.diametral_pitch)
                elif self.pressure_angle == 37.5:
                    self.max_eff_thickness = (0.5 * pi +
                                              0.1) / self.diametral_pitch
                    self.min_minor_ext_dia = min_minor_dia_dict[
                        self.spline_type][self.pressure_angle](
                            self.teeth, self.diametral_pitch)
                elif self.pressure_angle == 45.0:
                    self.max_eff_thickness = (0.5 * pi +
                                              0.2) / self.diametral_pitch
                    self.min_minor_ext_dia = min_minor_dia_dict[
                        self.spline_type][self.pressure_angle](
                            self.teeth, self.diametral_pitch)
                if self.spline_fit == 'SIDE':
                    self.max_major_ext_dia = (self.teeth +
                                              1) / self.diametral_pitch
                    if self.spline_root == 'FLAT':
                        self.min_major_ext_dia = self.max_major_ext_dia - self.dia_tolerance[
                            'FN'](self.diametral_pitch)
                        self.form_ext_dia = max(self.min_form_ext_dia,
                                                self.form_dia)
                    elif self.spline_root == 'FILLET':
                        self.min_major_ext_dia = self.max_major_ext_dia - self.dia_tolerance[
                            'TAB']
                        self.form_ext_dia = max(self.min_form_ext_dia,
                                                self.form_dia)
                elif self.spline_fit == 'DIA':
                    self.max_major_dia_chamfer = .14 / self.diametral_pitch + .006
                    self.min_major_dia_chamfer = .1 / self.diametral_pitch + .002
                    self.form_ext_dia = max(self.min_form_ext_dia,
                                            self.form_dia)
                    self.max_major_ext_dia = (
                        self.teeth + 1) / self.diametral_pitch - 0.0001
                    self.min_major_ext_dia = self.max_major_ext_dia - round(
                        (3 + 2 * self.pitch_dia) * 1e-4, ndigits=4)
                self.min_act_thickness = self.max_eff_thickness - self.total_tolerance
                self.pin_dia = 1.9200 / self.diametral_pitch
            elif self.spline_type == 'INT':
                self.form_dia = form_dia_dict[self.spline_type][
                    self.spline_fit](self.teeth, self.diametral_pitch)
                self.min_minor_int_dia = min_minor_dia_dict[self.spline_type][
                    self.pressure_angle](self.teeth, self.diametral_pitch)
                self.max_minor_int_dia = self.min_minor_int_dia + self.dia_tolerance[
                    'TAB']
                if self.pressure_angle == 30.0:
                    self.pin_dia = 1.7280 / self.diametral_pitch
                    self.min_eff_width = pi / (2 * self.diametral_pitch)
                    if self.spline_root == 'FLAT':
                        if self.spline_fit == 'SIDE':
                            self.max_major_int_dia = (
                                self.teeth +
                                1.35) / self.diametral_pitch + 0.004
                        elif self.spline_fit == 'DIA':
                            self.min_major_int_dia = (self.teeth +
                                                      1) / self.diametral_pitch
                            self.max_major_int_dia = self.min_major_int_dia + round(
                                (10 + 3 * self.pitch_dia) * 1e-4, ndigits=4)
                            self.min_corner_clearance = 0.12 / self.diametral_pitch
                            self.max_corner_clearance = 0.2 / self.diametral_pitch
                    elif self.spline_root == 'FILLET':
                        self.max_major_int_dia = (self.teeth +
                                                  1.8) / self.diametral_pitch
                elif self.pressure_angle == 37.5:
                    self.pin_dia = 1.7280 / self.diametral_pitch
                    self.min_eff_width = (0.5 * pi + .1) / self.diametral_pitch
                    self.max_major_int_dia = (self.teeth +
                                              1.6) / self.diametral_pitch
                elif self.pressure_angle == 45.0:
                    self.pin_dia = 1.9200 / self.diametral_pitch
                    self.max_eff_width = (0.5 * pi + .2) / self.diametral_pitch
                    self.min_major_int_dia = (self.teeth +
                                              1.4) / self.diametral_pitch
                self.max_act_width = self.min_eff_width + self.total_tolerance
            if self.spline_type == 'EXT':
                self.inv_phi_e = self.min_act_thickness / self.pitch_dia + (
                    involute(self.pressure_angle) +
                    self.pin_dia / self.base_dia - pi / self.teeth)
                if self.teeth % 2 == 0:
                    self.min_pin_measurement = self.base_dia / cos(
                        inverse_involute(self.inv_phi_e)) + self.pin_dia
                else:
                    self.min_pin_measurement = self.base_dia / (cos(
                        pi / (2 * self.teeth) *
                        cos(inverse_involute(self.inv_phi_e)))) + self.pin_dia
            elif self.spline_type == 'INT':
                self.inv_phi_i = self.max_act_width / self.pitch_dia + (
                    involute(self.pressure_angle) -
                    self.pin_dia / self.base_dia)
                if self.teeth % 2 == 0:
                    self.max_pin_measurement = self.base_dia / cos(
                        inverse_involute(self.inv_phi_i)) - self.pin_dia
                else:
                    self.max_pin_measurement = self.base_dia / (cos(
                        pi / (2 * self.teeth) *
                        cos(inverse_involute(self.inv_phi_i)))) - self.pin_dia
        elif 'ISO' in self.spec:
            self.spline_type, self.teeth, self.module, self.pressure_angle, tolerance = spec_list
            self.teeth = int(self.teeth[:-1])
            if self.pressure_angle[-1] == 'R': root = 'fillet'
            if self.pressure_angle[-1] == 'P': root = 'flat'
            self.pressure_angle = float(self.pressure_angle[:-1])
            try:
                self.module = float(self.module[:-1])
            except ValueError:
                self.module = float(self.module[:-1].replace(',', '.'))
            tolerance_class = int(tolerance[0])
            fit_class = tolerance[1:]

            self.pitch_dia = self.module * self.teeth
            if self.pitch_dia > 1000:
                raise Exception(
                    'The pitch diameter is out of range of fundamental deviations.'
                )

            self.base_dia = self.pitch_dia * cos(radians(self.pressure_angle))
            circular_pitch = pi * self.module
            base_pitch = circular_pitch * cos(radians(self.pressure_angle))
            if self.spline_type == 'EXT':
                basic_tooth_thickeness = .5 * pi * self.module
                i_E = 0.45 * basic_tooth_thickeness**(
                    1 / 3) + .001 * basic_tooth_thickeness
            elif self.spline_type == 'INT':
                basic_space_width = .5 * pi * self.module
                i_E = 0.45 * basic_space_width**(1 /
                                                 3) + .001 * basic_space_width
            if self.pitch_dia <= 500:
                i_D = 0.45 * self.pitch_dia**(1 / 3) + .001 * self.pitch_dia
            if self.pitch_dia > 500: i_D = 0.004 * self.pitch_dia + 2.1
            arc_length = self.module * self.teeth * pi / 2
            tol_factor = self.module + .0125 * self.module * self.teeth
            cF = .1 * self.module
            if self.length is None: self.length = self.pitch_dia / 2
            if tolerance_class == 7:
                self.tot_space_width_tol = 40 * i_D + 160 * i_E
                pitch_dev = 7.1 * sqrt(arc_length) + 18
                profile_dev = 6.3 * tol_factor + 40
                helix_dev = 2 * sqrt(self.length) + 10
            elif tolerance_class == 6:
                self.tot_space_width_tol = 25 * i_D + 100 * i_E
                pitch_dev = 5 * sqrt(arc_length) + 12.5
                profile_dev = 4 * tol_factor + 25
                helix_dev = 1.25 * sqrt(self.length) + 6.3
            elif tolerance_class == 5:
                self.tot_space_width_tol = 16 * i_D + 64 * i_E
                pitch_dev = 3.55 * sqrt(arc_length) + 9
                profile_dev = 2.5 * tol_factor + 16
                helix_dev = sqrt(self.length) + 5
            elif tolerance_class == 4:
                self.tot_space_width_tol = 10 * i_D + 40 * i_E
                pitch_dev = 2.5 * sqrt(arc_length) + 6.3
                profile_dev = 1.6 * tol_factor + 10
                helix_dev = 0.8 * sqrt(self.length) + 4

            tot_dia_tol = 40 * i_D + 160 * i_E
            dev_allowance = .6 * sqrt(pitch_dev**2 + profile_dev**2 +
                                      helix_dev**2)

            for diameters_range in FUNDAMENTAL_DEVIATIONS:
                if round(self.pitch_dia) in diameters_range:
                    if fit_class in FUNDAMENTAL_DEVIATIONS[diameters_range]:
                        fund_deviation = FUNDAMENTAL_DEVIATIONS[
                            diameters_range][fit_class] * 1e-3
                    else:
                        if fit_class == 'js':
                            FUNDAMENTAL_DEVIATIONS[diameters_range][
                                fit_class] = ceil(self.tot_space_width_tol / 2)
                        elif fit_class == 'k':
                            FUNDAMENTAL_DEVIATIONS[diameters_range][
                                fit_class] = ceil(self.tot_space_width_tol)
                        fund_deviation = FUNDAMENTAL_DEVIATIONS[
                            diameters_range][fit_class] * 1e-3
                    break

            if fit_class in ('js', 'k'):
                fund_deviation_max_major_ext = 0
            else:
                fund_deviation_max_major_ext = fund_deviation

            if self.pressure_angle == 30:
                hs = .6 * self.module
                if self.spline_type == 'EXT':
                    self.max_major_ext_dia = self.module * (
                        self.teeth + 1) + fund_deviation_max_major_ext / tan(
                            radians(self.pressure_angle))
                    if root == 'flat':
                        self.max_minor_ext_dia = self.module * (
                            self.teeth - 1.5) + fund_deviation / tan(
                                radians(self.pressure_angle))
                        self.ext_root_rad = .2 * self.module
                    elif root == 'fillet':
                        self.max_minor_ext_dia = self.module * (
                            self.teeth - 1.8) + fund_deviation / tan(
                                radians(self.pressure_angle))
                        self.ext_root_rad = .4 * self.module
                elif self.spline_type == 'INT':
                    if root == 'flat':
                        self.min_major_int_dia = self.module * (self.teeth +
                                                                1.5)
                        self.int_root_rad = .2 * self.module
                    elif root == 'fillet':
                        self.min_major_int_dia = self.module * (self.teeth +
                                                                1.8)
                        self.int_root_rad = .4 * self.module
            elif self.pressure_angle == 37.5:
                hs = .55 * self.module
                if self.spline_type == 'EXT':
                    self.max_major_ext_dia = self.module * (
                        self.teeth + 0.9) + fund_deviation_max_major_ext / tan(
                            radians(self.pressure_angle))
                    self.max_minor_ext_dia = self.module * (
                        self.teeth - 1.4) + fund_deviation / tan(
                            radians(self.pressure_angle))
                    self.ext_root_rad = .3 * self.module
                elif self.spline_type == 'INT':
                    self.min_major_int_dia = self.module * (self.teeth + 1.4)
                    self.int_root_rad = .3 * self.module
            elif self.pressure_angle == 45:
                hs = .5 * self.module
                if self.spline_type == 'EXT':
                    self.max_major_ext_dia = self.module * (
                        self.teeth + 0.8) + fund_deviation_max_major_ext / tan(
                            radians(self.pressure_angle))
                    self.max_minor_ext_dia = self.module * (
                        self.teeth - 1.2) + fund_deviation / tan(
                            radians(self.pressure_angle))
                    self.ext_root_rad = .25 * self.module
                elif self.spline_type == 'INT':
                    self.min_major_int_dia = self.module * (self.teeth + 1.2)
                    self.int_root_rad = .25 * self.module

            self.max_form_dia = 2 * sqrt(
                (.5 * self.base_dia)**2 +
                (.5 * self.pitch_dia * sin(radians(self.pressure_angle)) -
                 (hs - .5 * fund_deviation / tan(radians(self.pressure_angle))
                  ) / sin(radians(self.pressure_angle)))**2)

            if self.spline_type == 'EXT':
                for diameters_range in MAJOR_MINOR_DIA_TOLERANCES:
                    if round(self.max_major_ext_dia) in diameters_range:
                        if self.module <= 0.75:
                            self.min_major_ext_dia = self.max_major_ext_dia - MAJOR_MINOR_DIA_TOLERANCES[
                                diameters_range][10] * 1e-3
                        elif self.module < 2:
                            self.min_major_ext_dia = self.max_major_ext_dia - MAJOR_MINOR_DIA_TOLERANCES[
                                diameters_range][11] * 1e-3
                        elif self.module >= 2:
                            self.min_major_ext_dia = self.max_major_ext_dia - MAJOR_MINOR_DIA_TOLERANCES[
                                diameters_range][12] * 1e-3
                        break

                self.min_minor_ext_dia = self.max_minor_ext_dia - tot_dia_tol * 1e-3 / tan(
                    radians(self.pressure_angle))
                self.max_eff_thickness = basic_tooth_thickeness + fund_deviation
                self.max_act_thickness = self.max_eff_thickness - dev_allowance * 1e-3
                self.min_act_thickness = self.max_eff_thickness - self.tot_space_width_tol * 1e-3
                self.min_eff_thickness = self.min_act_thickness + dev_allowance * 1e-3
                DEe = base_pitch - (
                    basic_tooth_thickeness * cos(radians(self.pressure_angle))
                    + self.base_dia * involute(self.pressure_angle))
                BAarc = self.base_dia * tan(radians(self.pressure_angle)) / 2
                BOe = self.base_dia * tan(
                    radians(self.pressure_angle) +
                    involute(self.pressure_angle) + DEe / self.base_dia) / 2
                self.ext_pin_dia = find_greater_than_or_equal(
                    R40, 2 * (BOe - BAarc))
                inv_alphaEmax = self.max_act_thickness / self.pitch_dia + (
                    involute(self.pressure_angle) +
                    self.ext_pin_dia / self.base_dia - pi / self.teeth)
                alphaEmax = degrees(inverse_involute(inv_alphaEmax))
                self.max_ext_measurement = self.base_dia / cos(
                    radians(alphaEmax)
                ) + self.ext_pin_dia if self.teeth // 2 else self.base_dia * cos(
                    radians(90 / self.teeth)) / cos(
                        radians(alphaEmax)) + self.ext_pin_dia
                inv_alphaEmin = self.min_act_thickness / self.pitch_dia + (
                    involute(self.pressure_angle) +
                    self.ext_pin_dia / self.base_dia - pi / self.teeth)
                alphaEmin = degrees(inverse_involute(inv_alphaEmin))
                self.min_ext_measurement = self.base_dia / cos(
                    radians(alphaEmin)
                ) + self.ext_pin_dia if self.teeth // 2 else self.base_dia * cos(
                    radians(90 / self.teeth)) / cos(
                        radians(alphaEmin)) + self.ext_pin_dia
            elif self.spline_type == 'INT':
                self.min_form_int_dia = self.module * (self.teeth + 1) + 2 * cF
                self.min_minor_int_dia = self.max_form_dia + 2 * cF
                for diameters_range in MAJOR_MINOR_DIA_TOLERANCES:
                    if round(self.min_minor_int_dia) in diameters_range:
                        if self.module <= 0.75:
                            self.max_minor_int_dia = self.min_minor_int_dia + MAJOR_MINOR_DIA_TOLERANCES[
                                diameters_range][10] * 1e-3
                        elif self.module < 2:
                            self.max_minor_int_dia = self.min_minor_int_dia + MAJOR_MINOR_DIA_TOLERANCES[
                                diameters_range][11] * 1e-3
                        elif self.module >= 2:
                            self.max_minor_int_dia = self.min_minor_int_dia + MAJOR_MINOR_DIA_TOLERANCES[
                                diameters_range][12] * 1e-3
                        break

                self.max_major_int_dia = self.min_major_int_dia + tot_dia_tol * 1e-3 / tan(
                    radians(self.pressure_angle))
                self.min_eff_width = basic_space_width
                self.max_act_width = self.min_eff_width + self.tot_space_width_tol * 1e-3
                self.min_act_width = self.min_eff_width + dev_allowance * 1e-3
                self.max_eff_width = self.max_act_width - dev_allowance * 1e-3
                DEi = basic_space_width * cos(radians(
                    self.pressure_angle)) + self.base_dia * involute(
                        self.pressure_angle)
                BAarc = self.base_dia * tan(radians(self.pressure_angle)) / 2
                BOi = self.base_dia * tan(
                    radians(self.pressure_angle) +
                    involute(self.pressure_angle) - DEi / self.base_dia) / 2
                self.int_pin_dia = find_greater_than_or_equal(
                    R40, 2 * (BAarc - BOi))
                inv_alphaImax = self.max_act_width / self.pitch_dia + (
                    involute(self.pressure_angle) -
                    self.int_pin_dia / self.base_dia)
                alphaImax = degrees(inverse_involute(inv_alphaImax))
                self.max_int_measurement = self.base_dia / cos(
                    radians(alphaImax)
                ) - self.int_pin_dia if self.teeth // 2 else self.base_dia * cos(
                    radians(90 / self.teeth)) / cos(
                        radians(alphaImax)) - self.int_pin_dia
                inv_alphaImin = self.min_act_width / self.pitch_dia + (
                    involute(self.pressure_angle) -
                    self.int_pin_dia / self.base_dia)
                alphaImin = degrees(inverse_involute(inv_alphaImin))
                self.min_int_measurement = self.base_dia / cos(
                    radians(alphaImin)
                ) - self.int_pin_dia if self.teeth // 2 else self.base_dia * cos(
                    radians(90 / self.teeth)) / cos(
                        radians(alphaImin)) - self.int_pin_dia
        elif 'BS' in self.spec:
            self.spline_type, self.spline_root, self.spline_fit, self.diametral_pitch, self.stub_pitch, self.teeth, self.pressure_angle = spec_list
            self.diametral_pitch = float(self.diametral_pitch)
            self.pressure_angle = float(self.pressure_angle)
            self.teeth = int(self.teeth)
            self.stub_pitch = float(self.stub_pitch)

    def print_drawing_data(self, units):
        """Prints out the drawing data according to section 12.4 in ISO 4156:1-2001"""
        if 'ISO' in self.spec:
            if units == 'metric':
                units_coef = 1
            elif units == 'imperial':
                units_coef = 1 / 25.4
            if self.spline_type == 'INT':
                print(
                    f'{self.spec}',
                    f'Number of teeth {self.teeth}',
                    f'Module {round(self.module, ndigits=2)}',
                    f'Pressure angle {round(self.pressure_angle, ndigits=1)}',
                    f'Pitch diameter {round(self.pitch_dia*units_coef, ndigits=4)}',
                    f'Base diameter {round(self.base_dia*units_coef, ndigits=4)}',
                    f'Min major diameter {round(self.min_major_int_dia*units_coef, ndigits=3)}',
                    f'Max major diameter {round(self.max_major_int_dia*units_coef, ndigits=3)}',
                    f'Min form diameter {round(self.min_form_int_dia*units_coef, ndigits=3)}',
                    f'Min minor diameter {round(self.min_minor_int_dia*units_coef, ndigits=3)}',
                    f'Max minor diameter {round(self.max_minor_int_dia*units_coef, ndigits=3)}',
                    f'Max actual space width {round(self.max_act_width*units_coef, ndigits=3)}',
                    f'Max effective space width {round(self.max_eff_width*units_coef, ndigits=3)}',
                    f'Min actual space width {round(self.min_act_width*units_coef, ndigits=3)}',
                    f'Min effective space width {round(self.min_eff_width*units_coef, ndigits=3)}',
                    f'Max measurement over pins {round(self.max_int_measurement*units_coef, ndigits=3)}',
                    f'Min measurement over pins {round(self.min_int_measurement*units_coef, ndigits=3)}',
                    f'Pin diameter {round(self.int_pin_dia*units_coef, ndigits=3)}',
                    f'Fillet radius {round(self.int_root_rad*units_coef, ndigits=1)}\n',
                    sep='\n')
            elif self.spline_type == 'EXT':
                print(
                    f'{self.spec}',
                    f'Number of teeth {self.teeth}',
                    f'Module {round(self.module, ndigits=2)}',
                    f'Pressure angle {round(self.pressure_angle, ndigits=1)}',
                    f'Pitch diameter {round(self.pitch_dia*units_coef, ndigits=4)}',
                    f'Base diameter {round(self.base_dia*units_coef, ndigits=4)}',
                    f'Max major diameter {round(self.max_major_ext_dia*units_coef, ndigits=4)}',
                    f'Min major diameter {round(self.min_major_ext_dia*units_coef, ndigits=4)}',
                    f'Max form diameter {round(self.max_form_dia*units_coef, ndigits=3)}',
                    f'Min minor diameter {round(self.min_minor_ext_dia*units_coef, ndigits=3)}',
                    f'Max minor diameter {round(self.max_minor_ext_dia*units_coef, ndigits=3)}',
                    f'Max effective tooth thickness {round(self.max_eff_thickness*units_coef, ndigits=3)}',
                    f'Max actual tooth thickness {round(self.max_act_thickness*units_coef, ndigits=3)}',
                    f'Min effective tooth thickness {round(self.min_eff_thickness*units_coef, ndigits=3)}',
                    f'Min actual tooth thickness {round(self.min_act_thickness*units_coef, ndigits=3)}',
                    f'Max measurement over pins {round(self.max_ext_measurement*units_coef, ndigits=3)}',
                    f'Min measurement over pins {round(self.min_ext_measurement*units_coef, ndigits=3)}',
                    f'Pin diameter {round(self.ext_pin_dia, ndigits=3)}',
                    f'Fillet radius {round(self.ext_root_rad, ndigits=1)}\n',
                    sep='\n')
        elif 'ANSI' in self.spec:
            if units == 'metric':
                units_coef = 25.4
            elif units == 'imperial':
                units_coef = 1

            if self.spline_type == 'INT':
                print(
                    f'{self.spec}',
                    f'Number of teeth {self.teeth}',
                    f'Pitch {self.diametral_pitch}/{self.stub_pitch}',
                    f'Pressure angle {round(self.pressure_angle, ndigits=1)}',
                    f'Base diameter {round(self.base_dia*units_coef, ndigits=6)}',
                    f'Pitch diameter {round(self.pitch_dia*units_coef, ndigits=6)}',
                    f'Max major diameter {round(self.max_major_int_dia*units_coef, ndigits=4)}',
                    f'Min major diameter {round(self.min_major_int_dia*units_coef, ndigits=4)}',
                    f'Form diameter {round(self.form_dia*units_coef, ndigits=3)}',
                    f'Min minor diameter {round(self.min_minor_int_dia*units_coef, ndigits=4)}',
                    f'Max minor diameter {round(self.max_minor_int_dia*units_coef, ndigits=4)}',
                    f'Max actual space width {round(self.max_act_width*units_coef, ndigits=4)}',
                    # f'Max effective space width {round(max_eff_width, ndigits=4)}',
                    # f'Min actual space width {round(min_act_width, ndigits=4)}',
                    f'Min effective space width {round(self.min_eff_width*units_coef, ndigits=4)}',
                    f'Max measurement between pins {round(self.max_pin_measurement*units_coef, ndigits=4)}',
                    # f'Min measurement over pins {round(min_int_measurement, ndigits=3)}',
                    f'Pin diameter {round(self.pin_dia*units_coef, ndigits=4)}',
                    # f'Fillet radius {round(int_root_rad, ndigits=1)}\n',
                    sep='\n')
                if self.spline_fit == 'DIA':
                    print(
                        f'Max corner clearance {round(self.max_corner_clearance*units_coef, ndigits=3)}',
                        f'Min corner clearance {round(self.min_corner_clearance*units_coef, ndigits=3)}\n',
                        sep='\n')

            elif self.spline_type == 'EXT':
                print(
                    f'{self.spec}',
                    f'Number of teeth {self.teeth}',
                    f'Pitch {self.diametral_pitch}/{self.stub_pitch}',
                    f'Pressure angle {round(self.pressure_angle, ndigits=1)}',
                    f'Base diameter {round(self.base_dia*units_coef, ndigits=6)}',
                    f'Pitch diameter {round(self.pitch_dia*units_coef, ndigits=6)}',
                    f'Min major diameter {round(self.min_major_ext_dia*units_coef, ndigits=4)}',
                    f'Max major diameter {round(self.max_major_ext_dia*units_coef, ndigits=4)}',
                    f'Form diameter {round(self.form_dia*units_coef, ndigits=3)}',
                    f'Min minor diameter {round(self.min_minor_ext_dia*units_coef, ndigits=3)}',
                    # f'Max minor diameter {round(max_minor_ext_dia, ndigits=3)}',
                    f'Max effective tooth thickness {round(self.max_eff_thickness*units_coef, ndigits=4)}',
                    # f'Max actual tooth thickness {round(max_act_thickness, ndigits=4)}',
                    # f'Min effective tooth thickness {round(min_eff_thickness, ndigits=4)}',
                    f'Min actual tooth thickness {round(self.min_act_thickness*units_coef, ndigits=4)}',
                    # f'Max measurement over pins {round(max_ext_measurement, ndigits=3)}',
                    f'Min measurement over pins {round(self.min_pin_measurement*units_coef, ndigits=4)}',
                    f'Pin diameter {round(self.pin_dia*units_coef, ndigits=4)}',
                    # f'Fillet radius {round(ext_root_rad, ndigits=1)}\n',
                    sep='\n')
                if self.spline_fit == 'DIA':
                    print(
                        f'Max chamfer height {round(self.max_major_dia_chamfer*units_coef, ndigits=3)}',
                        f'Min chamfer height {round(self.min_major_dia_chamfer*units_coef, ndigits=3)}\n',
                        sep='\n')