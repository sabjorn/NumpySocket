import setuptools

setuptools.setup(name='numpysocket',
  version='1.0.0',
  description='TCP/IP Socket for Sending Numpy Arrays',
  long_description=open('README.md').read().strip(),
  long_description_content_type="text/markdown",
  author="Steven A. Bjornson",
  author_email='info@sabjorn.net',
  url='',
  packages=["numpysocket"],
  install_requires=['numpy'],
  license='MIT License',
  zip_safe=False,
  keywords='',
  classifiers=['']
)
