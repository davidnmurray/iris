# (C) British Crown Copyright 2016, Met Office
#
# This file is part of Iris.
#
# Iris is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Iris is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Iris.  If not, see <http://www.gnu.org/licenses/>.
"""Unit tests for the `iris.io.expand_filespecs` function."""

from __future__ import (absolute_import, division, print_function)
from six.moves import (filter, input, map, range, zip)  # noqa

# Import iris.tests first so that some things can be initialised before
# importing anything else.
import iris.tests as tests

import os
import tempfile
import shutil

import iris.io as iio


class TestExpandFilespecs(tests.IrisTest):

    def setUp(self):
        tests.IrisTest.setUp(self)
        self.tmpdir = tempfile.mkdtemp()
        self.fnames = ['a.foo', 'b.txt']
        for fname in self.fnames:
            with open(os.path.join(self.tmpdir, fname), 'w') as fh:
                fh.write('anything')

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_absolute_path(self):
        result = iio.expand_filespecs([os.path.join(self.tmpdir, '*')])
        expected = [os.path.join(self.tmpdir, fname) for fname in self.fnames]
        self.assertEqual(result, expected)

    def test_double_slash(self):
        product = iio.expand_filespecs(['//' + os.path.join(self.tmpdir, '*')])
        predicted = [os.path.join(self.tmpdir, fname) for fname in self.fnames]
        self.assertEqual(product, predicted)

    def test_relative_path(self):
        os.chdir(self.tmpdir)
        item_out = iio.expand_filespecs(['*'])
        item_in = [os.path.join(self.tmpdir, fname) for fname in self.fnames]
        self.assertEqual(item_out, item_in)

    def test_no_files_found(self):
        msg = 'b expanded to empty'
        with self.assertRaisesRegexp(IOError, msg):
            iio.expand_filespecs([self.tmpdir + '_b'])

    def test_files_and_none(self):
        msg = 'b expanded to empty.*expanded to .*b.txt'
        with self.assertRaisesRegexp(IOError, msg):
            iio.expand_filespecs([self.tmpdir + '_b',
                                 os.path.join(self.tmpdir, '*')])


if __name__ == "__main__":
    tests.main()