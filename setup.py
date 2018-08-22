from setuptools import setup

# with open('LICENSE') as l:
#     license = l.read()

with open('requirements.txt') as r:
    requirements = r.read().split('\n')

setup(
    name='playx',
    packages=['playx'],
    author='NISH1001',
    author_email='nishanpantha@gmail.com',
    description='Search and play any song from terminal.',
    url='http://github.com/NISH1001/playx',
    entry_points={
        'console_scripts': [
            'playx = playx.main:main'
        ]
    },
    version='1.0.1',
    license='MIT',
    install_requires=requirements,
)
