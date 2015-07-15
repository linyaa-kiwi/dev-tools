DESTDIR ?=
prefix ?= $(HOME)
bindir ?= $(prefix)/bin

-include config.mk

BINS := \
    libdrm-configure \
    mesa-configure \
    piglit-configure \
    prefix-env \
    waffle-configure \
    $@

.PHONY: all
all:
	@

.PHONY: install
install:
	@# After installing each set of files, append rules to uninstall.mk
	@# that remove those files.
	@printf >uninstall.mk '.PHONY: uninstall\n'
	@printf >>uninstall.mk 'uninstall:\n'
	@
	install -D -t $(DESTDIR)$(bindir) $(addprefix bin/,$(BINS))
	@printf >>uninstall.mk '\trm $(addprefix $(bindir)/,$(BINS))\n'
	@
	@printf >>uninstall.mk '\t# And finally remove uninstall.mk itself\n'
	@printf >>uninstall.mk '\trm uninstall.mk\n'

-include uninstall.mk
