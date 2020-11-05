from setuptools import setup, find_packages

# See note below for more information about classifiers
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: POSIX :: Linux',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

setup(
  name='SpyCam-Demo',
  version='0.0.1',
  description='A raspberry Pi operated pan/tilt camera which uses Computer Vision',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  # the URL of your package's home page e.g. github link
  author='Luca Barbas and Keagan Chasenski',
  author_email='3dkalucaphen@gmail.com',
  license='MIT', # note the American spelling
  classifiers=classifiers,
  keywords='Raspberry Pi', # used when people are searching for a module, keywords separated with a space
  packages=find_packages(),
  install_requires=['OpenCV, imutils'] # a list of other Python modules which this module depends on.  For example RPi.GPIO
)
