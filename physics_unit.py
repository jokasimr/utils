
from numpy import pi
from operator import add, sub, mul, truediv

class Unit():
    def __init__(self, **parts):
        self.parts = {part: power for part, power in parts.items()}

    def __repr__(self):
        letters = ' '.join('%s^%s' % (part, power)
                if not power==1 else '%s' % part
                for part, power in
                sorted(self.parts.items(), key=lambda x: x[0]))
        return '[%s]' % letters


    def _operate(self, other, operator):
        if not isinstance(other, Unit):
            if isinstance(other, float) or isinstance(other, int):
                return operator(self, PhysicalQuantity(other, Unit()))
            else:
                raise ValueError("%s is neither a unit or a value!" % other)
        
        parts = self.parts.copy()
        for p in other.parts:
            if p in parts:
                parts[p] = operator(parts[p], other.parts[p])
            else:
                parts[p] = operator(0, other.parts[p])
        parts = {key:val for key, val in parts.items() if val!=0}
        return Unit(**parts)

    def __pow__(self, other):
        if other==0:
            return Unit()
        elif other>0:
            operator = mul
        else:
            operator = truediv
        res = Unit()
        for _ in range(abs(other)):
            res = operator(res, self)
        return res

    def __mul__(self, other):
        return self._operate(other, add)
    
    def __rmul__(self, other):
        return self

    def __truediv__(self, other):
        return self._operate(other, sub)
    
    def __rtruediv__(self, other):
        return (self.__truediv__(other))**(-1)

    def __eq__(self, other):
        return self.parts.items() == other.parts.items()

    def __add__(self, other):
        if self == other:
            return Unit(**self.parts)
        else:
            raise ValueError("Units that are not the same cannot be added together.")
            
    def __radd__(self, other):
        raise ValueError("Units that are not the same cannot be added together.")
            
    def __sub__(self, other):
        if self == other:
            return Unit(**self.parts)
        else:
            raise ValueError("Units that are not the same cannot be subtracted together.")
            
    def __rsub__(self, other):
        raise ValueError("Units that are not the same cannot be added together.")

    def __len__(self):
        return sum(abs(x) for x in self.parts.values())




class PhysicalQuantity:
    def __init__(self, value, unit):
        self.value = value
        self.unit = unit

    def _operate(self, other, operator):
        unit = self.unit
        value = other
        if isinstance(other, PhysicalQuantity):
            unit = operator(unit, other.unit)
            value = other.value
        value = operator(self.value, value)
        if len(unit)==0:
            return value
        return PhysicalQuantity(value, unit)

    def __pow__(self, other):
        if isinstance(other, PhysicalQuantity):
            raise ValueError("Can't have a PQ in the exponent.")
        else:
            value = pow(self.value, other)
            unit = pow(self.unit, other)
        return PhysicalQuantity(value, unit)

    def __mul__(self, other):
        return self._operate(other, mul)
    
    def __rmul__(self, other):
        return self._operate(other, mul)

    def __truediv__(self, other):
        return self._operate(other, truediv)
    
    def __rtruediv__(self, other):
        return (self.__truediv__(other))**(-1)

    def __add__(self, other):
        return self._operate(other, add)
    

    def __sub__(self, other):
        return self._operate(other, sub)
    
    
    def __repr__(self):
        return '%s %s' % (self.value, self.unit)


PQ = PhysicalQuantity

# SI-units
kg = Unit(kg=1)
m = Unit(m=1)
s = Unit(s=1)
A = Unit(A=1)
K = Unit(K=1)
mol = Unit(mol=1)
cd = Unit(cd=1)

# SI non base units
J = kg*m**2/s**2
N = kg*m/s**2
u = Unit(u=1)
eV = Unit(eV=1)

# constants
c = PQ(299792458, m/s)
G = PQ(6.67408*10**(-11), m**3/kg/s**2)
h = PQ(6.626070040 * 10**(-34), J*s)
hb = h/(2*pi)
mu0 = PQ(4*pi*10**(-7), N/A**2)
e0 = (mu0*c**2)**(-1)
e = PQ(1.6021766208 * 10**(-19), A*s)
m_e = PQ(9.10938356 * 10**(-31), kg)
m_p = PQ(1.672621898 * 10**(-27), kg)
m_n = PQ(1.674927471*10**(-27), kg)
m_u = PQ(1.660539040*10**(-27), kg/u)
J_eV = e*PQ(1, J/(A*s)/eV)

'''
# REDEFINING STUFF; UGLY AHEAD
# SI non base units
J = PQ(1, kg*m**2/s**2)
N = PQ(1, kg*m/s**2)
u = PQ(1, u)
eV = PQ(1, eV)

# SI-units
kg = PQ(1, kg)
m = PQ(1, m)
s = PQ(1, s)
A = PQ(1, A)
K = PQ(1, K)
mol = PQ(1, mol)
cd = PQ(1, cd)

'''