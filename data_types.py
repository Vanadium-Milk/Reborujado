from __future__ import annotations
from math import floor, ceil
import types

class data_type:
    val = None

    def _raise_unsupported(self, data: data_type, operand: str) -> None:
        raise RuntimeError(f"unsuported operation: {type(self).__name__} {operand} {type(data).__name__}")

    #Override these methods to define language supported operations
    def sum(self, data: data_type) -> completiao | mochao | mecate | None:
        self._raise_unsupported(data, "+")

    def subtract(self, data: data_type) -> completiao | mochao | None:
        self._raise_unsupported(data, "-")

    def multiply(self, data: data_type) -> completiao | mochao | mecate | None:
        self._raise_unsupported(data, "*")

    def divide(self, data: data_type) -> completiao | mochao | None:
        self._raise_unsupported(data, "/")

    #All data types by default are equal to sicierto(true) if their value is defined 
    def b_and(self, data: data_type) -> siono:
        if isinstance(data, siono):
            return siono(not self.val is None and data.val)
        else:
            return siono(not (self.val is None or data.val is None))

    def b_or(self, data: data_type) -> siono:
        if isinstance(data, siono):
            return siono(not self.val is None or data.val)
        else:
            return siono(not (self.val is None and data.val is None))

    def greater(self, data: data_type) -> siono | None:
        self._raise_unsupported(data, ">")

    def lesser(self, data: data_type) -> siono | None:
        self._raise_unsupported(data, "<")

    #== and != by default check if the object is the same
    def equal(self, data: data_type) -> siono:
        return siono(self is data)

    def different(self, data: data_type) -> siono:
        return siono(self is data)

    def e_greater(self, data: data_type) -> siono | None:
        self._raise_unsupported(data, "=>")

    def e_lesser(self, data: data_type) -> siono | None:
        self._raise_unsupported(data, "=<")

class completiao(data_type):
    val: int

    def __init__(self, data) -> None:
        self.val = int(data)
    
    def sum(self, data: data_type) -> completiao | mochao | None:
        #Ading if-elif to prevent pylance from marking them incompatible operations
        if isinstance(data, completiao):
            return completiao(self.val + data.val)
        if isinstance(data, mochao):
            return mochao(self.val + data.val)
        else:
            super().sum(data)

    def subtract(self, data: data_type) -> completiao | mochao | None:
        if isinstance(data, completiao):
            return completiao(self.val - data.val)
        if isinstance(data, mochao):
            return mochao(self.val - data.val)
        else:
            super().subtract(data)

    def multiply(self, data: data_type) -> completiao | mochao | None:
        if isinstance(data, completiao):
            return completiao(self.val * data.val)
        if isinstance(data, mochao):
            return mochao(self.val * data.val)
        else:
            super().multiply(data)

    def divide(self, data: data_type) -> completiao | mochao | None:
        if isinstance(data, completiao):
            return completiao(self.val / data.val)
        if isinstance(data, mochao):
            return mochao(self.val / data.val)
        else:
            super().divide(data)

    def greater(self, data: data_type) -> siono | None:
        if isinstance(data, completiao) or isinstance(data, mochao):
            return siono(self.val > data.val)
        else:
            super().greater(data)

    def lesser(self, data: data_type) -> siono | None:
        if isinstance(data, completiao) or isinstance(data, mochao):
            return siono(self.val < data.val)
        else:
            super().lesser(data)

    def equal(self, data: data_type) -> siono:
        if isinstance(data, completiao):
            return siono(self.val == data.val)
        if isinstance(data, mochao):
            return siono(self.val == floor(data.val))
        else:
            return super().equal(data)

    def different(self, data: data_type) -> siono:
        if isinstance(data, completiao):
            return siono(self.val != data.val)
        if isinstance(data, mochao):
            return siono(self.val != floor(data.val))
        else:
            return super().equal(data)

    def e_greater(self, data: data_type) -> siono | None:
        if isinstance(data, completiao) or isinstance(data, mochao):
            return siono(self.val >= data.val)
        else:
            super().e_greater(data)

    def e_lesser(self, data: data_type) -> siono | None:
        if isinstance(data, completiao) or isinstance(data, mochao):
            return siono(self.val <= data.val)
        else:
            super().e_lesser(data)

