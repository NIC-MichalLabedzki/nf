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
##

# for python2
from __future__ import print_function as _print_function

"""
./nf.py [optional options] command [arg...]
"""

def nf(argv=None):
    VERSION = '1.4.0'
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

    parser = argparse.ArgumentParser(description='Simple command line tool to make notification after target program finished work', epilog=EXAMPLES, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-l', '--label', type=str, help='Add humn readable text to custom job identification')
    parser.add_argument('-p', '--print', action="store_true", help='Print notification text in stdout too')
    parser.add_argument('-n', '--no-notify', action="store_true", help='Do not do annoying notifications')
    parser.add_argument('-s', '--save', action="store_true", help='Save/append command and stat to .nf file')
    parser.add_argument('-w', '--wait-for-pid', type=int, action='append',help='Wait for PID aka wait for already run process finish work. This option can be used multiple times.')
    parser.add_argument('--detach', action="store_true", help='Run command or wait for pid in detached process')

    parser.add_argument('-b', '--backend', type=str, choices=['paramiko', 'ssh', 'dbus', 'gdbus', 'notify-send', 'termux-notification', 'win10toast-persist', 'win10toast', 'plyer', 'plyer_toast', 'stdout'], help='Notification backend')
    parser.add_argument('-v', '--version', action="version", help='Print version', version=VERSION)
    parser.add_argument('-d', '--debug', action="store_true", help='More print debugging on stdout')
    parser.add_argument('--debugfile', type=str, help='More print debugging save into file')
    parser.add_argument('--custom_notification_text', type=str, help='Custom notification text')
    parser.add_argument('--custom_notification_title', type=str, help='Custom notification title')
    parser.add_argument('--custom_notification_exit_code', type=int, help='Custom notification exit code')
    parser.add_argument('cmd')
    parser.add_argument('args', nargs=argparse.REMAINDER)
    args = parser.parse_args(argv)

    logfile = {'handle': None}
    def log(*arg):
        current_time = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S.%f")
        if args.debug is True:
            argss = []
            for a in arg:
                argss.append(str(a))
            try:
                print('DEBUG {}: {}'.format(current_time, ' '.join(argss)))
            except:
                pass
        if args.debugfile is not None:
            argss = []
            for a in arg:
                argss.append(str(a))
            if logfile['handle'] is None:
                logfile['handle'] = open(args.debugfile, 'a+b', 0)
            logfile['handle'].write('DEBUG {}: {}\n'.format(current_time, ' '.join(argss)).encode())

    def print_stdout(*arg, **karg):
        try:
            print(*arg, **karg)
        except Exception as e:
            log('cannot print on stdout: ', *arg)

    log('nf version={}'.format(VERSION))
    log('python {}'.format(sys.version_info))
    log('platform {}'.format(sys.platform))
    is_wsl = None
    if sys.platform.startswith('linux'):
        with open('/proc/version') as f:
            v = f.read()
            is_wsl = True if 'Microsoft' in v else False
    log('is_wsl {}'.format(is_wsl))
    log('argv {}'.format(sys.argv))

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
                if 'SSH_CLIENT' in os.environ:
                    ssh_connection = os.environ['SSH_CLIENT'].split(' ')
                    ssh_ip = ssh_connection[0]
                    ssh_port = ssh_connection[2]

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
                if 'SSH_CLIENT' in os.environ:
                    ssh_connection = os.environ['SSH_CLIENT'].split(' ')
                    ssh_ip = ssh_connection[0]
                    ssh_port = ssh_connection[2]

                    import subprocess

                    try:
                        ssh_process = subprocess.Popen(["ssh", ssh_ip , '-p', ssh_port, '-o', 'StrictHostKeyChecking=no', '-o', 'ConnectTimeout=2', '-o', 'PreferredAuthentications=publickey', '-o', 'PubkeyAuthentication=yes'], stderr=subprocess.PIPE, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
                        time.sleep(1)
                        if ssh_process.poll() != None:
                            raise Exception('Public key not working')
                    except Exception as e:
                        log('backend={}'.format('ssh'), e)
                        ssh_process = subprocess.Popen(["ssh", ssh_ip , '-p', ssh_port, '-o', 'ConnectTimeout=2', '-o', 'PreferredAuthentications=password', '-o', 'PubkeyAuthentication=no'], stderr=subprocess.PIPE, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
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

        if ((sys.platform == 'win32' or is_wsl) and backend in ['stdout', 'win10toast-persist'] and args.backend == None) or args.backend == 'win10toast-persist':
            try:
                if is_wsl:
                    pass # TODO
                    # python -m pip install --platform win32 --only-binary=:all: --target win32_modules    win10toast-persist
                    # PYTHONPATH +=:win32_modules

                import win10toast
                backend = 'win10toast-persist'
            except Exception as e:
                log('backend={}'.format('win10toast-persist'), e)
                backend = 'stdout'

        if ((sys.platform == 'win32' or is_wsl) and backend in ['stdout', 'win10toast'] and args.backend == None) or args.backend == 'win10toast':
            try:
                if is_wsl:
                    pass # TODO

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
                import shutil

                gdbus_app = shutil.which('gdbus')
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
                import shutil

                notify_send_app = shutil.which('notify-send')
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
                import shutil

                termux_notification_app = shutil.which('termux-notification')
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
    notify__title = args.cmd

    cmdline = args.cmd + (' ' if len(args.args) > 0 else '') + ' '.join(args.args)
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
            multiplexer_client_pid = int(subprocess.check_output(tmux_cmdline).decode().strip('"\n'))
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
                    tmux_cmdline = ['tmux', 'display-message', '-p', '"#{client_pid}"']
                    multiplexer_client_pid = int(subprocess.check_output(tmux_cmdline).decode().strip('"\n'))
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



        def call_dbus(service_name, path, method, *arg):
            import shutil
            import subprocess
            app = shutil.which('qdbus')
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
                app = shutil.which('gdbus')
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
                    app = shutil.which('dbus-send')
                    if app is not None:
                        log('which dbus-send: {}'.format(app))
                        tool_cmdline = [app, '--session', '--print-reply=literal', '--dest={}'.format(service_name), path, '{}.{}'.format(service_name, method)]
                        tool_cmdline.extend(xarg)
                    else:
                        log('cannot find dbus backend')

            log('dbus cmdline', tool_cmdline)

            output = subprocess.check_output(tool_cmdline).decode().strip()
            log('dbus backend output', output)

            if app == shutil.which('gdbus'):
                output = output.strip('(),')
            if app == shutil.which('dbus-send'):
                if 'int32' in output:
                    output = output.split(' ')[1]
            log('dbus final output', output)

            return output


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
            sty = os.environ['STY']
            log('multiplexer_app {} STY {}'.format(multiplexer_app, sty))
            screen_cmdline = ['screen', '-q', '-Q', 'title']
            import subprocess
            screen_output = subprocess.check_output(screen_cmdline)
            multiplexer_window_name = screen_output.decode().rstrip('\n\r')
            if multiplexer_window_name == '':
                multiplexer_window_name = None
            log('multiplexer_app {} title {}'.format(multiplexer_app, multiplexer_window_name))
        if multiplexer_app == 'tmux':
            tmux_cmdline = ['tmux', 'list-window', '-F', '"#{window_name} #{window_active}"']
            tmux_output = subprocess.check_output(tmux_cmdline)
            tmux_windows = tmux_output.decode()[0:-1].splitlines()
            [multiplexer_window_name] = [tmux_window.strip('"')[0:-2] for tmux_window in tmux_windows if tmux_window.strip('"')[-1] == '1']
            if multiplexer_window_name == '':
                multiplexer_window_name = None
            log('multiplexer_app {} window {}'.format(multiplexer_app, multiplexer_window_name))

            tmux_cmdline = ['tmux', 'list-pane', '-F', '"#{pane_title} #{pane_active}"']
            tmux_output = subprocess.check_output(tmux_cmdline)
            tmux_panes = tmux_output.decode()[0:-1].splitlines()
            [multiplexer_pane_name] = [tmux_pane.strip('"')[0:-2] for tmux_pane in tmux_panes if tmux_pane.strip('"')[-1] == '1']
            log('multiplexer_app {} pane {}'.format(multiplexer_app, multiplexer_pane_name))

            tmux_cmdline = ['tmux', 'display-message', '-p', '"#{session_name} -> #{window_index} #{window_name} -> #{pane_index} #{pane_title}"']
            multiplexer_way = subprocess.check_output(tmux_cmdline).decode()[0:-1].strip('"').strip()
            log('multiplexer_app {} way {}'.format(multiplexer_app, multiplexer_way))

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
            run_cmd = shell + ' {c} "{cmdline}"'.format(c=c, cmdline=cmdline.replace('"', '\\"'))

            if shell.endswith('cmd.exe'):
                cmdline_args = run_cmd
                system_shell = True
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

                import subprocess
                subprocess.Popen(not_detached_sys_argv, creationflags=DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP, stdout=subprocess.PIPE, close_fds=True)
                exit_code = 0
                return exit_code
            else:
                pid = os.fork()
                if pid > 0:
                    log('parent pid={} exit'.format(os.getpid()))

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
    try:
        if sys.version_info >= (3, 5):
            exit_code = subprocess.run(cmdline_args, shell=system_shell).returncode
        else:
            import subprocess
            exit_code = subprocess.call(cmdline_args, shell=system_shell)
    except Exception as e:
        log('core run cmdline failed for: <{}>'.format(cmdline_args), e)
        #exit_code = os.system(run_cmd)
    # exit_code = os.system(cmdline) # works fine
    ############################################################################
    # end of core
    ############################################################################

    log('cmdline={} system_shell={} exit code={}'.format(cmdline_args, system_shell, exit_code))

    time_end = datetime.datetime.now()

    time_elapsed = datetime.datetime(1970, 1, 1, 0, 0, 0) +  (time_end - time_start)

    notify__body = '"' + os.getcwd() + "$ " + args.cmd + '"'

    notify__app_name = args.cmd
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

    if not args.no_notify:
        try:
            if backend == 'dbus':
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
                notify_cmdline = [gdbus_app, 'call', '--session', '--dest', 'org.freedesktop.Notifications', '--object-path', '/org/freedesktop/Notifications', '--method', 'org.freedesktop.Notifications.Notify',
                                  notify__app_name,
                                  str(int(time.time() * 1000000 % 2 ** 32)),
                                  notify__app_icon,
                                  notify__title,
                                  notify__body,
                                  "[]",
                                  "{}",
                                  str(notify__timeout)]
                if sys.version_info >= (3, 5):
                    import subprocess
                    notify_exit_code = subprocess.run(notify_cmdline).returncode
                else:
                    import subprocess
                    notify_exit_code = subprocess.call(notify_cmdline)
            elif backend == 'notify-send':
                notify_cmdline = [notify_send_app, notify__title, notify__body, '--expire-time', str(notify__timeout), '--icon', notify__app_icon, '--app-name', notify__app_name]
                if sys.version_info >= (3, 5):
                    import subprocess
                    notify_exit_code = subprocess.run(notify_cmdline).returncode
                else:
                    import subprocess
                    notify_exit_code = subprocess.call(notify_cmdline)
            elif backend == 'termux-notification':
                notify_cmdline = [termux_notification_app, '--title', notify__title, '--content', notify__body, '--sound', '--vibrate', '500,100,200', '--action', '"am start com.termux/.app.TermuxActivity"']
                if sys.version_info >= (3, 5):
                    import subprocess
                    notify_exit_code = subprocess.run(notify_cmdline).returncode
                else:
                    import subprocess
                    notify_exit_code = subprocess.call(notify_cmdline)
            elif backend == 'win10toast-persist':
                toaster = win10toast.ToastNotifier()
                toaster.show_toast(notify__title, notify__body, duration=None)
            elif backend == 'win10toast':
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
                    cmd = "unset SSH_CLIENT; python - --custom_notification_title=\"{}\" --custom_notification_text=\"{}\" --custom_notification_exit_code={} echo << 'EOF'".format(notify__title.replace("\"", "\\\""), notify__body.replace("\"", "\\\""), exit_code).encode() + b"\n" + myself.encode() + b"\nEOF\n"
                    if sys.version_info >= (3, 3):
                        output, stderr_output = ssh_process.communicate(cmd, timeout=5)
                    else:
                        output, stderr_output = ssh_process.communicate(cmd)
                    log('stdout', output)
                    log('stderr', stderr_output)
            elif backend == 'paramiko':
                if ssh_client:
                    with open(__file__, 'r') as f:
                        line = f.readline()
                        while line != '##\n':
                            line = f.readline()
                        myself = f.read()
                    cmd = "unset SSH_CLIENT; python - --custom_notification_title=\"{}\" --custom_notification_text=\"{}\" --custom_notification_exit_code={} echo << 'EOF'".format(notify__title.replace("\"", "\\\""), notify__body.replace("\"", "\\\""), exit_code).encode() + b"\n" + myself.encode() + b"\nEOF\n"
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
            log('', e)

        print_stdout('-' * columns)
        if notify__title != '':
            print_stdout(notify__title)
        print_stdout(notify__body)
        print_stdout('-' * columns)
        if not args.no_notify:
            print_stdout('\a')

    if args.save:
        with open(".nf", 'a') as f:
            print_stdout(cmdline, file=f)
            print_stdout('Exit code: {}'.format(exit_code), file=f)
            print_stdout('Start {}'.format(time_start.strftime("%Y-%m-%d %H:%M.%S.%f")), file=f)
            print_stdout('Stop  {}'.format(time_end.strftime("%Y-%m-%d %H:%M.%S.%f")), file=f)
            print_stdout('Diff             {}'.format(time_elapsed.strftime('%H:%M.%S')), file=f)
            print_stdout('----------', file=f)
    if logfile['handle'] is not None:
        logfile['handle'].write('\n'.encode())
        logfile['handle'].close()
    return exit_code

def main():
    import sys
    exit_code = nf()
    if exit_code == 'detached':
        os._exit(0)
    else:
        sys.exit(exit_code)

if __name__ == "__main__":
   main()
