try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup, Extension
import os.path
import re
from glob import glob

CLASSIFIERS = """
Development Status :: 5 - Production/Stable
Intended Audience :: Developers
License :: OSI Approved :: BSD License
Programming Language :: C
Programming Language :: Python :: 2
Programming Language :: Python :: 2.7
Programming Language :: Python :: 3
Programming Language :: Python :: 3.5
Programming Language :: Python :: 3.6
Programming Language :: Python :: 3.7
Programming Language :: Python :: 3.8
"""

dconv_source_files = glob("./deps/double-conversion/double-conversion/*.cc")
dconv_source_files.append("./lib/dconv_wrapper.cc")

module1 = Extension(
    "ujson",
    sources=dconv_source_files
    + [
        "./python/ujson.c",
        "./python/objToJSON.c",
        "./python/JSONtoObj.c",
        "./lib/ultrajsonenc.c",
        "./lib/ultrajsondec.c",
    ],
    include_dirs=["./python", "./lib", "./deps/double-conversion/double-conversion"],
    extra_compile_args=["-D_GNU_SOURCE"],
    extra_link_args=["-lstdc++", "-lm"],
)


def get_version():
    filename = os.path.join(os.path.dirname(__file__), "./python/version.h")
    file = None
    try:
        file = open(filename)
        header = file.read()
    finally:
        if file:
            file.close()
    m = re.search(r'#define\s+UJSON_VERSION\s+"(\d+\.\d+(?:\.\d+)?)"', header)
    assert m, "version.h must contain UJSON_VERSION macro"
    return m.group(1)


f = open("README.rst")
try:
    README = f.read()
finally:
    f.close()


setup(
    name="ujson",
    version=get_version(),
    description="Ultra fast JSON encoder and decoder for Python",
    long_description=README,
    ext_modules=[module1],
    author="Jonas Tarnstrom",
    author_email="jonas.tarnstrom@esn.me",
    download_url="https://github.com/esnme/ultrajson",
    platforms=["any"],
    url="http://www.esn.me",
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*",
    classifiers=[x for x in CLASSIFIERS.split("\n") if x],
)
