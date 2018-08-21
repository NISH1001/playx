from setuptools import setup

with open('LICENSE') as l:
    license = l.read()

with open('requirements.txt') as r:
    requirements = r.read().split('\n')

setup(name='playx',
      packages=['playx'],
      author='NISH1001',
      entry_points={
          'console_scripts': [
              'playx = playx.main:main'
          ]
      },
      version='0.0.1',
      license=license,
      install_requires=requirements,
      )
