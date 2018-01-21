

from physics_old import Unit, PhysicalQuantity as PQ

kg = Unit(kg=1)
V = Unit(m=3)
rå = kg/V
Ek = Unit(m=2, s=-2, kg=1)

assert Ek.__repr__() == (kg*V / Unit(m=1) / Unit(s=2)).__repr__()
assert rå.__repr__() == '[kg m^-3]'

assert kg == Unit(kg=1)


a = False
try:
    x = rå + kg
except ValueError:
    a = True
assert a
assert (rå + Unit(kg=1, m=-3)) == rå


me = PQ(9, kg)
assert (me*me).__repr__() == '81 [kg^2]'
assert (me/me).__repr__() == '1.0 []'

print(PQ(10.3, Ek*kg)+PQ(4, Ek)*me)


