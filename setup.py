import os
import re
from setuptools import setup


dir_path = os.path.dirname(os.path.realpath(__file__))
init_string = open(os.path.join(dir_path, 'astroMetric', "__init__.py")).read()
VERS = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VERS, init_string, re.M)
__version__ = mo.group(1)


setup(
    name='astroMetric',
    url='https://github.com/ZechangSun/astroMetric',
    version=__version__,
    author='Zechang Sun',
    author_email='szc22@mails.tsinghua.edu.cn',
    license='MIT',
    packages=["astroMetric"],
    description='useful functions for mean/scatter/outlier fraction determination',
    long_description=open("README.md").read(),
    package_data={"": ["README.md", "LICENSE", "AUTHORS.md"]},
    include_package_data=True,
    install_requires=["numpy", "typing"],
    keywords=['bi-weight mean', 'bi-weight scatter', 'MAD', 'outlier fraction'],
    classifiers=["Development Status :: 3 - Alpha",
                 "License :: OSI Approved :: MIT License",
                 "Natural Language :: English",
                 "Programming Language :: Python :: 3.10",
                 "Operating System :: OS Independent",
                 "Topic :: Scientific/Engineering :: Astronomy",
                 "Intended Audience :: Science/Research"]
)