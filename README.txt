Chad's Development Tools

Summary
=======
These are little scripts that I use to for setting up my environment, building
projects, etc.

There are no stability guarantees here, other than "it works for me".


How to Install
==============
These scripts don't require installation. You can execute them directly from
the git checkout. For example, suppose you have cloned Mesa to ~/src/mesa and
these dev-tools to ~/src/chadv-dev-tools. Then you can configure Mesa with the
mesa-configure script as follows:

    $ cd ~/src/mesa
    $ ~/src/chadv-dev-tools/mesa-configure

However, these scripts also work correctly if executed from an installed
location. If you prefer to install them, then:

    1. Configure:

        $ cp config.mk.example config.mk
        $ ed config.mk

    2. Build and install:

        $ make
        $ make install


USE flags
=========
The "USE" environment variable modifies the behavior of the configure scripts
(such as 'mesa-configure'). Its value is a space-separated list of flags,
called "USE flags". This project borrowed the concept of USE flags from
Gentoo's Portage buildsystem.

Some USE flags are common to all configure scripts, such as the "debug" flag.
Some USE flags are specific to a particular set of projects, such as the "dri3"
USE flag which affects only the configuration of projects that use DRI3.

Each flag listed in the USE environment variable, if prefixed with "-",
disables a particular project feature. Each flag, if prefixed with "+" or if it
has no prefix, enables a particular project feature.

Each project has a default list of USE flags defined in the Python variable
lib/chadv_dev_tools/${project}.py:Pkg.USE. The list of USE flags defined in
the environment modifies on the project's default list. The script
${project}-show-use-flags prints the USE flags that script ${project}-configure
would use, as currently defined by the environment and the project's defaults.

Example: Mesa
-------------
Suppose the default USE flags defined by lib/chadv_dev_tools/mesa.py is:

    USE="gbm dri3 x11 wayland surfaceless"

Verify the defaults:

    $ mesa-show-use-flags
    +gbm +dri3 +x11 +wayland +surfaceless

Try temporarily disabling the 'dri3' USE flag:

    $ USE="-dri3" mesa-show-use-flags
    +gbm -dri3 +x11 +wayland +surfaceless
    $ USE="" mesa-show-use-flags
    +gbm +dri3 +x11 +wayland +surfaceless

To disable DRI3 support when configuring Mesa, run:

    $ USE="-dri3" mesa-configure

To configure Mesa in debug mode (as opposed to release mode), and additionally
disable support for DRI3 and EGL's surfaceless platform, run:

    $ USE="debug -dri3,-surfaceless" mesa-configure

For Mesa, USE="debug" instructs mesa-configure to pass the following options to
Mesa's Autoconf configure script:

    * CFLAGS="-g3 -O0"
    * CXXFLAGS="-g3 -O0"
    * --enable-debug, which is a non-standard Autoconf option specific to Mesa



Installing graphics libraries to a non-standard location
========================================================

0.  Check which Mesa version you're running. Later, after installing a custom
    Mesa, we'll verify the installation by confirming that the active Mesa
    version has changed.

    $ glxinfo > /tmp/glxinfo-old.txt
    $ grep Mesa /tmp/glxinfo-old.txt

1.  Edit config.mk to have the prefix you want.

2.  Run
    $ make; make install

    If you look into your prefix bin directory, you should now see the
    following:

    $ ls $PREFIX/bin/
    libdrm-configure  mesa-configure  prefix-env  waffle-configure

3.  Run the script to set up all mesa environment variables with that
    prefix, and execute a new bash environment:

    $ cd $PREFIX

    $ bin/prefix-env exec --prefix=$PREFIX bash

    Or, if you want a debug build:
    $ USE="debug" bin/prefix-env exec --prefix=$PREFIX bash

4.  Change directories into your libdrm repository, and configure libdrm with the
    libdrm-configure script:

    $ libdrm-configure --prefix=$PREFIX

    Or, if you want a debug build:
    $ USE="debug" libdrm-configure --prefix=$PREFIX

    Then `make; make install`.

5.  Change directories into your mesa repository, and configure mesa with the
    mesa-configure script:

    $ mesa-configure --prefix=$PREFIX

    Or, if you want a debug build:
    $ USE="debug" mesa-configure --prefix=$PREFIX

6.  Confirm that the environment's Mesa version matches the version you
    installed. It should differ from the Mesa version we checked earlier.

    $ glxinfo > /tmp/glxinfo-new.txt
    $ grep Mesa /tmp/glxinfo-new.txt
