from setuptools import setup
setup(use_scm_version=True,
      install_requires=[
        'win10toast ; platform_system=="Windows"',
        'paramiko ; platform_system=="Windows"'
      ],
      extras_require={
        'optionals': [ 'paramiko', 'plyer', 'psutil' ]
      }
     )
