
"""

author: minu jeong
"""

from functools import partial


class _VectorProperty(property):
    pass


class _Vector(object):
    """
    abstract vector class.
    do not create this class as instance.

    [WARNING]
    _KEYMAPs should not conflict.
    """

    # static:
    _PRECISION = float
    _KEYMAP_SET_1 = "xyzw"
    _KEYMAP_SET_2 = "rgba"
    _KEYMAP_SET_3 = "uvw"

    # private:
    _dimension = 0
    _data = []

    def __init__(self, *argvs):
        """
        dynamic constructor for _Vector classes.
        Won't be initializable by name, "_Vector".
        You should use, Vector2, Vector3, etc.
        """

        self._data = list(map(
            lambda argv: self._PRECISION(argv),
            argvs[:self._dimension]))

        self._map_keys()

    def _map_keys(self):
        """
        create and connect properties
        """

        def getter_template(idx, instance):
            return instance._data[idx]

        def setter_template(idx, instance, value):
            instance._data[idx] = _Vector._PRECISION(value)

        # connect properties
        mappings = [
            _Vector._KEYMAP_SET_1,
            _Vector._KEYMAP_SET_2,
            _Vector._KEYMAP_SET_3
        ]

        # map single char keys
        for mapping in mappings:
            for map_key in mapping:
                idx = mapping.index(map_key)

                fprop_single = property(
                    partial(getter_template, idx),
                    partial(setter_template, idx)
                )
                setattr(type(self), map_key, fprop_single)

    def __getattr__(self, attr_name):
        mappings = [
            _Vector._KEYMAP_SET_1,
            _Vector._KEYMAP_SET_2,
            _Vector._KEYMAP_SET_3
        ]
        for mapping in mappings:
            if any(filter(lambda x: x not in mapping, attr_name)):
                continue

            result = []
            for attr_key in attr_name:
                result.append(
                    self._data[mapping.index(attr_key)])
            if result:
                return result

        raise AttributeError("error getting attribute: {}".format(attr_name))

    def __setattr__(self, attr_name, values):
        mappings = [
            _Vector._KEYMAP_SET_1,
            _Vector._KEYMAP_SET_2,
            _Vector._KEYMAP_SET_3
        ]

        if len(attr_name) > 1:
            for mapping in mappings:
                if any(filter(lambda x: x not in mapping, attr_name)):
                    continue

                if not len(attr_name) == len(values):
                    raise Exception("values count should match the attribute receiver")

                was_valid = False
                for attr_key, value in zip(attr_name, values):
                    self._data[mapping.index(attr_key)] = value
                    was_valid = True

                if was_valid:
                    return

        super(_Vector, self).__setattr__(attr_name, values)

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
        return "vector {}".format(
            ', '.join(map(lambda x: str(x), self._data))
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
