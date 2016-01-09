#!/usr/bin/env python
# encoding=utf8
from pip.req import parse_requirements
from os.path import dirname, join
from setuptools import setup


def read_requirements():
    filepath = join(dirname(__file__), 'requirements.txt')
    generator = parse_requirements(filepath, session=False)
    return [str(requirement.req) for requirement in generator]


def read(fname):
    return open(join(dirname(__file__), fname)).read()

README = read('README.rst')

setup(
    name="django-form-designer",
    version="0.8.0",
    url='https://github.com/samluescher/django-form-designer',
    license='BSD',
    description="Design contact forms, search forms etc from the Django admin,"
                " without writing any code. Integrates with Django CMS.",
    long_description=README,

    author='Samuel Luescher',
    author_email='sam at luescher dot org',
    install_requires=read_requirements(),
    packages=[
        'form_designer',
        'form_designer.migrations',
        'form_designer.templatetags',
        'form_designer.contrib',
        'form_designer.contrib.exporters',
        'form_designer.contrib.cms_plugins',
        'form_designer.contrib.cms_plugins.form_designer_form',
    ],
    package_data={
        'form_designer': [
            'static/form_designer/js/*.js',
            'templates/admin/form_designer/formlog/change_list.html',
            'templates/html/formdefinition/*.html',
            'templates/html/formdefinition/forms/*.html',
            'templates/html/formdefinition/forms/includes/*.html',
            'templates/txt/formdefinition/*.txt',
            'locale/*/LC_MESSAGES/*',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
