from glob import glob
from os.path import basename
from os.path import splitext

from setuptools import setup
from setuptools import find_packages


def _requires_from_file(filename):
    return open(filename).read().splitlines()


setup(
    name="panediv-nfw",
    version="0.1.1",
    license="MIT",
    description="Genelate layout template for tmuxinator.",
    long_description=open('README_PYPI.md').read(),
    long_description_content_type="text/markdown",
    author="nfwprod@gmail.com",
    url="https://github.com/nfwprod/panediv-nfw",
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    install_requires=_requires_from_file('requirements.txt'),
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "pytest-cov", "pyyaml", "pytest-datadir"],
    entry_points={
        "console_scripts": [
            "panediv=panediv.cli:run",
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
    ],
)
