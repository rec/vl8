from pathlib import Path
from setuptools import setup

_classifiers = [
    'Development Status :: 3 - Alpha',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
]


def _version():
    with open('vl8.py') as fp:
        line = next(i for i in fp if i.startswith('__version__'))
        return line.strip().split()[-1].strip("'")


REQUIREMENTS = Path('requirements.txt').read_text().splitlines()


if __name__ == '__main__':
    setup(
        name='vl8',
        version=_version(),
        author='Tom Ritchford',
        author_email='tom@swirly.com',
        url='https://github.com/rec/vl8',
        py_modules=['vl8'],
        description='🔉 vl8: Sort audio granularly 🔉',
        long_description=open('README.rst').read(),
        license='MIT',
        classifiers=_classifiers,
        keywords=['audio'],
        install_requires=REQUIREMENTS,
    )
