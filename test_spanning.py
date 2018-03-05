#! /usr/bin/env python3
import unittest
from spanning import *


class TestReadOnlySpan(unittest.TestCase):
    span = ReadOnlySpan

    def test_init_list(self):
        ls = [1, 2, 3, 4, 5]

        sp = self.span(ls)
        self.assertEqual(sp._over, ls)
        self.assertEqual(sp._slice.start, 0)
        self.assertEqual(sp._slice.stop, len(ls))
        self.assertEqual(sp._slice.step, 1)

        sp = self.span(ls, 2)
        self.assertEqual(sp._over, ls)
        self.assertEqual(sp._slice.start, 2)
        self.assertEqual(sp._slice.stop, len(ls))
        self.assertEqual(sp._slice.step, 1)

        sp = self.span(ls, 2, 4)
        self.assertEqual(sp._over, ls)
        self.assertEqual(sp._slice.start, 2)
        self.assertEqual(sp._slice.stop, 4)
        self.assertEqual(sp._slice.step, 1)

        sp = self.span(ls, 1, step=2)
        self.assertEqual(sp._over, ls)
        self.assertEqual(sp._slice.start, 1)
        self.assertEqual(sp._slice.stop, len(ls))
        self.assertEqual(sp._slice.step, 2)

        sp = self.span(ls, 1, step=-1)
        self.assertEqual(sp._over, ls)
        self.assertEqual(sp._slice.start, 1)
        self.assertEqual(sp._slice.stop, len(ls))
        self.assertEqual(sp._slice.step, -1)

        sp = self.span(ls, 1, 3, -1)
        self.assertEqual(sp._over, ls)
        self.assertEqual(sp._slice.start, 1)
        self.assertEqual(sp._slice.stop, 3)
        self.assertEqual(sp._slice.step, -1)

    def test_init_span(self):
        ls = [1, 2, 3, 4, 5, 6, 7]

        sp = self.span(self.span(ls))
        self.assertEqual(sp._over, ls)
        self.assertEqual(sp._slice.start, 0)
        self.assertEqual(sp._slice.stop, len(ls))
        self.assertEqual(sp._slice.step, 1)
        self.assertIsInstance(sp._over, list)

        sp = self.span(self.span(ls, 2))
        self.assertEqual(sp._over, ls)
        self.assertEqual(sp._slice.start, 2)
        self.assertEqual(sp._slice.stop, len(ls))
        self.assertEqual(sp._slice.step, 1)
        self.assertIsInstance(sp._over, list)

        sp = self.span(self.span(ls, 2, 5))
        self.assertEqual(sp._over, ls)
        self.assertEqual(sp._slice.start, 2)
        self.assertEqual(sp._slice.stop, 5)
        self.assertEqual(sp._slice.step, 1)
        self.assertIsInstance(sp._over, list)

        sp = self.span(self.span(ls, 2), 2)
        self.assertEqual(sp._over, ls)
        self.assertEqual(sp._slice.start, 4)
        self.assertEqual(sp._slice.stop, len(ls))
        self.assertEqual(sp._slice.step, 1)
        self.assertIsInstance(sp._over, list)

        sp = self.span(self.span(ls, 1, 5), 2)
        self.assertEqual(sp._over, ls)
        self.assertEqual(sp._slice.start, 3)
        self.assertEqual(sp._slice.stop, 5)
        self.assertEqual(sp._slice.step, 1)
        self.assertIsInstance(sp._over, list)

        sp = self.span(self.span(ls, 1, 6), 2, 4)
        self.assertEqual(sp._over, ls)
        self.assertEqual(sp._slice.start, 3)
        self.assertEqual(sp._slice.stop, 5)
        self.assertEqual(sp._slice.step, 1)
        self.assertIsInstance(sp._over, list)

    def test_index_get(self):
        ls = [1, 2, 3, 4, 5, 6, 7, 8]

        sp = self.span(ls)
        self.assertEqual(sp[0], 1)
        self.assertEqual(sp[2], 3)
        self.assertEqual(sp[4], 5)
        with self.assertRaises(IndexError):
            test_var = sp[8]

        sp = self.span(ls, 3)
        self.assertEqual(sp[0], 4)
        self.assertEqual(sp[2], 6)
        self.assertEqual(sp[4], 8)
        with self.assertRaises(IndexError):
            test_var = sp[5]

        sp = self.span(ls, 2, 5)
        self.assertEqual(sp[0], 3)
        self.assertEqual(sp[1], 4)
        self.assertEqual(sp[2], 5)
        with self.assertRaises(IndexError):
            test_var = sp[3]

        sp = self.span(ls, step=-1)
        self.assertEqual(sp[0], 8)
        self.assertEqual(sp[1], 7)
        self.assertEqual(sp[2], 6)
        self.assertEqual(sp[5], 3)
        with self.assertRaises(IndexError):
            test_var = sp[8]

        sp = self.span(ls, 2, step=2)
        self.assertEqual(sp[0], 3)
        self.assertEqual(sp[1], 5)
        self.assertEqual(sp[2], 7)
        with self.assertRaises(IndexError):
            test_var = sp[4]

        sp = self.span(ls, 2, step=-1)
        self.assertEqual(sp[0], 8)
        self.assertEqual(sp[1], 7)
        self.assertEqual(sp[2], 6)
        self.assertEqual(sp[5], 3)
        with self.assertRaises(IndexError):
            test_var = sp[6]

        sp = self.span(ls, 2, 5, step=-1)
        self.assertEqual(sp[0], 5)
        self.assertEqual(sp[1], 4)
        self.assertEqual(sp[2], 3)
        with self.assertRaises(IndexError):
            test_var = sp[3]

        sp = self.span(ls, 2, 5, step=2)
        self.assertEqual(sp[0], 3)
        self.assertEqual(sp[1], 5)
        with self.assertRaises(IndexError):
            test_var = sp[2]

    def test_eq(self):
        ls = [1, 2, 3, 4, 5]
        self.assertEqual(self.span(ls), ls)
        self.assertEqual(self.span(ls, 1, 4), [2, 3, 4])
        self.assertEqual(self.span(ls, 3, 4), [4])
        self.assertEqual(self.span(ls, 1, step=-1), [5, 4, 3, 2])
        self.assertEqual(self.span(ls, step=2), [1, 3, 5])
        self.assertEqual(self.span(ls, step=-2), [5, 3, 1])

        tpl = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
        self.assertEqual(self.span(tpl, 4, 7), [4, 5, 6])
        self.assertEqual(self.span(tpl, end=7, step=-2), [6, 4, 2, 0])
        self.assertEqual(self.span(tpl, 2, step=3), [2, 5, 8])

        ls = [1, 2, 3, 1, 2, 3, 3, 2, 1]
        self.assertEqual(self.span(ls, 0, 3), self.span(ls, 3, 6))
        self.assertEqual(self.span(ls, 3, 6), self.span(ls, 6, 9, -1))

    def test_ne(self):
        ls = [1, 2, 3, 4, 5, 6, 7, 8]

        self.assertNotEqual(self.span(ls), [1, 2, 3])
        self.assertNotEqual(self.span(ls, step=-1), ls)
        self.assertNotEqual(self.span(ls, 2), ls)

    def test_lt(self):
        ls = [1, 2, 3, 4, 5, 6]

        self.assertLess(self.span(ls, end=5), ls)
        self.assertLess(self.span(ls, end=3), ls)
        self.assertLess(self.span([1, 1, 1, 1, 1, 1]), ls)
        self.assertLess(self.span([1, 2, 3, 4, 5, 5]), ls)
        self.assertLess(self.span([5, 5, 4, 3, 2, 1], step=-1), ls)

    def test_le(self):
        ls = [1, 2, 3, 4, 5, 6]

        self.assertLessEqual(self.span(ls, end=5), ls)
        self.assertLessEqual(self.span(ls, end=3), ls)
        self.assertLessEqual(self.span([1, 1, 1, 1, 1, 1]), ls)
        self.assertLessEqual(self.span([1, 2, 3, 4, 5, 5]), ls)
        self.assertLessEqual(self.span([5, 5, 4, 3, 2, 1], step=-1), ls)
        self.assertLessEqual(self.span(ls, end=6), ls)
        self.assertLessEqual(self.span([6, 5, 4, 3, 2, 1], step=-1), ls)
        self.assertLessEqual(
            self.span([1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6], step=2), ls)
        self.assertLessEqual(
            self.span([6, 6, 5, 5, 4, 4, 3, 3, 2, 2, 1, 1], step=-2), ls)

    def test_gt(self):
        ls = [1, 2, 3, 4, 5, 6]

        self.assertGreater(self.span([2]), ls)
        self.assertGreater(self.span(ls, 1), ls)
        self.assertGreater(self.span(ls, 5, 6), ls)
        self.assertGreater(self.span(ls, 2, step=2), ls)
        self.assertGreater(self.span(ls, step=-1), ls)
        self.assertGreater(self.span([1, 2, 3, 4, 5, 7]), ls)
        self.assertGreater(self.span([1, 2, 3, 4, 5, 6, 1]), ls)

    def test_ge(self):
        ls = [1, 2, 3, 4, 5, 6]

        self.assertGreaterEqual(self.span([2]), ls)
        self.assertGreaterEqual(self.span(ls, 1), ls)
        self.assertGreaterEqual(self.span(ls, 5, 6), ls)
        self.assertGreaterEqual(self.span(ls, 2, step=2), ls)
        self.assertGreaterEqual(self.span(ls, step=-1), ls)
        self.assertGreaterEqual(self.span([1, 2, 3, 4, 5, 7]), ls)
        self.assertGreaterEqual(self.span([1, 2, 3, 4, 5, 6, 1]), ls)
        self.assertGreaterEqual(self.span(ls), ls)
        self.assertGreaterEqual(self.span([6, 5, 4, 3, 2, 1], step=-1), ls)
        self.assertGreaterEqual(
            self.span([1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6], step=2), ls)
        self.assertGreaterEqual(
            self.span([6, 6, 5, 5, 4, 4, 3, 3, 2, 2, 1, 1], step=-2), ls)

    def test_len(self):
        self.assertEqual(len(self.span([1, 2, 3])), 3)
        self.assertEqual(len(self.span([3, 2, 1], step=-1)), 3)
        self.assertEqual(len(self.span([1, 2, 3, 4], 2)), 2)
        self.assertEqual(len(self.span([1, 2, 3], step=2)), 2)
        self.assertEqual(len(self.span([1, 2, 3, 4], step=2)), 2)
        self.assertEqual(len(self.span([1, 2, 3, 4], end=3)), 3)
        self.assertEqual(len(self.span([1, 2, 3, 4], 1, 3, -1)), 2)
        self.assertEqual(len(self.span([1, 2, 3, 4, 5], step=-2)), 3)
        self.assertEqual(len(self.span([1, 2, 3, 4, 5], end=4)), 4)

    def test_reversed(self):
        pass

    def test_contains(self):
        pass

    def test_iter(self):
        pass

    def test_repr(self):
        pass

    def test_str(self):
        pass


class TestSpan(TestReadOnlySpan):
    # Span has the exact same functionality as ReadOnlySpan
    # however, it also includes index setting
    span = Span

    def test_index_set(self):
        ls = [1, 2, 3, 4]
        sp = self.span(ls)
        sp[1] = 9
        sp[3] = 15
        self.assertEqual(ls[1], 9)
        self.assertEqual(ls[3], 15)

        ls = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        sp = self.span(ls, 5, 7)
        sp[0] = 20
        sp[1] = 60
        self.assertEqual(ls[5], 20)
        self.assertEqual(ls[6], 60)
        with self.assertRaises(IndexError):
            sp[2] = 99

        ls = [9, 8, 7, 6, 5, 4, 3]
        sp = self.span(ls, 3, 5)
        sp[0] = 15
        sp[1] = 51
        self.assertEqual(ls[3], 15)
        self.assertEqual(ls[4], 51)
        with self.assertRaises(IndexError):
            sp[2] = 40


if __name__ == "__main__":
    unittest.main()
