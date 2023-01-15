"""
setup.py
"""
from setuptools import setup

setup(
    name='microstructure-plotter',
    version='0.1',
    packages=['microplot', 'microplots.scripts'],
    setup_requires=['chaco==5.1.0','enable==5.3.1','traits==6.4.1','traitsui==7.4.2','pandas==1.3.5','pyqt'],
    url='https://github.com/will-thompson-k/microstructure-plotter',
    license='MIT',
    author='Will Thompson',
    author_email='',
    description='Visualize financial market data 📈 on infinitesimal timescales 🔎',
)