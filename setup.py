try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='price crawler',
    version='0.1',
    packages=['.'],
    url='http://localhost:5000',
    license='',
    author='Joe Doe',
    author_email='joe,doe@engineer.com',
    description='Price crawler',
    install_requires=[
        'flask-restplus',
        'Flask',
        'pymongo',
        'gunicorn',
        'bs4'
    ]
)