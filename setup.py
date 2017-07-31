from setuptools import setup, find_packages
import sys, os

VERSION = '0.5.0'

setup(name='MehtaneBudgetModel',
      version=VERSION,
      description="",
      long_description="""""",
      classifiers=[],
      keywords='Deep-Learning multi-omics survival data integration',
      author='o_poirion',
      author_email='o.poirion@gmail.com',
      url='',
      license='MIT',
      packages=find_packages(exclude=['examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'numpy',
          'scipy',
          'seaborn'
      ],
      )
