from distutils.core import setup

with open('README.rst') as f:
    readme = f.read()

setup(
    name='pyvsc',
    version='0.1',
    description='VSC Losses Electrothermal Model',
    long_description=readme,
    author='Juan Manuel Mauricio',
    author_email='jmmauricio@us.es',
    packages=['pyvsc', 'pyvsc.tests'],
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.6',
    ]
)
