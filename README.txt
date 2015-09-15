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


Turning on debug mode
=====================

Set the USE environment variable to "debug" before running any script.

Installing graphics libraries to a non-standard location
========================================================

0.  Check which mesa version you're running:

    $ glxinfo > /tmp/glxinfo-old.txt

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

6.  Check which mesa version you're running:

    $ glxinfo > /tmp/glxinfo-new.txt

    You should see that you're now running an updated version of mesa.
