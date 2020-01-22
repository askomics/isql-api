from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requires = f.read().splitlines()

setup(
    name='isql-api',
    version='2.1.1',
    description='''
        Rest API to use virtuoso isql commands through HTTP.
    ''',
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Flask",
        "Topic :: Internet :: WWW/HTTP",
    ],
    maintainer='Xavier Garnier',
    maintainer_email='xavier.garnier@irisa.fr',
    url='https://github.com/xgaia/virtuoso-isql-http',
    keyword='virtuoso rest api http isql',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
    scripts=['isqlapi.py'],
)
