OUT = \
      output/mapcat_0.png \
      output/mapcat_1.png \
      output/mapcat_2.png

NEGATED = $(patsubst %.png,%_neg.png,$(OUT))

run:
	@./glcat.py

all: $(OUT) $(NEGATED)

.PHONY: view
view: $(OUT)
	eog $(OUT)

$(OUT): secondary

.SECONDARY: secondary
secondary: mapcat.py input/mono.png
	./mapcat.py

%.png: %.svg
	inkscape -e $@ $^
	mogrify -type Grayscale $@

%_neg.png: %.png
	convert -negate $^ $@

.PHONY: clean
clean:
	rm -f input/mono.png $(OUT)
