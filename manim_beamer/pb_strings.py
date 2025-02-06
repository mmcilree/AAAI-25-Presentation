class PBConstraint():
    def __init__(self, pb_sum, rhs):
        self._pb_sum = pb_sum
        self._rhs = rhs
    
    def __str__(self):
        return str(self._pb_sum) + " \geq " + str(self._rhs)

class PBSum():
    def __init__(self, terms = []):
        self._terms = terms
    
    def __str__(self):
        return " + ".join([str(t) for t in self._terms])
    
    def __add__(self, term):
        new_terms = self._terms + [term]
        return PBSum(terms = new_terms)
    
    def __ge__(self, num):
        return PBConstraint(self, num)
    
class PBTerm():
    def __init__(self, coeff, var):
        self._var = var
        self._coeff = coeff
    
    def __str__(self):
        if isinstance(self._var, PBIntVar):
            return " + ".join([str((2**i) * self._coeff) + ' ' + str(self._var.bit_vars[i]) for i in range(self._var.num_bits)])

        
        return str(self._coeff) + ' ' + str(self._var)
            
class PBIntVar():
    def __init__(self, label, num_bits, id=None):
        self._id = id if id is not None else ''
        self._label = label
        self.num_bits = num_bits
        self.bit_vars = [PBBitVar(label, i) for i in range(self.num_bits)]
    
    def __rmul__(self, coeff):
        return PBTerm(coeff, self)

class PBBitVar():
    def __init__(self, label, bit):
        self._label = label
        self._bit = bit
    
    def __str__(self):
        return self._label + "_{b" + str(self._bit) + "}"
    
    def __rmul__(self, coeff):
        return PBTerm(coeff, self)
