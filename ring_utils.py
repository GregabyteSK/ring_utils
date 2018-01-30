#Ring calculator

from math import pi
from fractions import Fraction

awg_gauge = { #AWG to inches
            0:0.3249,
            1:0.2893,
            2:0.2576,
            3:0.2294,
            4:0.2043,
            5:0.1819,
            6:0.162,
            7:0.1443,
            8:0.1285,
            9:0.1144,
            10:0.1019,
            11:0.0907,
            12:0.0808,
            13:0.072,
            14:0.0641,
            15:0.0571,
            16:0.0508,
            17:0.0453,
            18:0.0403,
            19:0.0359,
            20:0.032,
            21:0.0285,
            22:0.0254,
            23:0.0226,
            24:0.0201,
            25:0.0179,
            26:0.0159,
            27:0.0142,
            28:0.0126,
            29:0.0113,
            30:0.01,
            31:0.0089,
            32:0.008 }

#density in lbs/in^3
al_wire_density = { 0:0.1, #Default, pure AL
                    5356:0.0954}

#Average of inner and outer diameter
def middle_diameter(gauge, inner_diameter = None, outer_diameter = None):
    if inner_diameter and outer_diameter:
        return (inner_diameter + outer_diameter) / 2
    if inner_diameter:
        return inner_diameter + awg_gauge[gauge]
    if outer_diameter:
        return outer_diameter - awg_gauge[gauge]

def circumference(gauge, inner_diameter = None, outer_diameter = None):
    return 2 * pi * (middle_diameter(inner_diameter = inner_diameter, outer_diameter = outer_diameter, gauge = gauge) / 2)

#Calculates how many rings can be gotten out of a spool of wire
def spool(length, gauge, ring_size):
    if type(ring_size) == str:
        ring_size = float(sum(Fraction(s) for s in ring_size.split()))
    return length / circumference(inner_diameter = ring_size, gauge = gauge)

#Calculates spool length
def weight_to_length(weight, gauge, density = None):
    return weight / (density * pi * (awg_gauge[gauge]/2)**2)

def aspect_ratio(gauge, inner_diameter = None, outer_diameter = None):
    if outer_diameter and not inner_diameter:
        inner_diameter = outer_diameter - 2 * awg_gauge[gauge]
    if inner_diameter:
        return inner_diameter / awg_gauge[gauge]

print "Rings per spool: %s" % spool(length = weight_to_length(1, 16, al_wire_density[5356]), gauge = 16, ring_size = '3/16')
