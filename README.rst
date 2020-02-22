==============
nf
==============

.. |NF_VERSION| replace:: v1.3.2

.. image:: https://img.shields.io/travis/NIC-MichalLabedzki/nf/v1.3.2?label=latest%20stable%20build
   :target: https://travis-ci.org/NIC-MichalLabedzki/nf

.. image:: https://img.shields.io/travis/NIC-MichalLabedzki/nf/master?label=latest%20development%20build
   :target: https://travis-ci.org/NIC-MichalLabedzki/nf

.. image:: https://badge.fury.io/py/nf.svg
   :target: https://badge.fury.io/py/nf

.. image:: https://img.shields.io/pypi/v/nf

.. image:: https://img.shields.io/pypi/pyversions/nf.svg
   :target: https://pypi.python.org/pypi/nf

.. image:: https://img.shields.io/pypi/implementation/nf

.. image:: https://img.shields.io/github/repo-size/NIC-MichalLabedzki/nf

.. image:: https://img.shields.io/github/languages/code-size/NIC-MichalLabedzki/nf

.. image:: https://img.shields.io/pypi/l/nf

.. image:: https://img.shields.io/coveralls/github/NIC-MichalLabedzki/nf

.. image:: https://img.shields.io/github/commits-since/NIC-MichalLabedzki/nf/v1.3.2

IN SHORT
--------

``nf`` is a tool to make notification for user that its command finish work. For example "make" program that takes long time to finish.

SPDX-License-Identifier: 0BSD

Project name: nf
License: 0BSD / Free Public License 1.0.0
More information about license: https://opensource.org/licenses/0BSD

CHANGELOG
---------

From 1.2.0:
    1. Add support for `yakuake`, `konsole`, 'screen' and 'tmux' terminal tab name (to fast find notification source)
    2. Add new backend: gdbus

SCREENSHOTS
-----------

1. Screenshot from KDE:

.. image::  https://raw.githubusercontent.com/NIC-MichalLabedzki/nf/v1.3.2/images/screenshot_1_kde.png
   :target: https://raw.githubusercontent.com/NIC-MichalLabedzki/nf/v1.3.2/images/screenshot_1_kde.png
   :alt: Screenshot from KDE
   :width: 200

2. Screenshot from KDE:

.. image::  https://raw.githubusercontent.com/NIC-MichalLabedzki/nf/v1.3.2/images/screenshot_2_kde.png
   :target: https://raw.githubusercontent.com/NIC-MichalLabedzki/nf/v1.3.2/images/screenshot_2_kde.png
   :alt: Screenshot from KDE
   :width: 200

3. Screenshot from KDE:

.. image::  https://raw.githubusercontent.com/NIC-MichalLabedzki/nf/v1.3.2/images/screenshot_3_kde.png
   :target: https://raw.githubusercontent.com/NIC-MichalLabedzki/nf/v1.3.2/images/screenshot_3_kde.png
   :alt: Screenshot from KDE
   :width: 200

4. Screenshot from Android:

.. image::  https://raw.githubusercontent.com/NIC-MichalLabedzki/nf/v1.3.2/images/screenshot_4_android.png
   :target: https://raw.githubusercontent.com/NIC-MichalLabedzki/nf/v1.3.2/images/screenshot_4_android.png
   :alt: Screenshot from Android
   :width: 200

NON-INSTALL
-----------

.. code-block:: bash

    git clone git@github.com:NIC-MichalLabedzki/nf.git

You can run it from sources without any dependancies* (python and some modules delivered with it)

.. code-block:: bash

    python ./nf.py

See:

.. code-block:: bash

    python ./nf.py --help

See CLI section for more details.


INSTALLATION
------------

.. code-block:: bash

    pip install nf

or

.. code-block:: bash

    pip install -e git@github.com:NIC-MichalLabedzki/nf.git

or

.. code-block:: bash

    pip install -e https://github.com/NIC-MichalLabedzki/nf.git

