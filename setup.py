from setuptools import setup
setup(use_scm_version=True,
      install_requires=[
        'win10toast ; platform_system=="Windows"'
        ])
