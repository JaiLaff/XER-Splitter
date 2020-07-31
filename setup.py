from setuptools import setup, find_packages

with open("README.md", "r") as readme:
    long_description = readme.read()


setup(name='xersplitter',
      version='1.0.0',
      description='Split your Primavera P6 .XER files into CSV or XLSX files',
      long_description = long_description,
      long_description_content_type = "text/markdown",
      url='http://github.com/JaiLaff/XER-Splitter',
      author='Jai Lafferty',
      author_email='jai.lafferty@gmail.com',
      license='GPLv3',
      packages=find_packages(),
      zip_safe=False,
      python_requires='>=3.6',
      classifiers =[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Development Status :: 5 - Production/Stable"
    ],
      entry_points = {
        'console_scripts': ['xersplitter=xersplitter.Splitter:Main'],
    }
)