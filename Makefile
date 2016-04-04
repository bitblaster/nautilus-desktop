all: install

install:
	mkdir -p ~/.local/share/nautilus-python/extensions/
	cp extension.py ~/.local/share/nautilus-python/extensions/
