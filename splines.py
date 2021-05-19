from math import ceil, cos, sin, tan, pi, radians, sqrt, degrees
from renard import R40, find_greater_than_or_equal

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


class Splines:
    """
    A splines class

    Attributes
    ----------
    spec: str
        A formatted string according to the desgnation section in section 12.3 ISO 4156-1:2005.
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
        """Calculates the sizes according to the methodology in ISO 4156:1-2001, stores the key sizes in the class attributes."""
        spec_list = [
            i for i in self.spec.split() if i not in ('x', '-', 'ISO', '4156')
        ]
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
            i_E = 0.45 * basic_space_width**(1 / 3) + .001 * basic_space_width
        if self.pitch_dia <= 500:
            i_D = 0.45 * self.pitch_dia**(1 / 3) + .001 * self.pitch_dia
        if self.pitch_dia > 500: i_D = 0.004 * self.pitch_dia + 2.1
        arc_length = self.module * self.teeth * pi / 2
        tol_factor = self.module + .0125 * self.module * self.teeth
        cF = .1 * self.module

        involute = lambda alpha: tan(radians(alpha)) - pi * alpha / 180
        inverse_involute = lambda x: x**(1 / 3) / (.693357 + .192484 * x**
                                                   (2 / 3))

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
        dev_allowance = .6 * sqrt(pitch_dev**2 + profile_dev**2 + helix_dev**2)

        for diameters_range in FUNDAMENTAL_DEVIATIONS:
            if round(self.pitch_dia) in diameters_range:
                if fit_class in FUNDAMENTAL_DEVIATIONS[diameters_range]:
                    fund_deviation = FUNDAMENTAL_DEVIATIONS[diameters_range][
                        fit_class] * 1e-3
                else:
                    if fit_class == 'js':
                        FUNDAMENTAL_DEVIATIONS[diameters_range][
                            fit_class] = ceil(self.tot_space_width_tol / 2)
                    elif fit_class == 'k':
                        FUNDAMENTAL_DEVIATIONS[diameters_range][
                            fit_class] = ceil(self.tot_space_width_tol)
                    fund_deviation = FUNDAMENTAL_DEVIATIONS[diameters_range][
                        fit_class] * 1e-3
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
                    max_minor_ext_dia = self.module * (
                        self.teeth - 1.5) + fund_deviation / tan(
                            radians(self.pressure_angle))
                    self.ext_root_rad = .2 * self.module
                elif root == 'fillet':
                    max_minor_ext_dia = self.module * (
                        self.teeth - 1.8) + fund_deviation / tan(
                            radians(self.pressure_angle))
                    self.ext_root_rad = .4 * self.module
            elif self.spline_type == 'INT':
                if root == 'flat':
                    min_major_int_dia = self.module * (self.teeth + 1.5)
                    self.int_root_rad = .2 * self.module
                elif root == 'fillet':
                    min_major_int_dia = self.module * (self.teeth + 1.8)
                    self.int_root_rad = .4 * self.module
        elif self.pressure_angle == 37.5:
            hs = .55 * self.module
            if self.spline_type == 'EXT':
                self.max_major_ext_dia = self.module * (
                    self.teeth + 0.9) + fund_deviation_max_major_ext / tan(
                        radians(self.pressure_angle))
                max_minor_ext_dia = self.module * (
                    self.teeth - 1.4) + fund_deviation / tan(
                        radians(self.pressure_angle))
                self.ext_root_rad = .3 * self.module
            elif self.spline_type == 'INT':
                min_major_int_dia = self.module * (self.teeth + 1.4)
                self.int_root_rad = .3 * self.module
        elif self.pressure_angle == 45:
            hs = .5 * self.module
            if self.spline_type == 'EXT':
                self.max_major_ext_dia = self.module * (
                    self.teeth + 0.8) + fund_deviation_max_major_ext / tan(
                        radians(self.pressure_angle))
                max_minor_ext_dia = self.module * (
                    self.teeth - 1.2) + fund_deviation / tan(
                        radians(self.pressure_angle))
                self.ext_root_rad = .25 * self.module
            elif self.spline_type == 'INT':
                min_major_int_dia = self.module * (self.teeth + 1.2)
                self.int_root_rad = .25 * self.module

        self.max_form_ext_dia = 2 * sqrt(
            (.5 * self.base_dia)**2 +
            (.5 * self.pitch_dia * sin(radians(self.pressure_angle)) -
             (hs - .5 * fund_deviation / tan(radians(self.pressure_angle))) /
             sin(radians(self.pressure_angle)))**2)

        if self.spline_type == 'EXT':
            self.min_minor_ext_dia = max_minor_ext_dia - tot_dia_tol * 1e-3 / tan(
                radians(self.pressure_angle))
            self.max_eff_thickness = basic_tooth_thickeness + fund_deviation
            self.max_act_thickness = self.max_eff_thickness - dev_allowance * 1e-3
            self.min_act_thickness = self.max_eff_thickness - self.tot_space_width_tol * 1e-3
            self.min_eff_thickness = self.min_act_thickness + dev_allowance * 1e-3
            DEe = base_pitch - (
                basic_tooth_thickeness * cos(radians(self.pressure_angle)) +
                self.base_dia * involute(self.pressure_angle))
            BAarc = self.base_dia * tan(radians(self.pressure_angle)) / 2
            BOe = self.base_dia * tan(
                radians(self.pressure_angle) + involute(self.pressure_angle) +
                DEe / self.base_dia) / 2
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
            self.min_minor_int_dia = self.max_form_ext_dia + 2 * cF
            self.max_major_int_dia = min_major_int_dia + tot_dia_tol * 1e-3 / tan(
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
                radians(self.pressure_angle) + involute(self.pressure_angle) -
                DEi / self.base_dia) / 2
            self.int_pin_dia = find_greater_than_or_equal(
                R40, 2 * (BAarc - BOi))
            inv_alphaImax = self.max_act_width / self.pitch_dia + (involute(
                self.pressure_angle) - self.int_pin_dia / self.base_dia)
            alphaImax = degrees(inverse_involute(inv_alphaImax))
            self.max_int_measurement = self.base_dia / cos(
                radians(alphaImax)
            ) - self.int_pin_dia if self.teeth // 2 else self.base_dia * cos(
                radians(90 / self.teeth)) / cos(
                    radians(alphaImax)) - self.int_pin_dia
            inv_alphaImin = self.min_act_width / self.pitch_dia + (involute(
                self.pressure_angle) - self.int_pin_dia / self.base_dia)
            alphaImin = degrees(inverse_involute(inv_alphaImin))
            self.min_int_measurement = self.base_dia / cos(
                radians(alphaImin)
            ) - self.int_pin_dia if self.teeth // 2 else self.base_dia * cos(
                radians(90 / self.teeth)) / cos(
                    radians(alphaImin)) - self.int_pin_dia

    def print_drawing_data(self):
        """Prints out the drawing data according to section 12.4 in ISO 4156:1-2001"""
        if self.spline_type == 'INT':
            print(
                f'{self.spec}',
                f'Number of teeth {self.teeth}',
                f'Module {round(self.module, ndigits=2)}',
                f'Pressure angle {round(self.pressure_angle, ndigits=1)}',
                f'Pitch diameter {round(self.pitch_dia, ndigits=4)}',
                f'Base diameter {round(self.base_dia, ndigits=4)}',
                f'Major diameter {round(self.max_major_int_dia, ndigits=2)}',
                f'Form diameter {round(self.min_form_int_dia, ndigits=2)}',
                f'Minor diameter {round(self.min_minor_int_dia, ndigits=2)}',
                f'Max actual space width {round(self.max_act_width, ndigits=3)}',
                f'Max effective space width {round(self.max_eff_width, ndigits=3)}',
                f'Min actual space width {round(self.min_act_width, ndigits=3)}',
                f'Min effective space width {round(self.min_eff_width, ndigits=3)}',
                f'Max measurement over pins {round(self.max_int_measurement, ndigits=3)}',
                f'Min measurement over pins {round(self.min_int_measurement, ndigits=3)}',
                f'Pin diameter {round(self.int_pin_dia, ndigits=3)}',
                f'Fillet radius {round(self.int_root_rad, ndigits=1)}\n',
                sep='\n')
        elif self.spline_type == 'EXT':
            print(
                f'{self.spec}',
                f'Number of teeth {self.teeth}',
                f'Module {round(self.module, ndigits=2)}',
                f'Pressure angle {round(self.pressure_angle, ndigits=1)}',
                f'Pitch diameter {round(self.pitch_dia, ndigits=4)}',
                f'Base diameter {round(self.base_dia, ndigits=4)}',
                f'Major diameter {round(self.max_major_ext_dia, ndigits=2)}',
                f'Form diameter {round(self.max_form_ext_dia, ndigits=2)}',
                f'Minor diameter {round(self.min_minor_ext_dia, ndigits=2)}',
                f'Max effective tooth thickness {round(self.max_eff_thickness, ndigits=3)}',
                f'Max actual tooth thickness {round(self.max_act_thickness, ndigits=3)}',
                f'Min effective tooth thickness {round(self.min_eff_thickness, ndigits=3)}',
                f'Min actual tooth thickness {round(self.min_act_thickness, ndigits=3)}',
                f'Max measurement over pins {round(self.max_ext_measurement, ndigits=3)}',
                f'Min measurement over pins {round(self.min_ext_measurement, ndigits=3)}',
                f'Pin diameter {round(self.ext_pin_dia, ndigits=3)}',
                f'Fillet radius {round(self.ext_root_rad, ndigits=1)}\n',
                sep='\n')