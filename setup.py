from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    README = f.read()

setup(
    name='imp-json',
    version='0.1.0',
    description='import JSON directly in python',
    long_description=README,
    py_modules=['impjson'],
    install_requires=[],
    tests_require=[
        'pytest',
        'pytest-cov'
    ],
    test_suite='pytest'
)
