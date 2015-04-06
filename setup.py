from setuptools import setup, find_packages


setup(
    name='blimey',
    version='0.9.4',
    description='A password management library with AgileKeychain (1Password) support',
    author='Open Password Team',
    author_email='niko@nevala.fi',
    url='https://github.com/openpassword/blimey',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Topic :: Security',
        'Topic :: Security :: Cryptography',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4'
    ],
    keywords='password management 1password agilekeychain',
    packages=find_packages(exclude=['specs*']),
    package_data={
        'blimey': ['agile_keychain/template/*.template']
    },
    install_requires=[
        'pbkdf2',
        'pycrypto',
        'jinja2'
    ]
)
