from setuptools import setup

tests_deps = [
    "flake8==6.0.0",
    "coverage",
]

extras = {"test": tests_deps}


def readfile(filename: str):
    with open(filename, "r+") as f:
        return f.read()


if __name__ == "__main__":
    setup(
        name="corona",
        version="0.0.0",
        description="Connects to data from rki and displays it",
        author="Omega1902",
        author_email="27062486+Omega1902@users.noreply.github.com",
        url="",
        py_modules=["corona"],
        license=readfile("LICENSE"),
        entry_points={"console_scripts": ["corona = corona:cli"]},
        tests_deps=tests_deps,
        extras_require=extras,
    )
