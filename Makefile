DESTDIR ?=
prefix ?= $(HOME)
bindir ?= $(prefix)/bin

-include config.mk

BINS := \
    bin/libdrm-configure \
    bin/mesa-configure \
    bin/prefix-env \
    bin/waffle-configure \
    $@

.PHONY: all
all:
	@

.PHONY: install
install:
	install -D -t $(DESTDIR)$(bindir) $(BINS)

