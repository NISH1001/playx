from setuptools import setup

with open('LICENSE') as l:
    license = l.read()

with open('requirements.txt') as r:
    requirements = r.read().split('\n')

setup(name='playx',
      packages=['playx'],
      entry_points={
          'console_scripts': [
              'playx = playx.main:main'
          ]
      },
      version='0.0.1', # need input
      license=license,

      )
