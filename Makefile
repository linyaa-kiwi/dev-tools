DESTDIR ?=
prefix ?= $(HOME)
bindir ?= $(prefix)/bin

-include config.mk

BINS := \
    bin/libdrm-configure \
    bin/libdrm-env \
    bin/mesa-configure \
    bin/mesa-env \
    bin/prefix-env \
    bin/waffle-config \
    $@

.PHONY: all
all:
	@

.PHONY: install
install:
	install -D -t $(DESTDIR)$(bindir) $(BINS)

