from setuptools import setup
from setuptools import find_packages


setup(
    name="pastream",
    packages=find_packages(),
    entry_points={
        "gui_scripts": ["pastream=main:pastream_gui"]
    }
)