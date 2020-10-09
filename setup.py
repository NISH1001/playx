from setuptools import setup

exec(open("playx/version.py").read())

setup(
    name="playx",
    packages=["playx", "playx.playlist"],
    author="NISH1001",
    author_email="nishanpantha@gmail.com",
    description="Search and play any song from terminal.",
    long_description="Search and play any song from terminal seamlessly.",
    url="http://github.com/NISH1001/playx",
    entry_points={"console_scripts": ["playx = playx.main:main"]},
    version=__version__,
    license="MIT",
    install_requires=["youtube_dl", "requests", "beautifulsoup4", "selenium", "lxml", "youtube_search"],
)
