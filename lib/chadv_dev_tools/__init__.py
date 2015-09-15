# Copyright 2015 Chad Versace <chad@kiwitree.net>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
# * Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
# * Neither the name of the copyright holder nor the names of copyright
#   holder's contributors may be used to endorse or promote products
#   derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
# TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os
import os.path
from copy import copy

from subprocess import check_call

class Pkg:

    # Default USE flags shared by *all* packages
    USE = ['-debug']

    def __init__(self):
        self.USE.extend(Pkg.USE)
        self.__final_use_flags = None

    @property
    def src_dir(self):
        return os.getcwd()

    @property
    def final_use_flags(self):
        if self.__final_use_flags is not None:
            return self.__final_use_flags

        final_flags = []
        env_flags = os.environ.get('USE', '').split(',')

        for default_flag in self.USE:
            if default_flag[0] not in ('+', '-'):
                raise Exception(("default use flag {!r} is not prefixed "
                                 "with '+' or '-'".format(default_flag)))

            # The flag stripped of its +/- prefix.
            base_flag = default_flag[1:]

            # Environment USE flags override default flags.
            if (base_flag in env_flags) or ('+' + base_flag in env_flags):
                final_flags.append('+' + base_flag)
                continue
            elif '-' + base_flag in env_flags:
                final_flags.append('-' + base_flag)
                continue
            else:
                final_flags.append(default_flag)

        self.__final_use_flags = final_flags
        return self.__final_use_flags

    def use_enable(self, configure_args, use_flag, enable_flag=None):
        """Append an enable option 'configure_args' if 'use_flag' is
        enabled."""
        raise NotImplementedError

    def use(self, flag):
        """Return bool."""

        # Flag must not be prefixed.
        assert(flag[0] != '+')
        assert(flag[0] != '-')

        for x in self.final_use_flags:
            if x == flag or x == '+' + flag:
                return True
            elif x == '-' + flag:
                return False

        return False

    def configure_args(self):
        """Return [str]."""
        raise NotImplementedError

    def cmd_show_use_flags(self, args=[]):
        print(' '.join(self.final_use_flags))

    def cmd_configure(self, extra_args=[]):
        raise NotImplementedError

class AutotoolsPkg(Pkg):

    def use_enable(self, configure_args, use_flag, enable_flag=None):
        if enable_flag is None:
            enable_flag = use_flag

        if self.use(use_flag):
            configure_args.append('--enable-' + enable_flag)

    def autoreconf(self):
        if not os.path.exists(os.path.join(self.src_dir, 'configure')):
            check_call(['autoreconf', '-vfi'], cwd=self.src_dir)

    @property
    def configure_args(self):
        """Return [str]."""

        args = []

        prefix = os.environ.get('PREFIX', None)
        if prefix is not None and len(prefix) > 0:
            args.append('--prefix=' + prefix)

        cflags = os.environ.get('CFLAGS', '')
        cxxflags = os.environ.get('CXXFLAGS', '')
        if self.use('debug'):
            cflags += ' -g3 -O0'
            cxxflags += ' -g3 -O0'
        args.append('CFLAGS=' + cflags)
        args.append('CXXFLAGS=' + cxxflags)

        return args

    def cmd_configure(self, extra_args=[]):
        if not os.path.exists(os.path.join(self.src_dir, 'configure')):
            check_call(['autoreconf', '-vfi'], cwd=self.src_dir)

        args = ['./configure'] + self.configure_args + extra_args
        check_call(args, cwd=self.src_dir)

class CMakePkg(Pkg):

    def use_enable(self, configure_args, use_flag, enable_flag=None):
        if enable_flag is None:
            enable_flag = use_flag

        if self.use(use_flag):
            configure_args.append('--enable-' + enable_flag)

    @property
    def configure_args(self):
        args = ['-GNinja']

        build_type = ''
        prefix = os.environ.get('PREFIX', None)
        cflags = os.environ.get('CFLAGS', '')
        cxxflags = os.environ.get('CXXFLAGS', '')

        if prefix is not None and len(prefix) > 0:
            args.append('-DCMAKE_INSTALL_PREFIX=' + prefix)
            args.append('-DCMAKE_INSTALL_LIBDIR=lib')

        if self.use('debug'):
            build_type = 'Debug'
            cflags += ' -g3 -O0'
            cxxflags += ' -g3 -O0'

        args.append('-DCMAKE_BUILD_TYPE=Debug')
        args.append('-DCMAKE_C_FLAGS=' + cflags)
        args.append('-DCMAKE_CXX_FLAGS=' + cxxflags)

        return args

    def cmd_configure(self, extra_args=[]):
        args = ['cmake'] + self.configure_args + extra_args + ['.']
        check_call(args, cwd=self.src_dir)
