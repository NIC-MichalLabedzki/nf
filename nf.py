#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: 0BSD

# Original author: Michał Łabędzki
# Source: https://github.com/NIC-MichalLabedzki/nf

# for python2
from __future__ import print_function as _print_function

"""
./nf.py [optional options] command [arg...]
"""

def main():
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
    parser.add_argument('cmd')
    parser.add_argument('args', nargs=argparse.REMAINDER)
    args = parser.parse_args()

    try:
        import signal

        def sigint_handler(signum, frame):
            signal.signal(signal.SIGINT, signal.default_int_handler)
            signal.signal(signal.SIGINT, sigint_handler)

        signal.signal(signal.SIGINT, sigint_handler)
    except:
        pass

    backend = 'stdout'
    dbus_session = None
    if not args.no_notify:
        try:
            import dbus
            dbus_session = dbus.SessionBus()
        except:
            dbus_session = None

        dbus_notification = None
        if args.no_notify:
            pass
        elif dbus_session is not None:
            backend = 'dbus'
            dbus_notification = dbus_session.get_object('org.freedesktop.Notifications', '/org/freedesktop/Notifications')
        else:
            try:
                import shutil

                notify_send_app = shutil.which('notify-send')
                if notify_send_app is not None:
                    backend = 'notify-send'
                else:
                    termux_notification_app = shutil.which('termux-notification')
                    if termux_notification_app is not None:
                        backend = 'termux-notification'
                    else:
                        try:
                            import win10toast
                            backend = 'win10toast'
                        except:
                            pass
            except:
                pass

            if backend == 'stdout':
                print("nf: WARNING: Could not get dbus session, notification will not work", file=sys.stderr)

    notify__summary = args.cmd

    cmdline = args.cmd + ' ' + ' '.join(args.args)
    if args.label is not None:
        notify__summary += ' (' + args.label + ')'

    time_start = datetime.datetime.now()

    if sys.version_info >= (3, 5):
        import subprocess
        exit_code = subprocess.run(cmdline, shell=True).returncode
    else:
        import subprocess
        exit_code = subprocess.call(cmdline, shell=True)
    # exit_code = os.system(cmdline) # works fine

    time_end = datetime.datetime.now()

    time_elapsed = datetime.datetime(1970, 1, 1, 0, 0, 0) +  (time_end - time_start)

    notify__body = '"' + os.getcwd() + "$ " + args.cmd + '"'

    notify__app_name = args.cmd
    notify__timeout = 0
    if exit_code != 0:
        notify__app_icon = "process-stop"
        notify__body += ' was exit with exit code = ' + str(exit_code)
    else:
        notify__app_icon = "services"
        notify__body += ' finished work.'

    notify__body += "\n\nStart time:   " + time_start.strftime("%H:%M.%S") + "\n" + "End time:     " + time_end.strftime("%H:%M.%S") + "\n" + "Elapsed time: " + time_elapsed.strftime("%H:%M.%S")
    notify__body += "\nTimestamp: " + str(time.time())  # Observation: in KDE the same notification body results in replace notification(s) so you can run 5 nf and see only 2 notifications

    if backend == 'dbus':
        notify__replaces_id = dbus.UInt32(time.time() * 1000000 % 2 ** 32)
        print('uuu', notify__replaces_id)
        notify__actions = dbus.Array(signature='s')
        notify__hints = dbus.Dictionary(signature='sv')

        dbus_notification.Notify(notify__app_name, notify__replaces_id, notify__app_icon, notify__summary, notify__body, notify__actions, notify__hints, notify__timeout)
    elif backend == 'notify-send':
        notify_cmdline = 'notify-send {summary} "`echo -en "{body}"`" --expire-time={timeout} --icon="{icon}" --app-name={app_name}'.format(
            summary=notify__summary, body=notify__body, app_name=notify__app_name, icon=notify__app_icon, timeout=notify__timeout)
        if sys.version_info >= (3, 5):
            import subprocess
            notify_exit_code = subprocess.run(notify_cmdline, shell=True).returncode
        else:
            import subprocess
            notify_exit_code = subprocess.call(notify_cmdline, shell=True)
    elif backend == 'termux-notification':
        notify_cmdline = "termux-notification --title '{title}' --content '{content}' --sound --vibrate 500,100,200 --action 'am start com.termux/.app.TermuxActivity'".format(title=notify__summary, content=notify__body)
        if sys.version_info >= (3, 5):
            import subprocess
            notify_exit_code = subprocess.run(notify_cmdline, shell=True).returncode
        else:
            import subprocess
            notify_exit_code = subprocess.call(notify_cmdline, shell=True)
    elif backend == 'win10toast':
        try:
            toaster = win10toast.ToastNotifier()
            toaster.show_toast(notify__summary, notify__body)
        except:
            pass

    if backend == 'stdout' or args.print:
        columns = 10
        try:
            import shutil
            sizes = shutil.get_terminal_size()
            columns = sizes.columns
        except:
            pass

        print('-' * columns)
        print(notify__body)
        print('-' * columns)
        if not args.no_notify:
            print('\a')

    if args.save:
        with open(".nf", 'a') as f:
            print(cmdline, file=f)
            print('Exit code: {}'.format(exit_code), file=f)
            print('Start {}'.format(time_start.strftime("%Y-%m-%d %H:%M.%S.%f")), file=f)
            print('Stop  {}'.format(time_end.strftime("%Y-%m-%d %H:%M.%S.%f")), file=f)
            print('Diff             {}'.format(time_elapsed.strftime('%H:%M.%S')), file=f)
            print('----------', file=f)

    sys.exit(exit_code)

if __name__ == "__main__":
   main()
