#
# Make file for python
# Author : Sunil bn
#

build:

test:

.PHONY: clean
clean:
	-rm Server/*.pyc Server/*~
	-rm Client/*.pyc Client/*~
	-rm *~
