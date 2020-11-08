from setuptools import setup, find_packages

def get_long_description():
    with open('README.md') as f:
        return f.read()

setup(
    name='timelog',
    version='0.1.0',

    description="Timelog is a way to log your time in markdown-similar text file",

    long_description=get_long_description(),
    long_description_content_type='text/markdown',

    python_requires='>=3.7',

    install_requires=[
        'click>=7.1.0'
    ],

    extras_require={
        'test': ['pytest', 'pytest_click'],
    },

    packages=find_packages(),
    scripts=['scripts/timelog'],

    author='ice1e0',
    license='MIT',

    entry_points={}
)