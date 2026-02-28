import math
def degress_to_radians():
    degrees = float(input("Input degrees: "))
    print(f"Output radius: {degrees * math.pi / 180:.6f}")

def area_of_trapezoid():
    h = float(input("Height: "))
    b1 = float(input("Base 1: "))
    b2 = float(input("Base 2: "))
    print(f"Area of trapezoid: {(b1 + b2) * h / 2:.6f}")


def area_poligon():
    sides = int(input("Number of sides: "))
    length = float(input("Length of sides: "))
    print(f"Area of poligon: {sides * length**2 / (4 * math.tan(math.pi / sides)):.6f}")
area_poligon()


def area_of_parallelogram():
    b = float(input("Length of base: "))
    h = float(input("Height of parallelogram: "))
    print(f"Area of parallelogram: {b * h:.6f}")