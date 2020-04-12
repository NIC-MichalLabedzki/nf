==============
nf
==============

.. |NF_VERSION| replace:: v1.4.0

.. image:: https://img.shields.io/travis/NIC-MichalLabedzki/nf/v1.4.0?label=latest%20stable%20build
   :target: https://travis-ci.org/NIC-MichalLabedzki/nf

.. image:: https://img.shields.io/coveralls/github/NIC-MichalLabedzki/nf/v1.4.0
   :target: https://coveralls.io/github/NIC-MichalLabedzki/nf

.. image:: https://img.shields.io/pypi/v/nf
   :target: https://pypi.org/project/nf/

.. image:: https://img.shields.io/pypi/implementation/nf

.. image:: https://img.shields.io/pypi/pyversions/nf.svg
   :target: https://pypi.python.org/pypi/nf

.. image:: https://img.shields.io/pypi/l/nf

.. image:: https://img.shields.io/pypi/dm/nf

------------------------------

.. image:: https://img.shields.io/travis/NIC-MichalLabedzki/nf/master?label=latest%20development%20build
   :target: https://travis-ci.org/NIC-MichalLabedzki/nf

.. image:: https://img.shields.io/coveralls/github/NIC-MichalLabedzki/nf/master?label=latest%20development%20coverage
   :target: https://coveralls.io/github/NIC-MichalLabedzki/nf

.. image:: https://img.shields.io/github/repo-size/NIC-MichalLabedzki/nf

.. image:: https://img.shields.io/github/languages/code-size/NIC-MichalLabedzki/nf

.. image:: https://img.shields.io/github/commits-since/NIC-MichalLabedzki/nf/v1.4.0

IN SHORT
--------

``nf`` is a tool to make notification for user that its command finish work. For example "make" program that takes long time to finish.

SPDX-License-Identifier: 0BSD

Project name: nf
License: 0BSD / Free Public License 1.0.0
More information about license: https://opensource.org/licenses/0BSD

CHANGELOG
---------

From 1.4.0:
    1. --try-version=list
    2. --try-version=tag,branch,commit hash, "master" to try latest development or "list" to display possible tags/versions.
    3. fix issue: ssh/paramiko in detached/re-attached tmux does not work

SCREENSHOTS
-----------

1. Screenshot from KDE:

.. image::  https://raw.githubusercontent.com/NIC-MichalLabedzki/nf/v1.4.0/images/screenshot_1_kde.png
   :target: https://raw.githubusercontent.com/NIC-MichalLabedzki/nf/v1.4.0/images/screenshot_1_kde.png
   :alt: Screenshot from KDE
   :width: 200

2. Screenshot from KDE:

.. image::  https://raw.githubusercontent.com/NIC-MichalLabedzki/nf/v1.4.0/images/screenshot_2_kde.png
   :target: https://raw.githubusercontent.com/NIC-MichalLabedzki/nf/v1.4.0/images/screenshot_2_kde.png
   :alt: Screenshot from KDE
   :width: 200

3. Screenshot from KDE:

.. image::  https://raw.githubusercontent.com/NIC-MichalLabedzki/nf/v1.4.0/images/screenshot_3_kde.png
   :target: https://raw.githubusercontent.com/NIC-MichalLabedzki/nf/v1.4.0/images/screenshot_3_kde.png
   :alt: Screenshot from KDE
   :width: 200

4. Screenshot from Android:

.. image::  https://raw.githubusercontent.com/NIC-MichalLabedzki/nf/v1.4.0/images/screenshot_4_android.png
   :target: https://raw.githubusercontent.com/NIC-MichalLabedzki/nf/v1.4.0/images/screenshot_4_android.png
   :alt: Screenshot from Android
   :width: 200

NON-INSTALL
-----------

It is one-file script so you can download and use it.
You can also run it from sources without any dependancies* (need only python and maybe some modules delivered with it [or not])

\* - Windows needs some modules to work, see setup.py for details. On 2020-03-08 they are: `python -m install psutil win10toast-persist`

Latest developement version:

.. code-block:: bash

    wget -c https://github.com/NIC-MichalLabedzki/nf/raw/master/nf.py


or

.. code-block:: bash

    curl https://github.com/NIC-MichalLabedzki/nf/raw/master/nf.py -f -L -o nf.py

or put link into your browser

https://github.com/NIC-MichalLabedzki/nf/raw/master/nf.py

or

.. code-block:: bash

    git clone git@github.com:NIC-MichalLabedzki/nf.git



.. code-block:: bash

    python ./nf.py

See:

.. code-block:: bash

    python ./nf.py --help

See CLI section for more details.

Previous stable versions:

.. code-block:: bash

    wget -c https://github.com/NIC-MichalLabedzki/nf/raw/v1.4.0/nf.py
    wget -c https://github.com/NIC-MichalLabedzki/nf/raw/v1.3.2/nf.py
    wget -c https://github.com/NIC-MichalLabedzki/nf/raw/v1.2.0/nf.py
    wget -c https://github.com/NIC-MichalLabedzki/nf/raw/v1.1.1/nf.py
    wget -c https://github.com/NIC-MichalLabedzki/nf/raw/v1.0.1/nf.py

INSTALLATION
------------



.. code-block:: bash

    python -m pip install nf

or

.. code-block:: bash

    python -m pip install nf --user

or

.. code-block:: bash

    python -m pip install nf --user --proxy=YOUR.PROXY.IP.v4:YOUR_PORT

or

.. code-block:: bash

    python -m pip install -e git+https://github.com/NIC-MichalLabedzki/nf.git#egg=master

or

.. code-block:: bash

    git clone https://github.com/NIC-MichalLabedzki/nf.git
    cd nf
    python setup.py # or python -m pip install -e .

or

.. code-block:: bash

    git clone git@github.com:NIC-MichalLabedzki/nf.git
    cd nf
    python setup.py # or python -m pip install -e .

To update:

.. code-block:: bash

    python -m pip install nf -U

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

TMUX/SCREEN used by `nf` or how to test it
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
nf 1.5.0
~~~~~~~~

1. $HOME/.nf directory and "versions" subdir to downloaded versions
2. cache --try-version
3. WSL support