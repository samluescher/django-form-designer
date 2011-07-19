import os
from distutils.core import setup
from subprocess import Popen, PIPE

def read(fname):
    """Utility function to read the README file.
    
    Used for the long_description.  It's nice, because now
    1) we have a top level README file and
    2) it's easier to type in the README file than to put a raw string in below ...
    """
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def call_git_describe(abbrev=4):
    try:
        p = Popen(['git', 'describe', '--abbrev=%d' % abbrev],
                  stdout=PIPE, stderr=PIPE)
        p.stderr.close()
        line = p.stdout.readlines()[0]
        return line.strip()

    except:
        return None


def read_release_version():
    try:
        f = open("RELEASE-VERSION", "r")

        try:
            version = f.readlines()[0]
            return version.strip()

        finally:
            f.close()

    except:
        return None


def write_release_version(version):
    f = open("RELEASE-VERSION", "w")
    f.write("%s\n" % version)
    f.close()


def get_git_version(abbrev=4):
    """
    Author: Douglas Creager <dcreager@dcreager.net>
    This file is placed into the public domain.
    
    Calculates the current version number. If possible, this is the
    output of 'git describe', modified to conform to the versioning
    scheme that setuptools uses. If 'git describe' returns an error
    (most likely because we're in an unpacked copy of a release tarball,
    rather than in a git working copy), then we fall back on reading the
    contents of the RELEASE-VERSION file.
        
    This function will automatically update the RELEASE-VERSION file, if
    necessary. Note that the RELEASE-VERSION file should *not* be
    checked into git; please add it to your top-level .gitignore file.
    
    You'll probably want to distribute the RELEASE-VERSION file in your
    sdist tarballs; to do this, just create a MANIFEST.in file that
    contains the following line:
    
    include RELEASE-VERSION
    
    """
    # Read in the version that's currently in RELEASE-VERSION.

    release_version = read_release_version()

    # First try to get the current version using 'git describe'.

    version = call_git_describe(abbrev)

    # If that doesn't work, fall back on the value that's in
    # RELEASE-VERSION.

    if version is None:
        version = release_version

    # If we still don't have anything, that's an error.

    if version is None:
        raise ValueError("Cannot find the version number!")

    # If the current version is different from what's in the
    # RELEASE-VERSION file, update the file to be current.

    if version != release_version:
        write_release_version(version)

    # Finally, return the current version.

    return version

version = get_git_version()

if "a" in version:
    devstatus = "Development Status :: 3 - Alpha"
elif "b" in version:
    devstatus = "Development Status :: 4 - Beta"
else:
    devstatus = "Development Status :: 5 - Production/Stable"




setup(
    name = "django-form-designer",
    version = version,
    author = "Samuel Luescher",
    url = "http://github.com/philomat/django-form-designer",
    license = "BSD",
    description = ("A Django app for building many kinds of forms visually, without any programming knowledge."),
    packages = ['form_designer', 'form_designer.templatetags'],
    platforms = ['OS Independent'],
    long_description = read('README.md'),
    classifiers = [
        devstatus,
        "Programming Language :: Python",
        "Framework :: Django",
        "License :: OSI Approved :: BSD License",
        "Environment :: Web Environment",
    ],
)
