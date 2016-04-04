from setuptools import setup

setup(
    name='bio-it',
    author='Jacob Feala',
    author_email='jake@outlierbio.com',
    version='0.1',
    url='http://github.com/outlierbio/bio-it',
    packages=['bioit'],
    description='Demo for Bio-IT 2016 presentation',
    include_package_data=True,
    install_requires=[
        'boto3'
    ]
)