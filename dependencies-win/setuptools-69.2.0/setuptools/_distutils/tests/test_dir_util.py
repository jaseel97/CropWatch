"""Tests for distutils.dir_util."""
import os
import stat
import unittest.mock as mock

from distutils import dir_util, errors
from distutils.dir_util import (
    mkpath,
    remove_tree,
    create_tree,
    copy_tree,
    ensure_relative,
)

from distutils.tests import support
import pytest


@pytest.fixture(autouse=True)
def stuff(request, monkeypatch, distutils_managed_tempdir):
    self = request.instance
    tmp_dir = self.mkdtemp()
    self.root_target = os.path.join(tmp_dir, 'deep')
    self.target = os.path.join(self.root_target, 'here')
    self.target2 = os.path.join(tmp_dir, 'deep2')


class TestDirUtil(support.TempdirManager):
    def test_mkpath_remove_tree_verbosity(self, caplog):
        mkpath(self.target, verbose=0)
        assert not caplog.records
        remove_tree(self.root_target, verbose=0)

        mkpath(self.target, verbose=1)
        wanted = ['creating %s' % self.root_target, 'creating %s' % self.target]
        assert caplog.messages == wanted
        caplog.clear()

        remove_tree(self.root_target, verbose=1)
        wanted = ["removing '%s' (and everything under it)" % self.root_target]
        assert caplog.messages == wanted

    @pytest.mark.skipif("platform.system() == 'Windows'")
    def test_mkpath_with_custom_mode(self):
        # Get and set the current umask value for testing mode bits.
        umask = os.umask(0o002)
        os.umask(umask)
        mkpath(self.target, 0o700)
        assert stat.S_IMODE(os.stat(self.target).st_mode) == 0o700 & ~umask
        mkpath(self.target2, 0o555)
        assert stat.S_IMODE(os.stat(self.target2).st_mode) == 0o555 & ~umask

    def test_create_tree_verbosity(self, caplog):
        create_tree(self.root_target, ['one', 'two', 'three'], verbose=0)
        assert caplog.messages == []
        remove_tree(self.root_target, verbose=0)

        wanted = ['creating %s' % self.root_target]
        create_tree(self.root_target, ['one', 'two', 'three'], verbose=1)
        assert caplog.messages == wanted

        remove_tree(self.root_target, verbose=0)

    def test_copy_tree_verbosity(self, caplog):
        mkpath(self.target, verbose=0)

        copy_tree(self.target, self.target2, verbose=0)
        assert caplog.messages == []

        remove_tree(self.root_target, verbose=0)

        mkpath(self.target, verbose=0)
        a_file = os.path.join(self.target, 'ok.txt')
        with open(a_file, 'w') as f:
            f.write('some content')

        wanted = ['copying {} -> {}'.format(a_file, self.target2)]
        copy_tree(self.target, self.target2, verbose=1)
        assert caplog.messages == wanted

        remove_tree(self.root_target, verbose=0)
        remove_tree(self.target2, verbose=0)

    def test_copy_tree_skips_nfs_temp_files(self):
        mkpath(self.target, verbose=0)

        a_file = os.path.join(self.target, 'ok.txt')
        nfs_file = os.path.join(self.target, '.nfs123abc')
        for f in a_file, nfs_file:
            with open(f, 'w') as fh:
                fh.write('some content')

        copy_tree(self.target, self.target2)
        assert os.listdir(self.target2) == ['ok.txt']

        remove_tree(self.root_target, verbose=0)
        remove_tree(self.target2, verbose=0)

    def test_ensure_relative(self):
        if os.sep == '/':
            assert ensure_relative('/home/foo') == 'home/foo'
            assert ensure_relative('some/path') == 'some/path'
        else:  # \\
            assert ensure_relative('c:\\home\\foo') == 'c:home\\foo'
            assert ensure_relative('home\\foo') == 'home\\foo'

    def test_copy_tree_exception_in_listdir(self):
        """
        An exception in listdir should raise a DistutilsFileError
        """
        with mock.patch("os.listdir", side_effect=OSError()), pytest.raises(
            errors.DistutilsFileError
        ):
            src = self.tempdirs[-1]
            dir_util.copy_tree(src, None)
