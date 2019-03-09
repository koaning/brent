import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


base_packages = ["numpy>=1.15.4", "scipy>=1.2.0", "scikit-learn>=0.20.2",
                 "pandas>=0.23.4", "matplotlib>=3.0.2", "networkx>=2.2",
                 "graphviz>=0.10.1"]

setup(
    name="brent",
    version="0.2.3",
    packages=find_packages(exclude=['data', 'notebooks']),
    long_description=read('readme.md'),
    keywords=['causal', 'bayesian', 'graphical', 'model', 'inference'],
    python_requires='>=3.6',
    install_requires=base_packages,
    extras_require={
        "dev": ["flake8>=3.6.0", "pytest>=3.3.1", "pdoc3>=0.5.2",
                "nbval>=0.9.1", "plotnine>=0.5.1", "twine>=1.13.0"]
    },
    classifiers=['Intended Audience :: Developers',
                 'Intended Audience :: Science/Research',
                 'Programming Language :: Python :: 3.6',
                 'Programming Language :: Python :: 3.7',
                 'Development Status :: 3 - Alpha',
                 'License :: OSI Approved :: MIT License',
                 'Topic :: Scientific/Engineering',
                 'Topic :: Scientific/Engineering :: Artificial Intelligence']
)
