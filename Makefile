

tmp/exercises.pdf: tmp/exercises.dvi
	cd tmp && dvipdf exercises.dvi

tmp/exercises.dvi: tmp/exercises.latex
	cd tmp && latex exercises.latex

tmp/exercises.latex: exercises.rst tmp
	rst2latex.py --documentoptions=letterpaper exercises.rst > tmp/exercises.latex

tmp:
	mkdir tmp
