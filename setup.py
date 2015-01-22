from setuptools import setup, find_packages
import os

version = '0.0.1'

setup(
    name='transportion_management',
    version=version,
    description='An app to manage transportation vehicles, keep record of transfers, advances, PF, fule provided',
    author='Arun Logistics',
    author_email='bhupesh00gupta@gmail.com',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=("frappe",),
)
