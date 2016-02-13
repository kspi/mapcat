view: out.png
	eog out.png

out.png: mapcat.py input/mono.png
	./mapcat.py

input/mono.png: input/mono.svg
	inkscape -e $@ $^
