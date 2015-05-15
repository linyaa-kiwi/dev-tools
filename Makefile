DESTDIR =
prefix = $(HOME)/.local
bindir = $(prefix)/bin

BINS := \
    bin/libdrm-configure \
    bin/libdrm-env \
    bin/mesa-configure \
    bin/mesa-env \
    bin/prefix-env \
    $@

.PHONY: all
all:
	@

.PHONY: install
install:
	install -D -t $(DESTDIR)$(bindir) $(BINS)

