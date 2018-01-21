
"""
pi = 3.14159265359
# constants
c = 299792458 # m/s
G = 6.67408*10**(-11)# m**3/kg/s**2
h = 6.626070040 * 10**(-34)# J*s
hb = h/(2*pi)
mu0 = 4*pi*10**(-7)# N/A**2
e0 = (mu0*c**2)**(-1)
e = 1.6021766208 * 10**(-19)# A*s
m_e = 9.10938356 * 10**(-31)# kg
m_p = 1.672621898 * 10**(-27)# kg
m_n = 1.674927471*10**(-27)# kg
m_u = 1.660539040*10**(-27)# kg/u
"""
import pint
from IPython import display
import numpy as np
import matplotlib.pyplot as plt

u = pint.UnitRegistry(auto_reduce_dimensions=True)

def show(self):
    unit = self.u
    self = self*1.0
    self = self.to(unit)
    text = '${:~L.03}$'.format(self).replace('**', '^')
    text = text.replace('*', '\cdot')
    display.display(display.Latex(text))

s = show

constants = set(locals()) - set([v for v in locals() if v.startswith('_')])
import tabulate
display.display(display.HTML(tabulate.tabulate([sorted(constants)], tablefmt='html')))
del tabulate

