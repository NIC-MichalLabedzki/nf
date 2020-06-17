#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: 0BSD
#
# Original author: Michał Łabędzki
# Author email: michal.tomasz.labedzki@gmail.com
#
# Project name/application name: nf
# Source: https://github.com/NIC-MichalLabedzki/nf
#
# Usage:
#   ./nf.py [optional options] command [arg...]
#
##

# for python2
from __future__ import print_function as _print_function

nf_stored_code = None

def nf(argv=None):
    """
    This function does not exit python interpreter so can be used in other Python scripts.
    It is compatible with python 2 and 3. "argv" is list of strings - exactly the same arguments
    used in command line.

    For example:
    "nf(['-p', '-n', 'ls', '/etc'])"

    usage: nf.py [-h] [-l LABEL] [-p] [-n] [-s] [-w WAIT_FOR_PID] [--detach]
                [-b {paramiko,ssh,dbus,gdbus,notify-send,termux-notification,win10toast-persist,win10toast,plyer,plyer_toast,stdout}]
                [-v] [-d] [--debugfile DEBUGFILE]
                [--custom_notification_text CUSTOM_NOTIFICATION_TEXT]
                [--custom_notification_title CUSTOM_NOTIFICATION_TITLE]
                [--custom_notification_exit_code CUSTOM_NOTIFICATION_EXIT_CODE]
                cmd ...

    Simple command line tool to make notification after target program finished work

    positional arguments:
    cmd
    args

    optional arguments:
    -h, --help            show this help message and exit
    -l LABEL, --label LABEL
                            Add humn readable text to custom job identification
    -p, --print           Print notification text in stdout too
    -n, --no-notify       Do not do annoying notifications
    -s, --save            Save/append command and stat to .nf file
    -w WAIT_FOR_PID, --wait-for-pid WAIT_FOR_PID
                            Wait for PID aka wait for already run process finish
                            work. This option can be used multiple times.
    --detach              Run command or wait for pid in detached process
    -b {paramiko,ssh,dbus,gdbus,notify-send,termux-notification,win10toast-persist,win10toast,plyer,plyer_toast,stdout}, --backend {paramiko,ssh,dbus,gdbus,notify-send,termux-notification,win10toast-persist,win10toast,plyer,plyer_toast,stdout}
                            Notification backend
    -v, --version         Print version
    -d, --debug           More print debugging on stdout
    --debugfile DEBUGFILE
                            More print debugging save into file
    --custom_notification_text CUSTOM_NOTIFICATION_TEXT
                            Custom notification text
    --custom_notification_title CUSTOM_NOTIFICATION_TITLE
                            Custom notification title
    --custom_notification_exit_code CUSTOM_NOTIFICATION_EXIT_CODE
                            Custom notification exit code

    Examples:
    nf make
    nf ls
    nf ls not_exist_file
    nf sleep 2
    nf -l sleeping sleep 2
    nf -l `tty` ls
    nf "ls | grep .py"
    nf --detach sleep 15
    nf -w 55555 ls
    nf -w 55555 --detach echo Finished
    nf -w 55555 -w 55556 echo Done

    "/home/nic/src/nf$ nf.py -p ls
    LICENSE  nf.py  pytest.ini  README  README.dev  requirements-dev.txt  setup.cfg  setup.py  tox.ini
    -----------------------------------------------------------
    "/home/nic/src/nf$ ls" finished work.

    Start time:   17:32.50
    End time:     17:32.50
    Elapsed time: 00:00.00
    -----------------------------------------------------------

    Use environment variables:
    KONSOLE_DBUS_SERVICE
    KONSOLE_DBUS_SESSION
    KONSOLE_VERSION
    SSH_CLIENT
    STY
    TMUX

    New in 1.1.0:
    -s, --save

    New in 1.2.0:
    -b, --backend {paramiko, ssh, dbus,notify-send,termux-notification,win10toast,plyer,plyer_toast,stdout}
    -b ssh
    -b paramiko
    -b plyer
    -b plyer_toast
    --custom_notification_text CUSTOM_NOTIFICATION_TEXT
    --custom_notification_title CUSTOM_NOTIFICATION_TITLE
    --custom_notification_exit_code CUSTOM_NOTIFICATION_EXIT_CODE
    -d, --debug

    New in 1.3.0:
    -b gdbus

    New in 1.4.0:
    -b win10toast-persist
    --detach
    -w, --wait-for-pid WAIT_FOR_PID

    """
    VERSION = '1.5.0.dev0'
    import argparse
    import datetime
    import os
    import sys
    import time  # python 2 time.time() instead of datetime.datetime.timestamp()

    EXAMPLES = '''
Examples:
 nf make
 nf ls
 nf ls not_exist_file
 nf sleep 2
 nf -l sleeping sleep 2
 nf -l `tty` ls
 nf "ls | grep .py"
 nf --detach sleep 15
 nf -w 55555 ls
 nf -w 55555 --detach echo Finished
 nf -w 55555 -w 55556 echo Done

 "/home/nic/src/nf$ nf.py -p ls
 LICENSE  nf.py  pytest.ini  README  README.dev  requirements-dev.txt  setup.cfg  setup.py  tox.ini
 -----------------------------------------------------------
 "/home/nic/src/nf$ ls" finished work.

 Start time:   17:32.50
 End time:     17:32.50
 Elapsed time: 00:00.00
 -----------------------------------------------------------
 '''

    def print_stdout(*arg, **karg):
        try:
            print(*arg, **karg)
        except Exception as e:
            try:
                log('cannot print on stdout: ', *arg)
            except:
                pass

    def process_exec(cmdline):
        p_stdout = ''
        p_stderr = None
        exit_code = None
        try:
            import subprocess
            p = subprocess.Popen(cmdline, shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            p_stdout, p_stderr = p.communicate()
            exit_code = p.returncode
            log('process{} - exit code:{} stdout={} stderr={}:'.format(cmdline, exit_code, p_stdout, p_stderr))

        except Exception as e:
            log('screen - exit code:{} stdout={} stderr={}  exception:'.format(exit_code, p_stdout, p_stderr), e)

        return p_stdout

    parser = argparse.ArgumentParser(description='Simple command line tool to make notification after target program finished work', epilog=EXAMPLES, formatter_class=argparse.RawDescriptionHelpFormatter, add_help=False)

    parser.add_argument('-h', '--help', action="store_true", help='show this help message and exit')
    parser.add_argument('-l', '--label', type=str, help='Add human readable text to custom job identification')
    parser.add_argument('-p', '--print', action="store_true", help='Print notification text in stdout too')
    parser.add_argument('-n', '--no-notify', action="store_true", help='Do not do annoying notifications')
    parser.add_argument('-s', '--save', action="store_true", help='Save/append command and stat to .nf file')
    parser.add_argument('-w', '--wait-for-pid', type=int, action='append',help='Wait for PID aka wait for already run process finish work. This option can be used multiple times.')
    parser.add_argument('--detach', action="store_true", help='Run command or wait for pid in detached process')

    parser.add_argument('-b', '--backend', type=str, choices=['paramiko', 'ssh', 'wsl', 'dbus', 'gdbus', 'notify-send', 'termux-notification', 'win10toast-persist', 'win10toast', 'plyer', 'plyer_toast', 'stdout'], help='Notification backend')
    parser.add_argument('-v', '--version', action="store_true", help='Print version')
    parser.add_argument('-d', '--debug', action="store_true", help='More print debugging on stdout')
    parser.add_argument('--debugfile', type=str, help='More print debugging save into file')
    parser.add_argument('--custom_notification_text', type=str, help='Custom notification text')
    parser.add_argument('--custom_notification_title', type=str, help='Custom notification title')
    parser.add_argument('--custom_notification_exit_code', type=int, help='Custom notification exit code')

    parser.add_argument('--env-unset', type=str, help='Modify environment - unset variable')
    parser.add_argument('--env-set-default', type=str, help='Modify environment - set variable if not set; KEY=value')

    parser.add_argument('--try-version', type=str, help='Download and run specific nf version: tag, branch, commit hash or "list" to display possible tags/versions. Try "master" for latest development version.')
    parser.add_argument('cmd', nargs='?')
    parser.add_argument('args', nargs=argparse.REMAINDER)

    if argv == None:
        argv = sys.argv[1:]
    if argv:
        if '--version' in argv or '-v' in argv:
            index_version = argv.index('--version') if '--version' in argv else argv.index('-v')
            index_try_version = -1
            index_cmd = -1
            for arg in argv:
                if index_cmd == -1 and not arg.startswith('-'):
                    index_cmd = argv.index(arg)
                if arg.startswith('--try-version'):
                    index_try_version = argv.index(arg)
            if (index_version < index_cmd or index_cmd == -1) and (index_version < index_try_version or index_try_version == -1):
                print_stdout(VERSION)
                return 0

        if len(argv) == 0:
            help_text = parser.format_help()
            print_stdout(help_text)
            return 0

        if '--help' in argv or '-h' in argv:
            index_help = argv.index('--help') if '--help' in argv else argv.index('-h')
            index_try_version = -1
            index_cmd = -1
            for arg in argv:
                if index_cmd == -1 and not arg.startswith('-'):
                    index_cmd = argv.index(arg)
                if arg.startswith('--try-version'):
                    index_try_version = argv.index(arg)
            if (index_help < index_cmd or index_cmd == -1) and (index_help < index_try_version or index_try_version) == -1:
                help_text = parser.format_help()
                print_stdout(help_text)
                return 0
    else:
        help_text = parser.format_help()
        print_stdout(help_text)
        return 0

    args = parser.parse_args(argv)

    logfile = {'handle': None}
    def log(*arg):
        try:
            debug_prefix = 'DEBUG:    '
            current_time = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S.%f")
            if args.debug is True:
                argss = []
                for a in arg:
                    argss.append('{}'.format(a).replace('\n', '\n{}'.format(debug_prefix)))
                try:
                    print('DEBUG {}: {}'.format(current_time, ' '.join(argss)))
                except:
                    pass
            if args.debugfile is not None:
                argss = []
                for a in arg:
                    argss.append('{}'.format(a).replace('\n', '\n{}'.format(debug_prefix)))
                if logfile['handle'] is None:
                    logfile['handle'] = open(args.debugfile, 'a+b', 0)
                logfile['handle'].write('DEBUG {}: {}\n'.format(current_time, ' '.join(argss)).encode())
        except Exception as e:
            # print(e)
            pass

    log('nf version={}'.format(VERSION))
    log('python {}'.format(sys.version_info))
    log('platform {}'.format(sys.platform))
    is_wsl = False
    try:
        if sys.platform.startswith('linux'):
            with open('/proc/version') as f:
                v = f.read()
                is_wsl = True if 'Microsoft' in v else False
    except Exception as e:
        log('cannot detect wsl: ', e)
    log('is_wsl {}'.format(is_wsl))


    nf_used_environ_var = [
        # non-direct
        'DBUS_SESSION_BUS_ADDRESS',
        'DISPLAY',

        'KONSOLE_DBUS_SERVICE',
        'KONSOLE_DBUS_SESSION',
        'KONSOLE_VERSION',
        'SSH_CLIENT',
        'STY',
        'TMUX',

        # nothing special, all programs using environment/OS subtools use it
        'PATH'
    ]

    for env in nf_used_environ_var:
        log('env var: {}={}'.format(env, repr(os.environ.get(env))))

    if args.env_unset and args.env_unset in os.environ:
        del os.environ[args.env_unset]
    if args.env_set_default:
        s = args.env_set_default.split('=')
        if s[0] not in os.environ:
            os.environ[s[0]] = s[1]

    for env in nf_used_environ_var:
        log('final env var: {}={}'.format(env, repr(os.environ.get(env))))

# TODO
# find ls -t ~/.dbus/session-bus/ | head -n 1

    import sysconfig
    try:
        abi = '{}-{}'.format(sysconfig.get_python_version(), sysconfig.get_platform())
        try:
            if sys.version_info.major >= 3 and sys.version_info.minor >= 2:
                abi = 'abi_{}-{}'.format(sys.abiflags, abi)
        except Exception as e:
            log('abiabiflags error', e)
        if sys.version_info.major >= 3 and sys.version_info.minor >= 3:
            abi = '{}-{}'.format(sys.implementation.name, abi)
    except Exception as e:
        log('abi general error', e)
    log('abi {}'.format(abi))

    log('argv {}'.format(sys.argv))
    log('args {}'.format(args))

    def windows_to_wsl_path(win_path):
        try:
            wsl_path = process_exec(['wslpath', '-a', '-u', win_path]).decode().strip('"\n')
        except Exception as e:
            log('wspath exit error', e)
            return None

        log('windows_to_wsl_path return', wsl_path)
        return wsl_path

    NF_DIR = '.nfdir'
    nf_dir = os.path.join(os.path.expanduser('~'), NF_DIR)
    nf_dir_win_for_wsl = nf_dir # None? nf_dir for manual testing under linux
    if is_wsl:
        try:
            output = process_exec(['cmd.exe', '/c', 'echo %USERPROFILE%'])
            if output:
                user_dir_win = output.decode().rstrip('\r\n')
                user_dir_win_for_wsl = windows_to_wsl_path(user_dir_win)
                if user_dir_win_for_wsl is None:
                    nf_dir_win_for_wsl = nf_dir
                else:
                    nf_dir_win_for_wsl = os.path.join(user_dir_win_for_wsl, NF_DIR)
        except Exception as e:
            log('cannot get user directory', e)

    log('nf dir: {}'.format(nf_dir))
    log('nf dir win for wsl: {}'.format(nf_dir_win_for_wsl))

# functions (used more than once) ----------------------------------------------

    def which(cmd):
        path = None
        try:
            import shutil

            path = shutil.which(cmd)
        except Exception as e:
            log('which by shutil failed:', e)
            try:
                import distutils.spawn

                path = distutils.spawn.find_executable(cmd)
            except Exception as e:
                log('which by distutils failed', e)
        return path

    def get_ssh():
        import os
        ssh_ip = None
        ssh_port = None

        if 'TMUX' in os.environ:
            output = None
            try:
                output = process_exec(['tmux', 'show-environment', 'SSH_CLIENT'], shell=False).decode().strip()
                log('cmd: {} output'.format(cmdline_args), output)
                if output == '-SSH_CLIENT':
                    log('no ssh in tmux')
                else:
                    ssh_connection = output[11:].split(' ')
                    log('ssh in tmux:', ssh_connection)
                    ssh_ip = ssh_connection[0]
                    ssh_port = ssh_connection[2]
            except Exception as e:
                log('{} failed: {}'.format('tmux show-environment SSH_CLIENT', output), e)

        if (ssh_ip is None or ssh_port is None) and 'SSH_CLIENT' in os.environ:
            ssh_connection = os.environ['SSH_CLIENT'].split(' ')
            ssh_ip = ssh_connection[0]
            ssh_port = ssh_connection[2]
        log('debug ssh: ', ssh_ip, ssh_port)
        return (ssh_ip, ssh_port)


    def call_dbus(service_name, path, method, *arg):
        app = which('qdbus')
        if app is not None:
            log('which qdbus: {}'.format(app))

            xarg = []
            for a in arg:
                if a.startswith('int32:'):
                    a = a[6:]
                xarg.append(a)
            tool_cmdline = [app, service_name, path, method]
            tool_cmdline.extend(xarg)
        else:
            app = which('gdbus')
            if app is not None:
                log('which gdbus: {}'.format(app))

                xarg = []
                for a in arg:
                    if a.startswith('int32:'):
                        xarg.append(a[6:])
                    else:
                        xarg.append(a)
                tool_cmdline = [app, 'call', '--session', '--dest', service_name, '--object-path', path, '--method', '{}.{}'.format(service_name, method)]
                tool_cmdline.extend(xarg)
            else:
                app = which('dbus-send')
                if app is not None:
                    log('which dbus-send: {}'.format(app))
                    tool_cmdline = [app, '--session', '--print-reply=literal', '--dest={}'.format(service_name), path, '{}.{}'.format(service_name, method)]
                    tool_cmdline.extend(xarg)
                else:
                    log('cannot find dbus backend')

        log('dbus cmdline', tool_cmdline)

        output = process_exec(tool_cmdline).decode().strip()
        log('dbus backend output', output)

        if app == which('gdbus'):
            output = output.strip('(),')
        if app == which('dbus-send'):
            if 'int32' in output:
                output = output.split(' ')[1]
        log('dbus final output', output)

        return output


    def download_file(url, download_dir, output_filename):
        import ssl
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        data = ''
        try:
            import urllib.request
            request = urllib.request.urlopen(url, context=ctx)
            data = request.read()
        except Exception as e:
            log('urllib for python3 failed', e)
            try:
                import urllib
                request = urllib.urlopen(url, context=ctx)
                data = request.read()
            except Exception as e:
                log('urllib for python2 failed', e)
        if data == '':
            print_stdout('ERROR: Cannot download file: {}'.format(url))
            return 1

        downloaded_file = os.path.join(download_dir, output_filename)
        with open(downloaded_file, 'wb') as f:
            f.write(data)

    def nf_cleanup():
        if logfile['handle'] is not None:
            try:
                logfile['handle'].write('\n'.encode())
                logfile['handle'].close()
            except Exception as e:
                print_stdout('nf error while saving debugfile', e)

#-------------------------------------------------------------------------------

    if args.try_version:
        if args.try_version == 'list':
            url = 'https://api.github.com/repos/NIC-MichalLabedzki/nf/tags'
        else:
            url = 'https://github.com/NIC-MichalLabedzki/nf/raw/{}/nf.py'.format(args.try_version)

        import ssl
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        data = ''
        try:
            import urllib.request
            request = urllib.request.urlopen(url, context=ctx)
            data = request.read()
        except Exception as e:
            log('urllib for python3 failed', e)
            try:
                import urllib
                request = urllib.urlopen(url, context=ctx)
                data = request.read()
            except Exception as e:
                log('urllib for python2 failed', e)
        if data == '':
            print_stdout('ERROR: Cannot download specified nf version for: {}'.format(args.try_version))
            nf_cleanup()
            return 1

        if args.try_version == 'list':
            import json
            tags = json.loads(data.decode())
            print_stdout(' '.join([tag['name'] for tag in tags]))
        else:
            import subprocess
            try_version_index = 0
            for index, arg in enumerate(sys.argv[0:]):
                if arg.startswith('--try-version'):
                    try_version_index = index
                    if not arg.startswith('--try-version='):
                        try_version_index += 1
            new_argv = sys.argv[try_version_index + 1:]
            new_argv.insert(0, '-')
            new_argv.insert(0, sys.executable)
            log('run nf[{}] {}'.format(args.try_version, ' '.join(new_argv)))
            python_process = subprocess.Popen(new_argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, stderr_output = python_process.communicate(data)
            print_stdout(output.decode().rstrip('\n'))
            print(stderr_output.decode(), file=sys.stderr)

        nf_cleanup()
        return 0

    try:
        import signal

        def sigint_handler(signum, frame):
            signal.signal(signal.SIGINT, signal.default_int_handler)
            signal.signal(signal.SIGINT, sigint_handler)

        signal.signal(signal.SIGINT, sigint_handler)
    except Exception as e:
        log('signal exception', e)

    if args.backend is not None:
        backend = args.backend
    else:
        backend = 'stdout'

    if not args.no_notify:
        if (backend in ['stdout', 'paramiko'] and args.backend == None) or args.backend == 'paramiko':
            try:
                ssh_ip, ssh_port = get_ssh()

                if ssh_ip is not None and ssh_port is not None:
                    import paramiko
                    ssh_client = paramiko.SSHClient()
                    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    try:
                        ssh_client.load_system_host_keys()
                    except Exception as e:
                        log('backend={}'.format('paramiko'), e)
                    try:
                        ssh_client.connect(hostname=ssh_ip, port=ssh_port, timeout=2)
                    except Exception as e:
                        exc_info = sys.exc_info()
                        log('traceback {line} backend={backend}'.format(line=exc_info[-1].tb_lineno, backend='paramiko'), e)
                        import traceback
                        traceback.print_exception(*exc_info)
                        log('end ----')
                        try:
                            import getpass
                            password = getpass.getpass()
                            ssh_client.connect(hostname=ssh_ip, port=ssh_port, password=password, timeout=2)
                            del password
                        except Exception as e:
                            log('backend={}'.format('paramiko'), e)
                            backend = 'stdout'
                else:
                    if args.backend == 'paramiko':
                        print_stdout('nf: WARNING: No $SSH_CLIENT, backend "paramiko" will not work')
                    backend = 'stdout'
            except Exception as e:
                log('backend={}'.format('paramiko'), e)
                backend = 'stdout'

        if (backend in ['stdout', 'ssh'] and args.backend == None) or args.backend == 'ssh':
            try:
                ssh_ip, ssh_port = get_ssh()
                if ssh_ip is not None and ssh_port is not None:
                    import subprocess

                    try:
                        ssh_process = subprocess.Popen(["ssh", ssh_ip , '-p', ssh_port, '-o', 'StrictHostKeyChecking=no', '-o', 'ConnectTimeout=2', '-o', 'PreferredAuthentications=publickey', '-o', 'PubkeyAuthentication=yes'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        time.sleep(1)
                        if ssh_process.poll() != None:
                            raise Exception('Public key not working')
                    except Exception as e:
                        log('backend={}'.format('ssh'), e)
                        ssh_process = subprocess.Popen(["ssh", ssh_ip , '-p', ssh_port, '-o', 'ConnectTimeout=2', '-o', 'PreferredAuthentications=password', '-o', 'PubkeyAuthentication=no'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        ssh_process.stdout.readline()  # expect password prompt
                    if ssh_process.poll():
                        backend = 'stdout'
                    else:
                        backend = 'ssh'
                else:
                    if args.backend == 'ssh':
                        print_stdout('nf: WARNING: No $SSH_CLIENT, backend SSH will not work')
                    backend = 'stdout'
            except Exception as e:
                log('backend={}'.format('ssh'), e)
                backend = 'stdout'

        backend_internal = {}

        if is_wsl or (args.backend == 'wsl' and is_wsl is not True):
            python_exe = which('python.exe')
            log('type python.exe before', python_exe)

            environ = os.environ.copy()

            nf_dependencies_dir = os.path.join(nf_dir, 'dependencies')
            nf_current_deps_dir = os.path.join(nf_dependencies_dir, '{}.{}.{}'.format(sys.version_info.major, sys.version_info.minor, sys.version_info.micro), 'platform_unknown')
            pip_target_dir = os.path.join(nf_current_deps_dir, 'pip')
            nf_pip_done = os.path.join(pip_target_dir, 'nf_done')
            if not os.path.exists(nf_pip_done):
                cmd_exit_code = 0
                try:
                    cmdline_args = [sys.executable, '-m', 'pip', 'install', 'pip', '--target', pip_target_dir]
                    import subprocess
                    p = subprocess.Popen(cmdline_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    output, stderr_output = p.communicate()
                    cmd_exit_code = p.returncode
                    log('install pip stdout\n', output.decode())
                    log('install pip stderr\n', stderr_output.decode())
                    log('install pip exit code', cmd_exit_code)
                    if cmd_exit_code == 0:
                        os.mkdir(nf_pip_done)
                except Exception as e:
                    log('download pip failed for: <{}> exit code {}'.format(cmdline_args, cmd_exit_code), e)
                    print_stdout('ERROR: Cannot make notification under Windows - cannot download newer "pip"')

            if not os.path.exists(nf_pip_done):
                download_dir = os.path.join(nf_dir, 'downloaded')
                import os
                try:
                    os.makedirs(download_dir)
                except:
                    pass
                    # TODO

                downloaded_file = os.path.join(download_dir, 'get-pip.py')
                if not os.path.exists(downloaded_file):
                    download_file('https://bootstrap.pypa.io/get-pip.py', download_dir, 'get-pip.py')

                cmd_exit_code = 0
                try:
                    cmdline_args = [sys.executable, downloaded_file, 'pip', '--target', pip_target_dir]
                    import subprocess
                    p = subprocess.Popen(cmdline_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    output, stderr_output = p.communicate()
                    cmd_exit_code = p.returncode
                    log('install pip stdout\n', output.decode())
                    log('install pip stderr\n', stderr_output.decode())
                    log('install pip exit code', cmd_exit_code)
                    if cmd_exit_code == 0:
                        os.mkdir(nf_pip_done)
                except Exception as e:
                    log('download pip failed for: <{}> exit code {}'.format(cmdline_args, cmd_exit_code), e)
                    print_stdout('ERROR: Cannot make notification under Windows - cannot download newer "pip"')
# TODO

            if os.path.exists(nf_pip_done):
                if 'PYTHONPATH' not in environ:
                    environ['PYTHONPATH'] = os.path.abspath(pip_target_dir)
                else:
                    environ['PYTHONPATH'] = os.path.abspath(pip_target_dir) + ':' + environ['PYTHONPATH']
                import site;
                site.addsitedir(os.path.abspath(pip_target_dir))

            nf_remote_deps_dir = os.path.join(nf_dir_win_for_wsl, 'dependencies', '3.8.2', 'win_amd64')
            win_module_target_dir = os.path.join(nf_remote_deps_dir, 'win10toast-persist')
            nf_win_module_done = os.path.join(win_module_target_dir, 'nf_done')
            if not os.path.exists(win_module_target_dir):
                cmd_exit_code = 0
                try:
                    cmdline_args = [sys.executable, '-m', 'pip', 'install', 'win10toast-persist', '--platform', 'win_amd64', '--python-version', '3.8.2', '--only-binary=:all:', '--target', win_module_target_dir]
                    import subprocess
                    p = subprocess.Popen(cmdline_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=environ)
                    output, stderr_output = p.communicate()
                    cmd_exit_code = p.returncode
                    log('install win10toast-persist stdout\n', output.decode())
                    log('install win10toast-persist stderr\n', stderr_output.decode())
                    log('install win10toast-persist exit code', cmd_exit_code)
                    if cmd_exit_code == 0:
                        os.mkdir(nf_win_module_done)
                except Exception as e:
                    log('download win10toast-persist failed for: <{}> exit code {}'.format(cmdline_args, cmd_exit_code), e)
                    print_stdout('ERROR: Cannot make notification under Windows - cannot download backend module - win10toast-persist')

            download_dir = os.path.join(nf_dir, 'wsl', 'python', 'zip')
            import os
            try:
                os.makedirs(download_dir)
            except:
                pass
                # TODO

            new_python_dir = os.path.join(nf_dir_win_for_wsl, 'wsl', 'python', '3.8.2')
            downloaded_file = os.path.join(download_dir, 'python.zip')
            if not os.path.exists(downloaded_file):
                download_file('https://www.python.org/ftp/python/3.8.2/python-3.8.2-embed-amd64.zip', download_dir, 'python.zip')
                #download_file('https://www.python.org/ftp/python/3.8.2/python-3.8.2-embed-win32.zip', download_dir)

                try:
                    os.makedirs(new_python_dir)
                except Exception as e:
                    log('cannot create dirs', new_python_dir)

            if not os.path.exists(os.path.join(new_python_dir, 'python.exe')):
                try:
                    import zipfile
                    with zipfile.ZipFile(downloaded_file, 'r') as file_zip:
                        file_zip.extractall(new_python_dir)
                except Exception as e:
                    log('cannot unzip custom python', e)

            os.environ["PATH"] = os.path.abspath(new_python_dir) + os.pathsep + os.environ["PATH"]
            sys.path.insert(0, os.path.abspath(new_python_dir))

            python_exe = which('python.exe')
            log('type python.exe after set', python_exe)
            python_exe = os.path.join(new_python_dir, 'python.exe')
            #os.chmod(python_exe, 0o777)
            log('type python.exe after set ensure', python_exe)
            python_x = which('python')
            log('type python after set', python_x)

            if sys.platform != 'win32' and is_wsl is not True: # NOTE: just for testing without Win
                python_exe = 'python'

            backend = 'wsl'

        if (sys.platform == 'win32' and backend in ['stdout', 'win10toast-persist'] and args.backend == None) or args.backend == 'win10toast-persist':
            try:
# TODO: platform detect
                module_win_path = os.path.join(nf_dir, 'dependencies', '{}.{}.{}'.format(sys.version_info.major, sys.version_info.minor, sys.version_info.micro), 'win_amd64', 'win10toast-persist')
                if os.path.exists(module_win_path):
                    import site;
                    site.addsitedir(os.path.abspath(module_win_path))

                module_win_path = os.path.join(nf_dir, 'dependencies', '3.8.2', 'win_amd64', 'win10toast-persist')
                if os.path.exists(module_win_path):
                    import site;
                    site.addsitedir(os.path.abspath(module_win_path))

                import win10toast
                backend = 'win10toast-persist'
            except Exception as e:
                log('backend={}'.format('win10toast-persist'), e)
                backend = 'stdout'

        if (sys.platform == 'win32' and backend in ['stdout', 'win10toast'] and args.backend == None) or args.backend == 'win10toast':
            try:
                import win10toast
                backend = 'win10toast'
            except Exception as e:
                log('backend={}'.format('win10toast'), e)
                backend = 'stdout'

        if (backend in ['stdout', 'dbus'] and args.backend == None) or args.backend == 'dbus':
            try:
                import dbus

                dbus_session = dbus.SessionBus()
                if dbus_session is not None:
                    backend_internal['dbus_session'] = dbus_session
                    dbus_notification = dbus_session.get_object('org.freedesktop.Notifications', '/org/freedesktop/Notifications')
                    if dbus_notification is not None:
                        backend_internal['dbus_notification'] = dbus_notification
                        backend = 'dbus'
                    else:
                        backend = 'stdout'
                else:
                    backend = 'stdout'
            except Exception as e:
                log('backend={}'.format('dbus'), e)
                backend = 'stdout'

        if (backend in ['stdout', 'gdbus'] and args.backend == None) or args.backend == 'gdbus':
            try:
                gdbus_app = which('gdbus')
                log('backend={}'.format('gdbus'), gdbus_app)
                if gdbus_app is not None:
                    backend = 'gdbus'
                else:
                    backend = 'stdout'
            except Exception as e:
                log('backend={}'.format('gdbus'), e)
                backend = 'stdout'

        if (backend in ['stdout', 'notify-send'] and args.backend == None) or args.backend == 'notify-send':
            try:
                notify_send_app = which('notify-send')
                log('backend={}'.format('notify-send'), notify_send_app)
                if notify_send_app is not None:
                    backend = 'notify-send'
                else:
                    backend = 'stdout'
            except Exception as e:
                log('backend={}'.format('notify-send'), e)
                backend = 'stdout'

        if (backend in ['stdout', 'termux-notification'] and args.backend == None) or args.backend == 'termux-notification':
            try:
                termux_notification_app = which('termux-notification')
                if termux_notification_app is not None:
                    backend = 'termux-notification'
                else:
                    backend = 'stdout'
            except Exception as e:
                log('backend={}'.format('termux-notification'), e)
                backend = 'stdout'

        if (backend in ['stdout', 'plyer', 'plyer_toast'] and args.backend == None) or args.backend == 'plyer' or args.backend == 'plyer_toast':
            try:
                import plyer
                if args.backend == 'plyer' or args.backend == 'plyer_toast':
                    backend = args.backend
            except Exception as e:
                log('backend={}'.format('plyer'), e)
                backend = 'stdout'

        if backend == 'stdout' and args.backend != 'stdout':
            print_stdout("nf: WARNING: Could not get backend, notification will not work", file=sys.stderr)
    log('choosen backend is {}'.format(backend))

    cmd = None
    if args.cmd is None:
        if args.wait_for_pid is not None:
            cmd= "wait for pids {}".format(args.wait_for_pid)
# TODO: store on nf start and print here processes names
        else:
            cmd = 'nf'
    else:
        cmd = args.cmd

    notify__title = cmd

    log('part cmdline cmd', args.cmd)
    log('part cmdline args', args.args)
    cmdline = cmd + (' ' + ' '.join(args.args) if len(args.args) > 0 else '')
    if args.label is not None:
        notify__title += ' (' + args.label + ')'

    time_start = datetime.datetime.now()

    import shlex
    import subprocess

    run_cmd = cmdline
    cmdline_args = cmdline
    system_shell = True
    shell = None
    shell_cmdline = None
    exit_code = 0

    parent_names = []
    try:
        import psutil

        process_info = psutil.Process(os.getpid())
        ppid = process_info.ppid()
        parents = process_info.parents()
        parent_names = [parent.name() for parent in parents]

        if 'tmux: server' in parent_names:
            tmux_cmdline = ['tmux', 'display-message', '-p', '"#{client_pid}"']
            multiplexer_client_pid = int(process_exec(tmux_cmdline).decode().strip('"\n'))
            log('tmux multiplexer_client_pid {}'.format(multiplexer_client_pid))
            tmux_process_info = psutil.Process(multiplexer_client_pid)
            tmux_parents = tmux_process_info.parents()
            parent_names.extend([parent.name() for parent in tmux_parents])
        parent_process_info = psutil.Process(ppid)
        parent_process_info_exe = parent_process_info.exe()
        parent_process_info_cmdline = parent_process_info.cmdline()
    except Exception as e:
        log('psutil failed'.format(backend), e)
        parents = []
        parent_process_info_exe = ''
        parent_process_info_cmdline = ['']

        try:
            ppid = os.getppid()
            parent_process_info_exe = os.readlink('/proc/{}/exe'.format(ppid))
            log('exe', parent_process_info_exe)

            with open('/proc/{}/cmdline'.format(ppid)) as f:
                parent_process_info_cmdline = f.read()[0:-1].split('\0')
                log('cmdline', parent_process_info_cmdline)

            pid = ppid
            while pid != 1:
                pid_exe = os.readlink('/proc/{}/exe'.format(pid))
                parent_name = os.path.basename(pid_exe)
                if 'tmux: server' == parent_name:
                    multiplexer_client_pid = int(process_exec(['tmux', 'display-message', '-p', '"#{client_pid}"']).decode().strip('"\n'))
                    log('tmux multiplexer_client_pid {}'.format(multiplexer_client_pid))
                    pid = multiplexer_client_pid
                parent_names.append(parent_name)
                with open('/proc/{}/stat'.format(pid)) as f:
                    other_process_info_stat = f.read().split(' ')
                    pid = int(other_process_info_stat[3])
        except Exception as e:
            log('usinng /proc failed'.format(backend), e)

    # GUI: yakuake, konsole
    try:
        log('shell parents', parent_names)
        konsole_app_index = parent_names.index('konsole') if 'konsole' in parent_names else None
        yakuake_app_index = parent_names.index('yakuake') if 'yakuake' in parent_names else None
        log('detect konsole {} yakuake {}'.format(konsole_app_index, yakuake_app_index))
        if yakuake_app_index is not None and konsole_app_index is not None:
            if konsole_app_index < yakuake_app_index:
                gui_app = 'konsole'
            elif konsole_app_index > yakuake_app_index:
                gui_app = 'yakuake'
        elif konsole_app_index is not None:
            gui_app = 'konsole'
        elif yakuake_app_index is not None:
            gui_app ='yakuake'
        elif 'KONSOLE_VERSION' in os.environ:
            gui_app = 'konsole'
        else:
             gui_app = 'unknown'
        log('gui_app {}'.format(gui_app))

        gui_app_tab_name = None
        if gui_app == 'yakuake':
            # SESSION_ID=$(qdbus org.kde.yakuake /yakuake/sessions activeSessionId)
            # qdbus org.kde.yakuake /yakuake/tabs tabTitle ${SESSION_ID}
            try:
                import dbus
                gui_app_dbus_session = dbus.SessionBus()
                if gui_app_dbus_session is not None:
                    dbus_object = gui_app_dbus_session.get_object('org.kde.yakuake', '/yakuake/sessions')
                    if dbus_object is not None:
                        session_id = dbus_object.activeSessionId()
                        dbus_object = gui_app_dbus_session.get_object('org.kde.yakuake', '/yakuake/tabs')
                        gui_app_tab_name = dbus_object.tabTitle(session_id)
            except Exception as e:
                log('yakuake get tab name exception1'.format(backend), e)

                try:
                    active_session_id = call_dbus('org.kde.yakuake', '/yakuake/sessions', 'activeSessionId')
                    gui_app_tab_name = call_dbus('org.kde.yakuake', '/yakuake/tabs', 'tabTitle', 'int32:' + active_session_id)

                except Exception as e:
                    log('yakuake get tab name exception2'.format(backend), e)
        elif gui_app == 'konsole':
            # $KONSOLE_DBUS_SERVICE $KONSOLE_DBUS_SESSION title 1
            try:
                import dbus
                gui_app_dbus_session = dbus.SessionBus()
                if gui_app_dbus_session is not None:
                    dbus_object = gui_app_dbus_session.get_object(os.environ['KONSOLE_DBUS_SERVICE'], os.environ['KONSOLE_DBUS_SESSION'])
                    gui_app_tab_name = dbus_object.title(1)
            except Exception as e:
                log('yakuake get tab name exception1'.format(backend), e)

                try:
                    gui_app_tab_name = call_dbus(os.environ['KONSOLE_DBUS_SERVICE'], os.environ['KONSOLE_DBUS_SESSION'], 'title', 'int32:1')

                except Exception as e:
                    try:
                        gui_app_tab_name = call_dbus('org.kde.konsole', os.environ['KONSOLE_DBUS_SESSION'], 'title', 'int32:1')
                    except Exception as e:
                        log('yakuake get tab name exception3'.format(backend), e)
                    log('yakuake get tab name exception2'.format(backend), e)

        log('gui_app_tab_name', gui_app_tab_name)

        # text multiplexers: tmux, screen
        tmux_app_index = parent_names.index('tmux: server') if 'tmux: server' in parent_names else None
        screen_app_index = parent_names.index('screen') if 'screen' in parent_names else None
        if tmux_app_index is None:
            tmux_app_index = parent_names.index('tmux: server') if 'tmux: server' in parent_names else None
        log('detect tmux {} screen {}'.format(tmux_app_index, screen_app_index))

        if tmux_app_index is not None and screen_app_index is not None:
            if screen_app_index < tmux_app_index:
                multiplexer_app = 'screen'
            elif screen_app_index > tmux_app_index:
                multiplexer_app = 'tmux'
        elif screen_app_index is not None:
            multiplexer_app = 'screen'
        elif tmux_app_index is not None:
            multiplexer_app ='tmux'
        elif 'TMUX' in os.environ:
            multiplexer_app = 'tmux'
        elif 'STY' in os.environ:
            multiplexer_app = 'screen'
        else:
             multiplexer_app = 'unknown'

        log('multiplexer_app {}'.format(multiplexer_app))

        multiplexer_window_name = None
        multiplexer_pane_name = None
        multiplexer_way = None
        if multiplexer_app == 'screen':
            try:
                sty = os.environ.get('STY')
                log('multiplexer_app: {}, STY: {}'.format(multiplexer_app, sty))

                screen_output = process_exec(['screen', '-q', '-Q', 'title'])

                multiplexer_window_name = screen_output.decode().rstrip('\n\r')
                if multiplexer_window_name == '':
                    multiplexer_window_name = None
                log('multiplexer_app: {}, title: {}'.format(multiplexer_app, multiplexer_window_name))
            except Exception as e:
                log('screen multiplexer_window_name - exception:', e)
        if multiplexer_app  == 'tmux':
            try:
                tmux_output = process_exec(['tmux', 'display-message', '-p', '"#{session_name} -> #{window_index} #{window_name} -> #{pane_index} #{pane_title}"'])
                multiplexer_way = tmux_output.decode()[0:-1].strip('"').strip()
                log('multiplexer_app: {}, way: {}'.format(multiplexer_app, multiplexer_way))
            except Exception as e:
                log('tmux multiplexer_way - exception:', e)

            try:
                tmux_output = process_exec(['tmux', 'list-window', '-F', '"#{window_name} #{window_active}"'])
                tmux_windows = tmux_output.decode()[0:-1].splitlines()
                [multiplexer_window_name] = [tmux_window.strip('"')[0:-2] for tmux_window in tmux_windows if tmux_window.strip('"')[-1] == '1']
                if multiplexer_window_name == '':
                    multiplexer_window_name = None
                log('multiplexer_app: {}, window: {}'.format(multiplexer_app, multiplexer_window_name))
            except Exception as e:
                log('tmux multiplexer_window_name - exception:', e)

            try:
                tmux_output = process_exec(['tmux', 'list-pane', '-F', '"#{pane_title} #{pane_active}"'])
                tmux_panes = tmux_output.decode()[0:-1].splitlines()
                [multiplexer_pane_name] = [tmux_pane.strip('"')[0:-2] for tmux_pane in tmux_panes if tmux_pane.strip('"')[-1] == '1']
                log('multiplexer_app: {}, pane: {}'.format(multiplexer_app, multiplexer_pane_name))
            except Exception as e:
                log('tmux multiplexer_pane_name - exception:', e)

        console_names = []
        if gui_app_tab_name is not None:
            console_names.append(gui_app_tab_name)
        if multiplexer_way is not None:
            console_names.append(multiplexer_way)
        else:
            if multiplexer_window_name is not None:
                console_names.append(multiplexer_window_name)
            if multiplexer_pane_name is not None:
                console_names.append(multiplexer_pane_name)

        if len(console_names) > 1:
            names = ' -> '.join(console_names)
        elif len(console_names) == 1:
            names = console_names[0]

        if len(console_names) > 0:
            notify__title += ' [{}]'.format(names)

        shell = parent_process_info_exe
        shell_cmdline = parent_process_info_cmdline

        known_shells = ['bash', 'zsh', 'fish', 'csh', 'sh']
        detected_shell = [known_shell for known_shell in known_shells if shell.endswith(known_shell)]
        detected_win_shell = [known_shell for known_shell in known_shells if shell.endswith(known_shell + '.exe')]
        detected_xonsh = 1 if 'xonsh' in parent_process_info_cmdline[-1] else 0
        if detected_xonsh == 1:
            if sys.version_info >= (3, 8):
                shell = shlex.join(shell_cmdline)
            else:
                shell = ' '.join([shlex.quote(arg) for arg in shell_cmdline])
        if detected_shell or detected_win_shell or shell.endswith('cmd.exe') or detected_xonsh:

            if shell.endswith('cmd.exe'):
                c = '/c'
            else:
                c = '-c'
            run_cmd = shell + ' {c} {cmdline}'.format(c=c, cmdline=repr(cmdline))

            if shell.endswith('cmd.exe'):
                cmdline_args = run_cmd
                system_shell = True
            else:
                if sys.platform == 'win32':
                    cmdline_args = run_cmd
                else:
                    cmdline_args = shlex.split(run_cmd)
                system_shell = False
    except Exception as e:
        log('backend={} cmd run'.format(backend), e)

    log('detected_shell={} detected_shell_cmdline={} use_system_shell={} cmdline={}'.format(shell, shell_cmdline, system_shell, run_cmd))

    ############################################################################
    # --detach
    ############################################################################
    if args.detach:
        try:
            if sys.platform == 'win32':
                not_detached_sys_argv = [arg for arg in sys.argv if arg != '--detach']
                not_detached_sys_argv.insert(0, sys.executable)
                log('sys.argv', sys.argv)
                log('new sys.argv', not_detached_sys_argv)

                if sys.version_info >= (3, 7):
                    DETACHED_PROCESS = subprocess.DETACHED_PROCESS
                else:
                    DETACHED_PROCESS = 0x08

                subprocess.Popen(not_detached_sys_argv, creationflags=DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP, stdout=subprocess.PIPE, close_fds=True)
                exit_code = 0
                nf_cleanup()
                return exit_code
            else:
                pid = os.fork()
                if pid > 0:
                    log('parent pid={} exit'.format(os.getpid()))

                    nf_cleanup()
                    return 'detached'
                if pid == 0:
                    log('child pid={} start'.format(os.getpid()))
        except Exception as e:
            log('detach not supported for {} {}'.format(sys.platform, sys.version_info), e)

    ############################################################################
    # --wait-for-pids
    ############################################################################
    if args.wait_for_pid is not None:
        pids = list(set(args.wait_for_pid)) # unique items only
        log('wait for pid: {}'.format(pids))
        psutil_fail = False
        try:
            import psutil
            processes = [psutil.Process(pid) for pid in pids if  psutil.pid_exists(pid)]
            psutil.wait_procs(processes)
        except Exception as e:
            log('wait for pid psutil exception', e)
            psutil_fail = True
        if psutil_fail == True:
            try:
                start_time = None
                while True:
                    for pid in pids[:]:
                        try:
                            with open('/proc/{pid}/stat'.format(pid=pid)) as f:
                                stat = f.read().split()
                                if start_time is None:
                                    start_time = stat[21]
                                elif start_time != stat[21]:
                                    log('pid {} finished work'.format(pid))
                                    pids.remove(pid)
                                elif stat[2] == 'Z':
                                    log('pid {} is zombie, treat as finished'.format(pid))
                                    pids.remove(pid)
                        except Exception as e:
                            log('exception while waiting for pid {}:'.format(pid), e)
                            pids.remove(pid)
                    if len(pids) == 0:
                        break
                    time.sleep(1)
            except Exception as e:
                log('exception while waiting for pids', e)
    ############################################################################
    # core
    ############################################################################
    if args.cmd is not None:
        log('before run cmd', cmdline_args)
        try:
            import subprocess
            p = subprocess.Popen(cmdline_args, shell=system_shell)
            p.communicate()
            exit_code = p.returncode
            #if sys.version_info >= (3, 5):
            #    exit_code = subprocess.run(cmdline_args, shell=system_shell).returncode
            #else:
            #    import subprocess
            #    exit_code = subprocess.call(cmdline_args, shell=system_shell)
        except Exception as e:
            log('core run cmdline failed for: <{}>'.format(cmdline_args), e)
        log('after run cmd', cmdline_args)
            #exit_code = os.system(run_cmd)
        # exit_code = os.system(cmdline) # works fine
    ############################################################################
    # end of core
    ############################################################################

    log('cmdline={} system_shell={} exit code={}'.format(cmdline_args, system_shell, exit_code))

    time_end = datetime.datetime.now()

    time_elapsed = datetime.datetime(1970, 1, 1, 0, 0, 0) +  (time_end - time_start)

    notify__body = '"' + os.getcwd() + "$ " + cmd + '"'

    notify__app_name = cmd
    notify__timeout = 0

    if args.custom_notification_exit_code is not None:
        exit_code = args.custom_notification_exit_code

    if exit_code != 0:
        notify__app_icon = "process-stop"
        notify__body += ' was exit with exit code = ' + str(exit_code)
    else:
        notify__app_icon = "services"
        notify__body += ' finished work.'

    notify__body += "\n\nStart time:   " + time_start.strftime("%H:%M.%S") + "\n" + "End time:     " + time_end.strftime("%H:%M.%S") + "\n" + "Elapsed time: " + time_elapsed.strftime("%H:%M.%S")
    notify__body += "\nTimestamp: " + str(time.time())  # Observation: in KDE the same notification body results in replace notification(s) so you can run 5 nf and see only 2 notifications

    if args.custom_notification_title is not None:
        notify__title = args.custom_notification_title

    if args.custom_notification_text is not None:
        notify__body = args.custom_notification_text

    log('no_notifty is {}, backend is {}'.format(args.no_notify, backend))
    if not args.no_notify:
        try:
            if backend == 'wsl':

                nf_exit_code = 0
                cmdline_args = None
                try:
                    s = None
                    try:
                        import inspect
                        s = inspect.getsource(inspect.getmodule(nf))

                        if sys.version_info.major == 2:
                            s = s[s.find('##'):]

                        s = s.replace('nf_stored_code = None', 'nf_stored_code = {}'.format(repr(s)), 1)
                    except Exception as e:
                        s = nf_stored_code
                        s = s.replace('nf_stored_code = None', 'nf_stored_code = {}'.format(repr(s)), 1) # recover stored code variable
                        log('inspect exception:', e)

                    cmdline_args = [python_exe, '-', '--custom_notification_title={}'.format(notify__title), '--custom_notification_text={}'.format(notify__body),  '--custom_notification_exit_code={}'.format(exit_code)]

                    log('run external python:', cmdline_args)
                    import subprocess
                    p = subprocess.Popen(cmdline_args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=environ)
                    nf_script = s.encode()
                    output, stderr_output  = p.communicate(nf_script)
                    o = output.decode()
                    log('stdout external python', output)
                    log('stderr external python', stderr_output)
                    if o != '':
                        print_stdout(o)
                    # output is redirected on stdout
                    if nf_exit_code != 0:
                        log('run external python exit with error: <{}> exit code {}'.format(cmdline_args, nf_exit_code))
                except Exception as e:
                    log('run external python failed for: <{}> exit code {}'.format(cmdline_args, nf_exit_code), e)
                    print_stdout('ERROR: Cannot run external python, last3 win step')
                    backend = 'stdout'

                log('wsl external python exit code ', nf_exit_code)
            elif backend == 'dbus':
                notify__replaces_id = dbus.UInt32(time.time() * 1000000 % 2 ** 32)
                notify__actions = dbus.Array(signature='s')
                notify__hints = dbus.Dictionary(signature='sv')

                try:
                    backend_internal['dbus_notification'].Notify(notify__app_name, notify__replaces_id, notify__app_icon, notify__title, notify__body, notify__actions, notify__hints, notify__timeout)
                except Exception as e:
                    log('dbus notify #1 fails', e)
                    notify_interface = dbus.Interface(dbus_notification, dbus_interface='org.freedesktop.Notifications')
                    notify_interface.Notify(notify__app_name, notify__replaces_id, notify__app_icon, notify__title, notify__body, notify__actions, notify__hints, notify__timeout)
            elif backend == 'gdbus':
                process_exec([gdbus_app, 'call', '--session', '--dest', 'org.freedesktop.Notifications', '--object-path', '/org/freedesktop/Notifications', '--method', 'org.freedesktop.Notifications.Notify',
                                  notify__app_name,
                                  str(int(time.time() * 1000000 % 2 ** 32)),
                                  notify__app_icon,
                                  notify__title,
                                  notify__body,
                                  "[]",
                                  "{}",
                                  str(notify__timeout)])
            elif backend == 'notify-send':
                process_exec([notify_send_app, notify__title, notify__body, '--expire-time', str(notify__timeout), '--icon', notify__app_icon, '--app-name', notify__app_name])
            elif backend == 'termux-notification':
                process_exec([termux_notification_app, '--title', notify__title, '--content', notify__body, '--sound', '--vibrate', '500,100,200', '--action', '"am start com.termux/.app.TermuxActivity"'])
            elif backend == 'win10toast-persist':
                import win10toast
                toaster = win10toast.ToastNotifier()
                toaster.show_toast(notify__title, notify__body, duration=None)
            elif backend == 'win10toast':
                import win10toast
                toaster = win10toast.ToastNotifier()
                toaster.show_toast(notify__title, notify__body)
            elif backend == 'plyer':
                plyer.notification.notify(title=notify__title, message=notify__body, app_name=notify__app_name, app_icon=notify__app_icon,timeout=notify__timeout)
            elif backend == 'plyer_toast':
                plyer.notification.notify(title=notify__title, message=notify__body, app_name=notify__app_name, app_icon=notify__app_icon,timeout=notify__timeout, toast=True)
            elif backend == 'ssh':
                if ssh_process:
                    with open(__file__, 'r') as f:
                        line = f.readline()
                        while line != '##\n':
                            line = f.readline()
                        myself = f.read()
# TODO: unbash ssh cmd: remove unset SSH_CLIENT)
# TODO: detect DISPLAY=:0 
# ps -fC X
# UID        PID  PPID  C STIME TTY          TIME CMD
# xxxx yyy   zzz  eee fff ttyaaa         aa:aa:aa X :0
# so CMD is X :0 <-= ":0"
# TODO: detect DBUS_SESSION_BUS_ADDRESS if possible
                    new_args = []
                    for arg,value in vars(args).items():
                        arg = arg.replace('_', '-')
                        if value is not None and value is not False and arg != 'cmd' and arg != 'args':
                            if value == True:
                                new_args.append('--{}'.format(arg))
                            else:
                                new_args.append('--{}={}'.format(arg,value))
                    log('new_args', new_args)
                    cmd = "python - --custom_notification_title=\"{}\" --custom_notification_text=\"{}\" --custom_notification_exit_code={} --env-unset=SSH_CLIENT --env-set-default=DISPLAY=:0 {rest}".format(notify__title.replace("\"", "\\\""), notify__body.replace("\"", "\\\""), exit_code, rest=' '.join(new_args)).encode() + b"\n" + myself.encode() + b"\n"
                    if sys.version_info >= (3, 3):
                        output, stderr_output = ssh_process.communicate(cmd, timeout=5)
                    else:
                        output, stderr_output = ssh_process.communicate(cmd)
                    log('stdout', output.decode())
                    log('stderr', stderr_output.decode())
            elif backend == 'paramiko':
                if ssh_client:
                    with open(__file__, 'r') as f:
                        line = f.readline()
                        while line != '##\n':
                            line = f.readline()
                        myself = f.read()
                    cmd = "python - --custom_notification_title=\"{}\" --custom_notification_text=\"{}\" --custom_notification_exit_code={} --env-unset=SSH_CLIENT --env-set-default=DISPLAY=:0".format(notify__title.replace("\"", "\\\""), notify__body.replace("\"", "\\\""), exit_code).encode() + b"\n" + myself.encode() + b"\n"
                    stdin, output, stderr_output = ssh_client.exec_command(cmd)
                    log('stdout', output.read().decode())
                    log('stderr', stderr_output.read().decode())
                    ssh_client.close()
        except Exception as e:
            log('engine error, backend={}:'.format(backend), e)
            exc_info = sys.exc_info()
            log('traceback line: {line} ; '.format(line=exc_info[-1].tb_lineno), e)
            import traceback
            traceback.print_exception(*exc_info)

            backend = 'stdout'
    else:
        if backend != 'stdout':
            backend = 'stdout'

    if backend == 'stdout' or args.print:
        columns = 10
        try:
            import shutil
            sizes = shutil.get_terminal_size()
            columns = sizes.columns
        except Exception as e:
            log('Cannot get terminal size', e)

        print_stdout('-' * columns)
        print_stdout(notify__title)
        print_stdout(notify__body)
        print_stdout('-' * columns)
        if not args.no_notify:
            print_stdout('\a')

    if args.save:
        try:
            with open(".nf", 'a') as f:
                print_stdout(cmdline, file=f)
                print_stdout('Exit code: {}'.format(exit_code), file=f)
                print_stdout('Start {}'.format(time_start.strftime("%Y-%m-%d %H:%M.%S.%f")), file=f)
                print_stdout('Stop  {}'.format(time_end.strftime("%Y-%m-%d %H:%M.%S.%f")), file=f)
                print_stdout('Diff             {}'.format(time_elapsed.strftime('%H:%M.%S')), file=f)
                print_stdout('----------', file=f)
        except Exception as e:
            print_stdout('Cannot save .nf file')
            log('Cannot save .nf file', e)

    nf_cleanup()
    return exit_code

def main():
    """
    Execute nf(argv) where argv is sys.argv then exit with returned value. This function exit python interpreter.
    """
    import sys
    exit_code = nf()
    if exit_code == 'detached':
        os._exit(0)
    else:
        sys.exit(exit_code)

if __name__ == "__main__":
   main()
