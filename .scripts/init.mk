# Makefile boilerplate

# custom shell for coloring + timing
SHELL=.scripts/makeshell $(or $@,-)

# disable command echoing, will be done by makeshell
.SILENT:
