"""This is an old version of the Span class that uses custom-written
start and end calculations, rather than the built-in slice object.

I've kept it because I didn't want to lose working code, and it has a
*slight* performance increase of the slice-based object (although it is
very minimal).
"""


class _SpanOld:
    def __init__(self, over, start=None, end=None):
         # simulate some limits
        if start is not None and start < 0:
            raise IndexError("span start index out of range")

        offset = 0
        self.__over = over
        if isinstance(over, _SpanOld):  # prevent levels of Span building up
            self.__over = over.__over
            offset = over.__start
        # start span calculation
        self.__start = (0 if start is None else start) + offset
        # end span calculation
        max_end = len(self.__over) - offset
        self.__end = max_end if end is None else end + offset
        if self.__end < self.__start:  # allows for simulating [][1:]
            self.__end = self.__start
        elif self.__end > max_end:  # prevents span from going beyond end
            raise IndexError("span end index out of range")

    def __getitem__(self, key):
        if key >= self.__end:
            raise IndexError("span index out of range")
        return self.__over[self.__start + key]

    def __len__(self):
        return self.__end - self.__start

    def __repr__(self):
        sb = "["
        ln = len(self)
        for i in range(ln):
            sb += str(self[i])
            if i < ln - 1:
                sb += ", "
        return sb + "]"

    def __str__(self):
        return repr(self)
