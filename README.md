# Splines

## Outline
The repository contains the `splines` and `test_splines` modules. The former is the splines calculator, which uses the sizes calculation methodology described in ISO 4156-1:2005 and ANSI B92. The `splines` introduces the `Splines` class with methods to calculate and print out the key sizes of internal and external splines according to ISO 4156-2:2001 and ANSI B92. 

## Usage
The `Splines` class is initiated with the string-like spline specification in the format according to either the section 12.3 of ISO 4156-1:2001 or ANSI B92 and the splines length. If not specified, the default length is computed as half pitch diameter. 

## Example
The example of the input for the external spline calculation would look like: `'EXT 24z x 2,5m x 30R x 5f - ISO 4156'`. The `print_drawing_data` method lists the data required for the uniform spline specification on drawings of the spined components according to the section 12.4 in ISO 4156-1:2001. The `test_splines` implements the tests of the calculations module by asserting compliance between the sizes computed with the `splines` module and the sizing calculation examples in appendices to ISO 4156-1:2005.

### ISO splines
```
iso_splines = Splines('EXT 24z x 2,5m x 30R x 5f - ISO 4156', None)
iso_splines.print_drawing_data()
```

### ANSI splines
```
ansi_splines = Splines('EXT FLAT ROOT SIDE FIT 12/24 30T 30 CLASS 5 ANSI B92', None)
ansi_splines.print_drawing_data()
```