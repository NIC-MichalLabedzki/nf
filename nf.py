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

    examples = '''
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

    parser = argparse.ArgumentParser(description='Simple command line tool to make notification after target program finished work', epilog=examples, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-l', '--label', type=str, help='Add humn readable text to custom job identification')
    parser.add_argument('-p', '--print', action="store_true", help='Print notification text in stdout too')
    parser.add_argument('-n', '--no-notify', action="store_true", help='Do not do annoying notifications')
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
    elif dbus_session is None:
        print("nf: WARNING: Could not get dbus session, notification will not work", file=sys.stderr)
    else:
        dbus_notification = dbus_session.get_object('org.freedesktop.Notifications', '/org/freedesktop/Notifications')

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

    if dbus_notification:
        notify__app_name = args.cmd
        notify__replaces_id = dbus.UInt32()
        notify__app_icon = "services"
        notify__timeout = 0
        notify__actions = dbus.Array(signature='s')
        notify__hints = dbus.Dictionary(signature='sv')

    notify__body = '"' + os.getcwd() + "$ " + args.cmd + '"'

    if exit_code != 0:
        notify__app_icon = "process-stop"
        notify__body += ' was exit with exit code = ' + str(exit_code)
    else:
        notify__body += ' finished work.'

    notify__body += "\n\nStart time:   " + time_start.strftime("%H:%M.%S") + "\n" + "End time:     " + time_end.strftime("%H:%M.%S") + "\n" + "Elapsed time: " + time_elapsed.strftime("%H:%M.%S")
    if dbus_notification is None or args.print:
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
    if dbus_notification:
        dbus_notification.Notify(notify__app_name, notify__replaces_id, notify__app_icon, notify__summary, notify__body, notify__actions, notify__hints, notify__timeout)
    sys.exit(exit_code)

if __name__ == "__main__":
   main()
