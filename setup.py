import setuptools
#from packagename.version import Version

setuptools.setup(name='Numpy Socket',
                 version='0.1.0',
                 description='TCP/IP Socket for Sending Numpy Arrays',
                 long_description=open('README.md').read().strip(),
                 author="Steven A. Bjornson",
                 author_email='info@sabjorn.net',
                 url='',
                 py_modules=['numpysocket.numpysocket'],
                 install_requires=['numpy'],
                 license='MIT License',
                 zip_safe=False,
                 keywords='',
                 classifiers=[''])