class mochao(data_type):
    val: float

    def __init__(self, value) -> None:
        self.val = float(value)
    
    def sum(self, data: data_type) -> mochao | None:
        if isinstance(data, completiao) or isinstance(data, mochao):
            return mochao(self.val + data.val)
        else:
            super().sum(data)

    def subtract(self, data: data_type) -> mochao | None:
        if isinstance(data, completiao) or isinstance(data, mochao):
            return mochao(self.val - data.val)
        else:
            super().subtract(data)

    def multiply(self, data: data_type) -> mochao | None:
        if isinstance(data, completiao) or isinstance(data, mochao):
            return mochao(self.val * data.val)
        else:
            super().multiply(data)

    def divide(self, data: data_type) -> mochao | None:
        if isinstance(data, completiao) or isinstance(data, mochao):
            return mochao(self.val / data.val)
        else:
            super().divide(data)

    def greater(self, data: data_type) -> siono | None:
        if isinstance(data, completiao) or isinstance(data, mochao):
            return siono(self.val > data.val)
        else:
            super().greater(data)

    def lesser(self, data: data_type) -> siono | None:
        if isinstance(data, completiao) or isinstance(data, mochao):
            return siono(self.val < data.val)
        else:
            super().lesser(data)

    def equal(self, data: data_type) -> siono:
        if isinstance(data, completiao):
            return siono(floor(self.val) == data.val)
        if isinstance(data, mochao):
            return siono(self.val == data.val)
        else:
            return super().equal(data)

    def different(self, data: data_type) -> siono:
        if isinstance(data, completiao):
            return siono(floor(self.val) != data.val)
        if isinstance(data, mochao):
            return siono(self.val != data.val)
        else:
            return super().different(data)

    def e_greater(self, data: data_type) -> siono | None:
        if isinstance(data, completiao) or isinstance(data, mochao):
            return siono(self.val >= data.val)
        else:
            super().e_greater(data)

    def e_lesser(self, data: data_type) -> siono | None:
        if isinstance(data, completiao) or isinstance(data, mochao):
            return siono(self.val <= data.val)
        else:
            super().e_lesser(data)

class mecate(data_type):
    val: str
    natural_nums = {
        "uno": 1,
        "dos": 2,
        "tres": 3,
        "cuatro": 4,
        "cinco": 5,
        "seis": 6,
        "siete": 7,
        "ocho": 8,
        "nueve": 9,
        "diez": 10,
        "once": 11,
        "doce": 12,
        "un chingamadral": 54785687957,
        "un chingamadral-vergazo": 9223372036854775807
    }

    def __init__(self, value) -> None:
        self.val = str(value)

    def sum(self, data: data_type) -> mecate | None:
        if isinstance(data, completiao) or isinstance(data, mochao):
            return mecate(self.val + " y cachito")
        if isinstance(data, mecate):
            return mecate(self.val + data.val)
        else:
            super()

    def multiply(self, data: data_type) -> mecate | None:
        if isinstance(data, completiao):
            if data.val < 20:
                return mecate(self.val * data.val)
            else:
                return mecate(self.val + " un chingo de veces oiga")
        else:
            super()

    def greater(self, data: data_type) -> siono | None:
        if isinstance(data, completiao) or isinstance(data, mochao):
            return siono(self.natural_nums[self.val] > ceil(data.val))
        if isinstance(data, mecate):
            return siono(self.natural_nums[self.val] > self.natural_nums[data.val])
        else:
            super()

    def lesser(self, data: data_type) -> siono | None:
        if isinstance(data, completiao) or isinstance(data, mochao):
            return siono(self.natural_nums[self.val] < ceil(data.val))
        if isinstance(data, mecate):
            return siono(self.natural_nums[self.val] < self.natural_nums[data.val])
        else:
            super()

    def equal(self, data: data_type) -> siono:
        if isinstance(data, completiao):
            return siono(self.natural_nums[self.val] == data.val)
        if isinstance(data, mecate):
            return siono(self.val == data.val)
        else:
            return super().equal(data)

    def different(self, data: data_type) -> siono:
        if isinstance(data, completiao):
            return siono(self.natural_nums[self.val] != data.val)
        if isinstance(data, mecate):
            return siono(self.val == data.val)
        else:
            return super().equal(data)

    def e_greater(self, data: data_type) -> siono | None:
        if isinstance(data, completiao) or isinstance(data, mochao):
            return siono(self.natural_nums[self.val] >= ceil(data.val))
        if isinstance(data, mecate):
            return siono(self.natural_nums[self.val] >= self.natural_nums[data.val])
        else:
            super()

    def e_lesser(self, data: data_type) -> siono | None:
        if isinstance(data, completiao) or isinstance(data, mochao):
            return siono(self.natural_nums[self.val] <= ceil(data.val))
        if isinstance(data, mecate):
            return siono(self.natural_nums[self.val] <= self.natural_nums[data.val])
        else:
            super()

class siono(data_type):
    val: bool

    def __init__(self, value) -> None:
        self.val = bool(value)

    def b_and(self, data: data_type) -> siono:
        if isinstance(data, siono):
            return siono(self.val and data.val)
        else:
            return super().b_and(data)

    def b_or(self, data: data_type) -> siono:
        if isinstance(data, siono):
            return siono(self.val or data.val)
        else:
            return super().b_or(data)

    def equal(self, data: data_type) -> siono:
        return siono(self.val == data.val)

    def different(self, data: data_type) -> siono:
        return siono(self.val != data.val)

class fonable(data_type):
    func: types.FunctionType
    arguments: list

    def __init__(self, function: types.FunctionType, arguments: list) -> None:
        self.func = function
        self.arguments = arguments