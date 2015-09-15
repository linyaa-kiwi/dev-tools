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

import chadv_dev_tools as dev

class Pkg(dev.AutotoolsPkg):

    USE = ['+gbm', '+dri3', '+x11', '+wayland', '+surfaceless']

    def __with_egl_platforms(self):
        """Return '--with-egl-platforms=...'.

        If USE_EGL_PLATFORMS is set, then USE flags are ignored for
        determining the EGL platforms.  platforms.  If USE_EGL_PLATFORMS is
        empty, then disable all EGL platforms.
        """

        env = os.environ.get('USE_EGL_PLATFORMS', None)
        if env is not None:
            return '--with-egl-platforms=' + env

        platforms = []

        if self.use('x11'):
            platforms.append('x11')
        if self.use('gbm'):
            platforms.append('drm')
        if self.use('wayland'):
            platforms.append('wayland')
        if self.use('surfaceless'):
            platforms.append('surfaceless')

        return '--with-egl-platforms=' + ','.join(platforms)

    @property
    def configure_args(self):
        args = super().configure_args

        args += [
            '--disable-osmesa',
            '--disable-vdpau',
            '--disable-xa',
            '--enable-dri',
            '--enable-egl',
            '--enable-gles1',
            '--enable-gles2',
            '--enable-glx',
            '--enable-glx-tls',
            '--enable-shared-glapi',
            '--enable-texture-float',
            '--with-dri-drivers=i965',
            '--with-gallium-drivers=',
            self.__with_egl_platforms(),
        ]

        self.use_enable(args, 'debug')
        self.use_enable(args, 'dri3')
        self.use_enable(args, 'gbm')

        return args
