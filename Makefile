
.PHONY: build clean

build:
	pyinstaller --name neuroART --windowed --distpath ./release/build --workpath ./release/dist init.py


clean:
	rm -rf release
