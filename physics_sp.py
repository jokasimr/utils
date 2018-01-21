
import sympy as sp
from sympy.physics.units import *

u = atomic_mass_constant

print(convert_to(u, [c, mega * electronvolt]))
print(mega)

