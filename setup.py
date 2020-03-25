from setuptools import setup, find_packages

with open("README.md", "r") as fh:
      long_description = fh.read()

setup(
      name='ac2_tools',
      version='0.1',
      description='Ubiquti airControl2 API helper',
      author='Denis Bezrodnykh',
      author_email='denis.bee@gmail.com',
      url='https://github.com/denisbee/ac2_tools',
      python_requires='>=3.5',
      packages=find_packages(),
      long_description=long_description,
      long_description_content_type="text/markdown",
      install_requires=[ 'requests' ]
)