or

.. code-block:: bash

    git clone git@github.com:NIC-MichalLabedzki/nf.git
    cd nf
    python setup.py # or pip install -e .


INTERFACE
---------

There are one kind of interfaces: ``CLI``.

If you think there is a need to have ``lib``/``module`` to please let me know why.
Maybe there is a reason.

CLI
~~~

CLI is Command Line Interface. So you have tool called: nf

.. code-block:: bash

    $ python nf.py --help
    usage: nf.py [-h] [-l LABEL] [-p] [-n] [-s]
                [-b {paramiko,ssh,dbus,gdbus,notify-send,termux-notification,win10toast,plyer,plyer_toast,stdout}]
                [-d] [-v] [--custom_notification_text CUSTOM_NOTIFICATION_TEXT]
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
    -b {paramiko,ssh,dbus,gdbus,notify-send,termux-notification,win10toast,plyer,plyer_toast,stdout}, --backend {paramiko,ssh,dbus,gdbus,notify-send,termux-notification,win10toast,plyer,plyer_toast,stdout}
                            Notification backend
    -d, --debug           More print debugging
    -v, --version         Print version
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

    "/home/nic/src/nf$ nf.py -p ls
    LICENSE  nf.py  pytest.ini  README  README.dev  requirements-dev.txt  setup.cfg  setup.py  tox.ini
    -----------------------------------------------------------
    "/home/nic/src/nf$ ls" finished work.

    Start time:   17:32.50
    End time:     17:32.50
    Elapsed time: 00:00.00
    -----------------------------------------------------------


LIMITATIONS
-----------
1. Work with Jython: it does not have dbus module, fallback to command line.
2. Observed in KDE: notification with the same body (text) can be dropped. To avoid that I add timestamp text to make nofitications unique.

FEATURES
--------
1. Support Android notification by termux-notifications (of course by `termux`)
2. Support dbus by python module or fallback to `notify-send` (part of `libnotify` 0.7.7 or 0.7.8)
3. Option to print notification on stdout.
4. Option to save full command line and stat to file into working directory.
5. Support whole python implementations/versions (at least not crash and print on stdout)
6. Case SSH: If you are over SSH send notification over backward-SSH connection to your native system (force password)
7. Supported notification backends: paramiko (ssh), ssh, dbus, notify-send, termux-notification (Android), win10toast (Windows),plyer, plyer_toast, stdout
8. yakuake/konsole terminal tab name in label
9. screen/tmux session/window/pane title/name in label
10. Python module aka library interface "import nf;nf.nf(['ls'])"

TMUX/SCREEN used be `nf` or how to test it
------------------------------------------
1. tmux session name:
.. code-block:: bash

    tmux rename-session sesja
    tmux list-sessions -F "#{session_name}"

2. tmux window name:
.. code-block:: bash

    tmux rename-window okno
    tmux list-window -F "#{window_name} #{window_active}"

3. tmux pane name:
.. code-block:: bash

    printf '\033]2;%s\033\\' 'this is a title'
    tmux list-pane -F "#{pane_title} #{pane_active}"

4. client pid to get parent (for example: yakuake)
.. code-block:: bash

    tmux display-message -p "#{client_pid}"

5. screen sessions:
.. code-block:: bash

    screen -list
    There are screens on:
    7842.pts-30.nic (Attached)
    6981.pts-25.nic (Attached)
    2 Sockets in /tmp/screens/S-nic.

6. screen window title
.. code-block:: bash

    screen -S 6981.pts-25.nic -Q title
    terefere

7. screen windows:
.. code-block:: bash

    screen -S 6981.pts-25.nic -Q windows
    0* terefere  1 bash  2 bash  3- bash

TODO
----
1. nf 1.4.0:
    a) nf -i PID # monitor specifiec already run process by PID/name/(interactive list???)
    b) run nf in (hidden???) background to add ability to (on Linux) CTRL+Z and run nf in background then back to main process ("fg")