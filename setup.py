import setuptools

setuptools.setup(name='numpysocket',
                 version='0.2.1',
                 description='TCP/IP Socket for Sending Numpy Arrays',
                 long_description=open('README.md').read().strip(),
                 author="Steven A. Bjornson",
                 author_email='info@sabjorn.net',
                 url='',
                 py_modules=['numpysocket'],
                 install_requires=['numpy'],
                 license='MIT License',
                 zip_safe=False,
                 keywords='',
                 classifiers=[''])
