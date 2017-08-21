import setuptools


setuptools.setup(
    name='web-daemon-ctl',
    version='1.0',
    description='Server for remote control daemons via web interface',
    author='dimastark',
    author_email='dstarkdev@gmail.com',
    entry_points={
        'console_scripts': [
            'web-daemon-ctl = web.main:main',
        ]
    },
    packages=setuptools.find_packages(
        '.',
        exclude=[
            '*.tests', '*.tests.*', 'tests.*', 'tests',
        ],
    ),
    package_data={'': []},
    include_package_data=True,
    install_requires=[
        'setuptools',
        'aiohttp',
    ],
    tests_require=['nose'],
    test_suite='nose.collector',
)
