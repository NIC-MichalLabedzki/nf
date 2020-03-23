import setuptools

VERSION = '1.5.0.dev0'

class MakeRelease(setuptools.Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        print(" => make_release: START")

        import subprocess

        def git_status():
            print(" ->  git status")
            output = subprocess.check_output(['git', 'status', '--porcelain', '--untracked=no'])
            if output:
                print(" ->  git status: failed, output: '{}'".format(output.decode()))
                return 1

        def readme():
            print(" ->  readme")
            exit_code = subprocess.call(['rst2html5.py', '-v', '--exit-status=2', 'README.rst', 'nf.html'])
            if exit_code != 0:
                print(" ->  readme: failed, exit code {}".format(exit_code))
                return 2

        def dist():
            print(" ->  dist")
            exit_code = subprocess.call(['rm', '-rf', 'dist'])
            exit_code = subprocess.call(['python3', 'setup.py', 'sdist', 'bdist_wheel'])
            if exit_code != 0:
                print(" ->  dist: failed, exit code {}".format(exit_code))
                return 3

        def version_check():
            print(" ->  version_check")
            exit_code = subprocess.call(['grep', '1.5.0', 'README.rst'])
            if exit_code != 0:
                print(" ->  version_check: failed, exit code {}".format(exit_code))
                return 4

        exit_code = git_status()
        if exit_code: return exit_code

        exit_code = readme()
        if exit_code: return exit_code

        exit_code = dist()
        if exit_code: return exit_code

        exit_code = version_check()
        if exit_code: return exit_code

        print(" => make_release: DONE")

setuptools.setup(
    version=VERSION,
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
