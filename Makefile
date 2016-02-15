OUT = \
      output/mapcat_0.png \
      output/mapcat_1.png \
      output/mapcat_2.png

view: $(OUT)
	eog $(OUT)

$(OUT): mapcat.py input/mono.png
	./mapcat.py

input/mono.png: input/mono.svg
	inkscape -e $@ $^

clean:
	rm -f input/mono.png $(OUT)
