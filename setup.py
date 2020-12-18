from setuptools import setup, find_packages

setup(
 name='PyAST',
 version='0.1.0',
 author='Francesco Cavarretta',
 author_email='francescocavarretta@hotmail.it',
 packages=find_packages(),
 scripts=[],
 url='',
 license='',
 description='Package for Artificial Spike Train generation based on Abbasi et al 2000',
 long_description='',
 install_requires=[
     "numpy"
 ],
)
