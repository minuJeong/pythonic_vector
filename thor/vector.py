
"""

author: minu jeong
"""

from functools import partial
from itertools import permutations


class _Vector(object):
    """
    abstract vector class.
    do not create this class as instance.
    """

    _precision = float
    _dimension = 0
    _data = []
    _key_mappings_set_1 = "xyzw"
    _key_mappings_set_2 = "rgba"
    _key_mappings_set_3 = "uv"

    def __init__(self, *argvs):
        """
        dynamic constructor for _Vector classes.
        Won't be initializable by name, "_Vector".
        You should use, Vector2, Vector3, etc.
        """

        self._data = list(map(
            lambda argv: self._precision(argv),
            argvs[:self._dimension]))

        # connect properties
        mappings = [
            _Vector._key_mappings_set_1,
            _Vector._key_mappings_set_2,
            _Vector._key_mappings_set_3
        ]

        def getter_template(idx, instance):
            return instance._data[idx]

        def setter_template(idx, instance, value):
            instance._data[idx] = self._precision(value)

        for mapping in mappings:
            # map single char keys
            for map_key in mapping:
                idx = mapping.index(map_key)

                fprop = property(
                    partial(getter_template, idx),
                    partial(setter_template, idx)
                )
                setattr(_Vector, map_key, fprop)

            # map multi char keys
            for count in range(2, len(mapping) + 1):
                for permute in permutations(mapping, count):
                    getters = []
                    setters = []
                    for w in permute:
                        idx = mapping.index(w)
                        getters.append(partial(getter_template, idx))
                        setters.append(partial(setter_template, idx))

                    fprop = property(
                        (lambda ins: [fget(ins) for fget in getters]),
                        (lambda ins, vs: [fset(ins, v) for fset, v in zip(setters, vs)]),
                    )
                    prop_name = ''.join(permute)
                    setattr(_Vector, prop_name, fprop)

                    print(prop_name, len(getters))
                    print((lambda ins: [fget(ins) for fget in getters])(self))

    def __add__(self, dst):
        return type(self)(*list(map(
            lambda elm: elm[0] + elm[1],
            zip(self._data, dst._data))))

    def __sub__(self, dst):
        return type(self)(*list(map(
            lambda elm: elm[0] - elm[1],
            zip(self._data, dst._data))))

    def __mul__(self, dst):
        return type(self)(lambda x: x * dst, self._data)

    def __repr__(self):
        return "vector {}, {}, {}".format(
            self.x, self.y, self.z
        )

    def normalize(self):
        summed = sum(self._data)
        self._data = list(map(lambda x: x / summed, self._data))


def generate_vector_classes():
    """
    add Vector1 to Vector10 classes dynamically
    """

    if not __package__:
        raise Exception("vector module can only be used as library")

    for dimension in range(1, 5):
        v_class_name = "Vector{}".format(dimension)
        v_class = type(v_class_name, (_Vector,), {"_dimension": dimension})

        module = __import__(__package__)
        setattr(module, v_class_name, v_class)
        globals()[v_class_name] = v_class

generate_vector_classes()
