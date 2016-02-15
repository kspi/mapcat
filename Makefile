OUT = \
      output/mapcat_0.png \
      output/mapcat_1.png \
      output/mapcat_2.png

.PHONY: view
view: $(OUT)
	eog $(OUT)

$(OUT): secondary

.SECONDARY: secondary
secondary: mapcat.py input/mono.png
	./mapcat.py

input/mono.png: input/mono.svg
	inkscape -e $@ $^
	mogrify -type Grayscale $@

.PHONY: clean
clean:
	rm -f input/mono.png $(OUT)
