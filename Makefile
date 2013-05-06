##################################################
# Makefile
##################################################

.PHONY : default, clean

default : 
	(cd parser; python parsing.py)
clean :
	(cd parser; rm -f *.pyc)
