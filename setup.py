from setuptools import setup
from setuptools import find_packages


config = {
    "name": "pastream",
    "packages": find_packages(),
    "entry_points": {
        "console_scripts": [
            "pastream=main:main"
        ]
    }
}

setup(**config)
