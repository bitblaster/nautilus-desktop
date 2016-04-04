all: install

install:
	mkdir -p ~/.local/share/nautilus-python/extensions/
	cp nautilusdesktop.py ~/.local/share/nautilus-python/extensions/
	cp nautilusdesktop.glade ~/.local/share/nautilus-python/extensions/
