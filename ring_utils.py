#Ring calculator

from math import pi
from fractions import Fraction

awg = { #American Wire Gauge to inches
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

#Aluminum alloy density in lbs/in^3
al_wire_density = { 0:0.1, #Default, pure AL
                    5356:0.0954}

#Average of inner and outer diameter
def middle_diameter(wire_diameter, inner_diameter = None, outer_diameter = None):
    if inner_diameter and outer_diameter:
        return (inner_diameter + outer_diameter) / 2
    if inner_diameter:
        return inner_diameter + wire_diameter
    if outer_diameter:
        return outer_diameter - wire_diameter

def circumference(wire_diameter, inner_diameter = None, outer_diameter = None):
    return 2 * pi * (middle_diameter(inner_diameter = inner_diameter, outer_diameter = outer_diameter, wire_diameter = wire_diameter) / 2)

#broken
#Calculates how many rings can be gotten out of a spool of wire
def spool(length, wire_diameter, ring_size):
    if type(ring_size) == str:
        ring_size = float(sum(Fraction(s) for s in ring_size.split()))
    return round(length / circumference(inner_diameter = ring_size, wire_diameter = wire_diameter))

#Calculates spool length
def weight_to_length(weight, wire_diameter, density):
    """Calculates spool length given the spool weight, gauge, and metal density """
    return weight / (density * pi * (wire_diameter / 2) ** 2)

def aspect_ratio(wire_diameter, inner_diameter = None, outer_diameter = None):
    if outer_diameter and not inner_diameter:
        inner_diameter = outer_diameter - 2 * wire_diameter
    if inner_diameter:
        return inner_diameter / wire_diameter

def e4_1_area(inner_diameter, wire_diameter):
    """Calculates the rings per square foot needed for European 4 in 1 sheet weave maille"""
    #iph = inches per horizontal ring
    #ipv = inches per vertical ring

    ar = aspect_ratio(wire_diameter, inner_diameter)
    iph = wire_diameter * (0.9215 * ar - 0.1566)
    ipv = wire_diameter * (-0.0582 * ar**3 + 0.8677 * ar**2 - 3.2996 * ar + 6.2401)
    return round(144 / (iph * ipv));

#broken
def byzantine(inner_diameter, wire_diameter, length, connectors = 2):
    """Calculates the number of rings needed to make a byzantine chain"""
    variants = {
        2:{
            'name':'2 connector',
            'rings_per_unit':6,
            'rounding_multiple':6,
	        'a0':-6.29133663006863,
	        'a1':5.46848493807012,
	        'a2': -0.928019290982938,
	        'a3':0.120964629313913,
	        'a4':-0.00608094464016895,
            'a5': 0,
        },
        3:{
            'rounding_multiple':4,
            'a0':-38.43723917,
	        'a1':31.43459744,
	        'a2':-9.08642132,
	        'a3':1.278173853,
	        'a4':-0.068152449,
	        'a5':0,
        },
    }

    ar = aspect_ratio(inner_diameter, wire_diameter)
    #ipnu = inches / normalized unit
    ipnu = (variants[connectors]['a5'] * ar**5 + variants[connectors]['a4'] * ar**4 + variants[connectors]['a3'] * ar**3 + variants[connectors]['a2'] * ar**2 + variants[connectors]['a1'] * ar + variants[connectors]['a0']);
    #// rpl = rings / length
    rpl = length * variants[connectors]['rings_per_unit'] / (ipnu * wire_diameter);
    rpl = rpl - connectors;
    rpl = variants[connectors]['rounding_multiple'] * round(rpl / variants[connectors]['rounding_multiple']);
    return rpl + connectors;

print "Rings per spool: %s, should be ~3000" % spool(length = weight_to_length(1, 16, al_wire_density[5356]), wire_diameter = awg[16], ring_size = '3/16')

print "Byzantine (2 connector): %s , should be 68" %byzantine(inner_diameter=.5, wire_diameter=.1, length=10)
