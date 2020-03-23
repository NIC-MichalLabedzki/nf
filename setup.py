import setuptools

class MakeRelease(setuptools.Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        print(" => make_release: START")

        import subprocess

        print(" ->  readme")
        exit_code = subprocess.call(['rst2html5.py', '-v', '--exit-status=2', 'README.rst', 'nf.html'])
        if exit_code != 0:
            print(" ->  readme: failed, exit code {}".format(exit_code))
            return 1

        print(" ->  dist")
        exit_code = subprocess.call(['rm', '-rf', 'dist'])
        exit_code = subprocess.call(['python3', 'setup.py', 'sdist', 'bdist_wheel'])
        if exit_code != 0:
            print(" ->  dist: failed, exit code {}".format(exit_code))
            return 1

        print(" => make_release: DONE")

setuptools.setup(
    version='1.5.0.dev0',
    install_requires=[
        'win10toast-persist ; platform_system=="Windows"',
        'paramiko ; platform_system=="Windows"',
        'psutil ; platform_system=="Windows"'
        ],
    extras_require={
        'optionals': [ 'paramiko', 'plyer', 'psutil' ]
        },
    cmdclass={
        'make_release': MakeRelease
        },
)
