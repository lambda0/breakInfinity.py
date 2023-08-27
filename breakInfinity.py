import math
class breakInfinity:
    def __init__(self,x,a,b):
        self.sign=x
        self.mantissa=a
        self.exponent=b
    def toString(self, type):
        if type in [0, "sci", "scientific"]:
            if self.sign == 0:
                return "0"
            elif self.sign == 1:
                if -3 <= self.exponent <= 5:
                    return str(round((self.mantissa * (10 ** self.exponent)), 6))
                elif 5 < self.exponent <= 1e6:
                    return str(round(self.mantissa, 6)) + "e" + str(self.exponent)
                elif 1e6 < self.exponent <= 1e20:
                    return str(round(self.mantissa, 6)) + "e" + str(round(self.exponent / (10 ** (math.floor(math.log10(self.exponent)))), 6)) + "e" + str(math.floor(math.log10(self.exponent)))
                elif 1e20 < self.exponent <= 1e308:
                    return "e" + str(round(self.exponent / (10 ** (math.floor(math.log10(self.exponent)))), 6)) + "e" + str(math.floor(math.log10(self.exponent)))
                elif -3 > self.exponent >= -1e6:
                    return str(round(self.mantissa, 6)) + "e" + str(self.exponent)
                elif -1e6 > self.exponent >= -1e20:
                    return str(round(self.mantissa, 6)) + "e" + str(round(self.exponent / (10 ** (len(str(self.exponent)) - 2)), 6)) + "e" + str(len(str(self.exponent)) - 2)
                elif -1e20 > self.exponent >= -1e308:
                    return "e" + str(round(self.exponent / (10 ** (len(str(self.exponent)) - 2)), 6)) + "e" + str(len(str(self.exponent)) - 2)
            elif self.sign == -1:
                return breakInfinity(1, self.mantissa, self.exponent).toString(0)
    def normal(self):
        if self.sign == 0:
            self.mantissa = 0
            self.exponent = 0
        elif self.mantissa == 0:
            self.sign == 0
        elif self.mantissa < 0:
            self.sign = -self.sign
            self.mantissa = -self.mantissa
        else:
            while self.mantissa >= 10:
                self.mantissa /= 10
                self.exponent += 1
            while self.mantissa < 1:
                self.mantissa *= 10
                self.exponent -= 1
        return self
    def sgn(self):
        return self.sign
    def getMantissa(self):
        return self.mantissa
    def getExponent(self):
        return self.exponent
    def abs(self):
        return breakInfinity(1, self.mantissa, self.exponent)
    def cmp(self, other): # return larger value
        if other.sign > self.sign:
            return other
        elif self.sign > other.sign:
            return self
        elif self.sign == other.sign:
            if self.sign == 0:
                return self
            elif self.sign == 1:
                if self.exponent > other.exponent:
                    return self
                elif other.exponent > self.exponent:
                    return other
                elif self.exponent == other.exponent:
                    if self.mantissa > other.mantissa:
                        return self
                    elif other.mantissa > self.mantissa:
                        return other
                    elif self.mantissa == other.mantissa:
                        return self
            elif self.sign == -1:
                if self.exponent > other.exponent:
                    return other
                elif other.exponent > self.exponent:
                    return self
                elif self.exponent == other.exponent:
                    if self.mantissa > other.mantissa:
                        return other
                    elif other.mantissa > self.mantissa:
                        return self
                    elif self.mantissa == other.mantissa:
                        return self
    def cmpabs(self, other):
        return self.abs().cmp(other.abs())
    def neg(self):
        return breakInfinity(-self.sign, self.mantissa, self.exponent)
    def rec(self):
        return breakInfinity(self.sign, 1 / self.mantissa, -self.exponent).normal()
    def isPos(self):
        return True if self.sign == 1 else False
    def isZero(self):
        return True if self.sign == 0 else False
    def isNeg(self):
        return True if self.sign == -1 else False
    def eq(self, other):
        return True if self.sign == other.sign and self.mantissa == other.mantissa and self.exponent == other.exponent else False
    def gt(self, other):
        return True if self.cmp(other) == self and not self.eq(other) else False
    def gte(self, other):
        return self.eq(other) or self.gt(other)
    def lt(self, other):
        return not self.gte(other)
    def lte(self, other):
        return not self.gt(other)
    def neq(self, other):
        return not self.eq(other)
    def max(self, other):
        return self.cmp(other)
    def min(self, other):
        return self.neg().max(other.neg()).neg()
    def add(self, other):
        if abs(self.exponent - other.exponent) > 20:
            return self.cmpabs(other)
        elif self.eq(breakInfinity(0, 0, 0)):
            return other
        elif other.eq(breakInfinity(0, 0, 0)):
            return self
        elif self.sign == 1 and other.sign == 1:
            if self.gte(other):
                self.mantissa += (other.mantissa * (10 ** -abs(other.exponent - self.exponent)))
                return self
            elif self.lt(other):
                other.mantissa += (self.mantissa * (10 ** -abs(self.exponent - other.exponent)))
                return other
        elif self.sign == 1 and other.sign == -1:
            if self.abs().gte(other.abs()):
                self.mantissa -= (other.mantissa * (10 ** -abs(other.exponent - self.exponent)))
                return self
            elif self.abs().lt(other.abs()):
                other.mantissa -= (self.mantissa * (10 ** -abs(self.exponent - other.exponent)))
                return other
        elif self.sign == -1:
            return self.neg().add(other.neg()).neg
    def sub(self, other):
        return self.add(other.neg())
    def mul(self, other):
        if abs(self.exponent - other.exponent) > 1e20:
            return self.cmpabs(other)
        elif self.sign == 0 or other.exponent == 0:
            return breakInfinity(0, 0, 0)
        else:
            return breakInfinity(self.sign * other.sign, self.mantissa * other.mantissa, self.exponent + other.exponent).normal()
    def div(self, other):
        return self.mul(other.rec())
    def exp(self):
        exp = self.sign * math.floor(self.mantissa * (10 ** self.exponent))
        man = math.modf(self.mantissa * (10 ** self.exponent))[1]
        return breakInfinity(1, man, exp)
    def pow(self, other):
        exp = other.mantissa * (10 ** other.exponent) * (self.exponent + math.log10(self.mantissa))
        if exp > 1e20:
            return breakInfinity(1, 1, exp)
        else:
            return breakInfinity(1, 10 ** (exp % 1), exp // 1)
    def log(self):
        return breakInfinity(1, self.exponent + math.log10(self.mantissa), 0).normal()
    def logb(self, base):
        return self.log().div(base.log())
    def root(self, base):
        return self.pow(base.rec())
    def floor(self):
        if self.sign == 0:
            return self
        elif self.sign == 1:
            if self.lt(breakInfinity(1, 1, 20)):
                return breakInfinity(1, math.floor(self.mantissa * (10 ** self.exponent)) / (10 ** self.exponent), self.exponent)
            else:
                return self
        elif self.sign == -1:
            return self.neg().ceil().neg()
    def ceil(self):
        if self.sign == 0:
            return self
        elif self.sign == 1:
            if self.lt(breakInfinity(1, 1, 20)):
                return breakInfinity(1, math.ceil(self.mantissa * (10 ** self.exponent)) / (10 ** self.exponent), self.exponent)
            else:
                return self
        elif self.sign == -1:
            return self.neg().floor().neg()
    def round(self):
        if self.sign == 0:
            return self
        elif self.sign == 1:
            if self.lt(breakInfinity(1, 1, 20)):
                return breakInfinity(1, round(self.mantissa * (10 ** self.exponent)) / (10 ** self.exponent), self.exponent)
            else:
                return self
        elif self.sign == -1:
            return self.neg().round().neg()
