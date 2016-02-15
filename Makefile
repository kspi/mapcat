OUT = mapcat_0.png mapcat_1.png mapcat_2.png

view: $(OUT)
	eog $(OUT)

$(OUT): mapcat.py input/mono.png
	./mapcat.py

input/mono.png: input/mono.svg
	inkscape -e $@ $^

clean:
	rm -f input/mono.png $(OUT)
