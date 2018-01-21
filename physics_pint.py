import pint as pt
import numpy as np

u = pt.UnitRegistry()


print((1 * u.u).to(u.electronvolt/u.c**2))
