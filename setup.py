from setuptools import setup

tests_deps = [
    "flake8==6.0.0",
    "coverage",
]

extras = {"test": tests_deps}

if __name__ == "__main__":
    setup(tests_deps=tests_deps, extras_require=extras)
