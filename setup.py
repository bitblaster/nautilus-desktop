from distutils.core import setup

setup(name="nautilus-desktop",
      version="0.1",
      description="A nautilus extension to create desktop entries",
      author="David Seebacher",
      author_email="dseebacher@gmail.com",
      url="https://github.com/dseebacher/nautilus-desktop",
      license="MIT",
      data_files=[('/usr/share/nautilus-python/extensions', ['nautilus-desktop/nautilusdesktop.py', 'nautilus-desktop/nautilusdesktop.glade'])])
