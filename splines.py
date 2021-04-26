from math import cos, sin, tan, pi, radians, sqrt, degrees
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
    range(11, 18): {
        'd': -50,
        'e': -32,
        'f': -16,
        'h': 0,
        'H': 0,
    },
    range(19, 30): {
        'd': -65,
        'e': -40,
        'f': -20,
        'h': 0,
        'H': 0,
    },
    range(31, 50): {
        'd': -80,
        'e': -50,
        'f': -25,
        'h': 0,
        'H': 0,
    },
    range(51, 80): {
        'd': -100,
        'e': -60,
        'f': -30,
        'h': 0,
        'H': 0,
    },
    range(81, 120): {
        'd': -120,
        'e': -72,
        'f': -36,
        'h': 0,
        'H': 0,
    },
    range(121, 180): {
        'd': -145,
        'e': -85,
        'f': -43,
        'h': 0,
        'H': 0,
    },
    range(181, 250): {
        'd': -170,
        'e': -100,
        'f': -50,
        'h': 0,
        'H': 0,
    },
}


def calculate_spline_sizes(spec, length):
    spec_list = [i for i in spec.split() if i != 'x']
    spline, teeth, module, pressure_angle, tolerance = spec_list
    teeth = int(teeth[:-1])
    if pressure_angle[-1] == 'R': root = 'fillet'
    if pressure_angle[-1] == 'P': root = 'flat'
    pressure_angle = float(pressure_angle[:-1])
    module = float(module[:-1])
    tooth_space_tolerance_grade = int(tolerance[0])
    tolerance_class = tolerance[1]

    pitch_dia = module * teeth
    base_dia = pitch_dia * cos(radians(pressure_angle))
    circular_pitch = pi * module
    base_pitch = circular_pitch * cos(radians(pressure_angle))
    if spline == 'EXT':
        basic_tooth_thickeness = .5 * pi * module
        i_E = 0.45 * basic_tooth_thickeness**(
            1 / 3) + .001 * basic_tooth_thickeness
    elif spline == 'INT':
        basic_space_width = .5 * pi * module
        i_E = 0.45 * basic_space_width**(1 / 3) + .001 * basic_space_width
    i_D = 0.45 * pitch_dia**(1 / 3) + .001 * pitch_dia
    arc_length = module * teeth * pi / 2
    tol_factor = module + .0125 * module * teeth
    cF = .1 * module

    involute = lambda alpha: tan(radians(alpha)) - pi * alpha / 180
    inverse_involute = lambda x: x**(1 / 3) / (.693357 + .192484 * x**(2 / 3))

    for diameters_range in FUNDAMENTAL_DEVIATIONS:
        if round(pitch_dia) in diameters_range:
            if tolerance_class in FUNDAMENTAL_DEVIATIONS[diameters_range]:
                fund_deviation = FUNDAMENTAL_DEVIATIONS[diameters_range][
                    tolerance_class] * 1e-3
                break

    if tooth_space_tolerance_grade == 7:
        tot_space_width_tol = 40 * i_D + 160 * i_E
        pitch_dev = 7.1 * sqrt(arc_length) + 18
        profile_dev = 6.3 * tol_factor + 40
        helix_dev = 2 * sqrt(length) + 10
    elif tooth_space_tolerance_grade == 6:
        tot_space_width_tol = 25 * i_D + 100 * i_E
        pitch_dev = 5 * sqrt(arc_length) + 12.5
        profile_dev = 4 * tol_factor + 25
        helix_dev = 1.25 * sqrt(length) + 6.3
    elif tooth_space_tolerance_grade == 5:
        tot_space_width_tol = 16 * i_D + 64 * i_E
        pitch_dev = 3.55 * sqrt(arc_length) + 9
        profile_dev = 2.5 * tol_factor + 16
        helix_dev = sqrt(length) + 5
    elif tooth_space_tolerance_grade == 4:
        tot_space_width_tol = 10 * i_D + 40 * i_E
        pitch_dev = 2.5 * sqrt(arc_length) + 6.3
        profile_dev = 1.6 * tol_factor + 10
        helix_dev = 0.8 * sqrt(length) + 4

    tot_dia_tol = 40 * i_D + 160 * i_E
    dev_allowance = .6 * sqrt(pitch_dev**2 + profile_dev**2 + helix_dev**2)

    if pressure_angle == 30:
        hs = .6 * module
        if spline == 'EXT':
            max_major_ext_dia = module * (teeth + 1) + fund_deviation / tan(
                radians(pressure_angle))
            if root == 'flat':
                max_minor_ext_dia = module * (teeth -
                                              1.5) + fund_deviation / tan(
                                                  radians(pressure_angle))
                ext_root_rad = .2 * module
            elif root == 'fillet':
                max_minor_ext_dia = module * (teeth -
                                              1.8) + fund_deviation / tan(
                                                  radians(pressure_angle))
                ext_root_rad = .4 * module
        elif spline == 'INT':
            if root == 'flat':
                min_major_int_dia = module * (teeth + 1.5)
                int_root_rad = .2 * module
            elif root == 'fillet':
                min_major_int_dia = module * (teeth + 1.8)
                int_root_rad = .4 * module
    elif pressure_angle == 37.5:
        hs = .55 * module
        if spline == 'EXT':
            max_major_ext_dia = module * (teeth + 0.9) + fund_deviation / tan(
                radians(pressure_angle))
            max_minor_ext_dia = module * (teeth - 1.4) + fund_deviation / tan(
                radians(pressure_angle))
            ext_root_rad = .3 * module
        elif spline == 'INT':
            min_major_int_dia = module * (teeth + 1.4)
            int_root_rad = .3 * module
    elif pressure_angle == 45:
        hs = .5 * module
        if spline == 'EXT':
            max_major_ext_dia = module * (teeth + 0.8) + fund_deviation / tan(
                radians(pressure_angle))
            max_minor_ext_dia = module * (teeth - 1.2) + fund_deviation / tan(
                radians(pressure_angle))
            ext_root_rad = .25 * module
        elif spline == 'INT':
            min_major_int_dia = module * (teeth + 1.2)
            int_root_rad = .25 * module

    max_form_ext_dia = 2 * sqrt(
        (.5 * base_dia)**2 +
        (.5 * pitch_dia * sin(radians(pressure_angle)) -
         (hs - .5 * fund_deviation / tan(radians(pressure_angle))) /
         sin(radians(pressure_angle)))**2)

    if spline == 'EXT':
        min_minor_ext_dia = max_minor_ext_dia - tot_dia_tol * 1e-3 / tan(
            radians(pressure_angle))
        max_eff_thickness = basic_tooth_thickeness + fund_deviation
        max_act_thickness = max_eff_thickness - dev_allowance * 1e-3
        min_act_thickness = max_eff_thickness - tot_space_width_tol * 1e-3
        min_eff_thickness = min_act_thickness + dev_allowance * 1e-3
        DEe = base_pitch - (
            basic_tooth_thickeness * cos(radians(pressure_angle)) +
            base_dia * involute(pressure_angle))
        BAarc = base_dia * tan(radians(pressure_angle)) / 2
        BOe = base_dia * tan(
            radians(pressure_angle) + involute(pressure_angle) +
            DEe / base_dia) / 2
        ext_pin_dia = find_greater_than_or_equal(R40, 2 * (BOe - BAarc))
        inv_alphaEmax = max_act_thickness / pitch_dia + (
            involute(pressure_angle) + ext_pin_dia / base_dia - pi / teeth)
        alphaEmax = degrees(inverse_involute(inv_alphaEmax))
        max_ext_measurement = base_dia / cos(radians(
            alphaEmax)) + ext_pin_dia if teeth // 2 else base_dia * cos(
                radians(90 / teeth)) / cos(radians(alphaEmax)) + ext_pin_dia
        inv_alphaEmin = min_act_thickness / pitch_dia + (
            involute(pressure_angle) + ext_pin_dia / base_dia - pi / teeth)
        alphaEmin = degrees(inverse_involute(inv_alphaEmin))
        min_ext_measurement = base_dia / cos(radians(
            alphaEmin)) + ext_pin_dia if teeth // 2 else base_dia * cos(
                radians(90 / teeth)) / cos(radians(alphaEmin)) + ext_pin_dia
        print(
            f'{spec}',
            f'Number of teeth {teeth}',
            f'Module {round(module, ndigits=2)}',
            f'Pressure angle {round(pressure_angle, ndigits=1)}',
            f'Pitch diameter {round(pitch_dia, ndigits=4)}',
            f'Base diameter {round(base_dia, ndigits=4)}',
            f'Major diameter {round(max_major_ext_dia, ndigits=2)}',
            f'Form diameter {round(max_form_ext_dia, ndigits=2)}',
            f'Minor diameter {round(min_minor_ext_dia, ndigits=2)}',
            f'Max effective tooth thickness {round(max_eff_thickness, ndigits=3)}',
            f'Max actual tooth thickness {round(max_act_thickness, ndigits=3)}',
            f'Min effective tooth thickness {round(min_eff_thickness, ndigits=3)}',
            f'Min actual tooth thickness {round(min_act_thickness, ndigits=3)}',
            f'Max measurement over pins {round(max_ext_measurement, ndigits=3)}',
            f'Min measurement over pins {round(min_ext_measurement, ndigits=3)}',
            f'Pin diameter {round(ext_pin_dia, ndigits=3)}',
            f'Fillet radius {round(ext_root_rad, ndigits=1)}\n',
            sep='\n')
    elif spline == 'INT':
        min_form_int_dia = module * (teeth + 1) + 2 * cF
        min_minor_int_dia = max_form_ext_dia + 2 * cF
        max_major_int_dia = min_major_int_dia + tot_dia_tol * 1e-3 / tan(
            radians(pressure_angle))
        min_eff_width = basic_space_width
        max_act_width = min_eff_width + tot_space_width_tol * 1e-3
        min_act_width = min_eff_width + dev_allowance * 1e-3
        max_eff_width = max_act_width - dev_allowance * 1e-3
        DEi = basic_space_width * cos(
            radians(pressure_angle)) + base_dia * involute(pressure_angle)
        BAarc = base_dia * tan(radians(pressure_angle)) / 2
        BOi = base_dia * tan(
            radians(pressure_angle) + involute(pressure_angle) -
            DEi / base_dia) / 2
        int_pin_dia = find_greater_than_or_equal(R40, 2 * (BAarc - BOi))
        inv_alphaImax = max_act_width / pitch_dia + (involute(pressure_angle) -
                                                     int_pin_dia / base_dia)
        alphaImax = degrees(inverse_involute(inv_alphaImax))
        max_int_measurement = base_dia / cos(radians(
            alphaImax)) - int_pin_dia if teeth // 2 else base_dia * cos(
                radians(90 / teeth)) / cos(radians(alphaImax)) - int_pin_dia
        inv_alphaImin = min_act_width / pitch_dia + (involute(pressure_angle) -
                                                     int_pin_dia / base_dia)
        alphaImin = degrees(inverse_involute(inv_alphaImin))
        min_int_measurement = base_dia / cos(radians(
            alphaImin)) - int_pin_dia if teeth // 2 else base_dia * cos(
                radians(90 / teeth)) / cos(radians(alphaImin)) - int_pin_dia
        print(
            f'{spec}',
            f'Number of teeth {teeth}',
            f'Module {round(module, ndigits=2)}',
            f'Pressure angle {round(pressure_angle, ndigits=1)}',
            f'Pitch diameter {round(pitch_dia, ndigits=4)}',
            f'Base diameter {round(base_dia, ndigits=4)}',
            f'Major diameter {round(max_major_int_dia, ndigits=2)}',
            f'Form diameter {round(min_form_int_dia, ndigits=2)}',
            f'Minor diameter {round(min_minor_int_dia, ndigits=2)}',
            f'Max actual space width {round(max_act_width, ndigits=3)}',
            f'Max effective space width {round(max_eff_width, ndigits=3)}',
            f'Min actual space width {round(min_act_width, ndigits=3)}',
            f'Min effective space width {round(min_eff_width, ndigits=3)}',
            f'Max measurement over pins {round(max_int_measurement, ndigits=3)}',
            f'Min measurement over pins {round(min_int_measurement, ndigits=3)}',
            f'Pin diameter {round(int_pin_dia, ndigits=3)}',
            f'Fillet radius {round(int_root_rad, ndigits=1)}\n',
            sep='\n')