from setuptools import setup
setup(version='1.5.0.dev0',
      install_requires=[
        'win10toast-persist ; platform_system=="Windows"',
        'paramiko ; platform_system=="Windows"',
        'psutil ; platform_system=="Windows"'
      ],
      extras_require={
        'optionals': [ 'paramiko', 'plyer', 'psutil' ]
      }
     )
