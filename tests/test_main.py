from __future__ import print_function as _print_function

import mock
import pytest
import sys

def test_tool_runable():
    with pytest.raises(SystemExit) as exit_e:
        import runpy
        runpy.run_module('nf', run_name= "__main__")
    assert exit_e.value.code == 2

def test_main_no_args():
    with pytest.raises(SystemExit) as exit_e:
        import nf
        nf.main()
    assert exit_e.value.code == 2


@pytest.mark.real
def test_main_ls():
    import os
    if 'SSH_CLIENT' in os.environ:
        ssh_client = os.environ['SSH_CLIENT']
        del os.environ['SSH_CLIENT']
    else:
        ssh_client = None

    sys_argv = sys.argv
    sys.argv = ['nf', 'ls']
    with pytest.raises(SystemExit) as exit_e:
        import nf
        nf.main()
    assert exit_e.value.code == 0
    sys.argv = sys_argv
    if ssh_client:
        os.environ['SSH_CLIENT'] = ssh_client


@pytest.mark.real
def test_main_ls_not_exist():
    import os
    if 'SSH_CLIENT' in os.environ:
        ssh_client = os.environ['SSH_CLIENT']
        del os.environ['SSH_CLIENT']
    else:
        ssh_client = None

    sys_argv = sys.argv
    sys.argv = ['nf', 'ls not_exist']
    with pytest.raises(SystemExit) as exit_e:
        import nf
        nf.main()
    assert exit_e.value.code != 0
    sys.argv = sys_argv
    if ssh_client:
        os.environ['SSH_CLIENT'] = ssh_client


@pytest.mark.real
def test_main_ls_print():
    import os
    if 'SSH_CLIENT' in os.environ:
        ssh_client = os.environ['SSH_CLIENT']
        del os.environ['SSH_CLIENT']
    else:
        ssh_client = None

    sys_argv = sys.argv
    sys.argv = ['nf', '-p', 'ls']
    with pytest.raises(SystemExit) as exit_e:
        import nf
        nf.main()
    assert exit_e.value.code == 0
    sys.argv = sys_argv
    if ssh_client:
        os.environ['SSH_CLIENT'] = ssh_client


@pytest.mark.real
def test_main_ls_label():
    import os
    if 'SSH_CLIENT' in os.environ:
        ssh_client = os.environ['SSH_CLIENT']
        del os.environ['SSH_CLIENT']
    else:
        ssh_client = None

    sys_argv = sys.argv
    sys.argv = ['nf', '-l', 'this is label', 'ls']
    with pytest.raises(SystemExit) as exit_e:
        import nf
        nf.main()
    assert exit_e.value.code == 0
    sys.argv = sys_argv
    if ssh_client:
        os.environ['SSH_CLIENT'] = ssh_client


@pytest.mark.real
def test_main_ls_no_notify():
    import os
    if 'SSH_CLIENT' in os.environ:
        ssh_client = os.environ['SSH_CLIENT']
        del os.environ['SSH_CLIENT']
    else:
        ssh_client = None

    sys_argv = sys.argv
    sys.argv = ['nf', '-n', 'ls']
    with pytest.raises(SystemExit) as exit_e:
        import nf
        nf.main()
    assert exit_e.value.code == 0
    sys.argv = sys_argv
    if ssh_client:
        os.environ['SSH_CLIENT'] = ssh_client


@pytest.mark.real
def test_main_no_module_dbus():
    import os
    if 'SSH_CLIENT' in os.environ:
        ssh_client = os.environ['SSH_CLIENT']
        del os.environ['SSH_CLIENT']
    else:
        ssh_client = None

    sys_argv = sys.argv
    sys.argv = ['nf', 'ls']
    type(sys.modules)

    module_name = 'dbus'
    module_backup = sys.modules[module_name] if module_name in sys.modules else None
    sys.modules[module_name] = None

    with pytest.raises(SystemExit) as exit_e:
        import nf
        nf.main()
    assert exit_e.value.code == 0
    sys.modules[module_name] = module_backup
    sys.argv = sys_argv
    if ssh_client:
        os.environ['SSH_CLIENT'] = ssh_client


@pytest.mark.real
def test_main_no_module_shutil():
    import os
    if 'SSH_CLIENT' in os.environ:
        ssh_client = os.environ['SSH_CLIENT']
        del os.environ['SSH_CLIENT']
    else:
        ssh_client = None

    sys_argv = sys.argv
    sys.argv = ['nf', '-p', 'ls']

    module_name = 'shutil'
    module_backup = sys.modules[module_name] if module_name in sys.modules else None
    sys.modules[module_name] = None

    with pytest.raises(SystemExit) as exit_e:
        import nf
        nf.main()
    assert exit_e.value.code == 0
    sys.modules[module_name] = module_backup
    sys.argv = sys_argv
    if ssh_client:
        os.environ['SSH_CLIENT'] = ssh_client


@pytest.mark.real
def test_main_module_shutil_cannot_get_terminal_size():
    import os
    if 'SSH_CLIENT' in os.environ:
        ssh_client = os.environ['SSH_CLIENT']
        del os.environ['SSH_CLIENT']
    else:
        ssh_client = None

    sys_argv = sys.argv
    sys.argv = ['nf', '-p', 'ls']

    module_name = 'shutil'
    module_backup = sys.modules[module_name] if module_name in sys.modules else None

    class my_shutil:
        __spec__ = mock.Mock()

        def get_terminal_size(self, a):
            raise Exception

    sys.modules[module_name] = my_shutil

    with pytest.raises(SystemExit) as exit_e:
        import nf
        nf.main()
    assert exit_e.value.code == 0
    sys.modules[module_name] = module_backup
    sys.argv = sys_argv
    if ssh_client:
        os.environ['SSH_CLIENT'] = ssh_client


@pytest.mark.real
def test_main_module_dbus_error():
    import os
    if 'SSH_CLIENT' in os.environ:
        ssh_client = os.environ['SSH_CLIENT']
        del os.environ['SSH_CLIENT']
    else:
        ssh_client = None

    sys_argv = sys.argv
    sys.argv = ['nf', '-p', 'ls']

    module_name = 'dbus'
    module_backup = sys.modules[module_name] if module_name in sys.modules else None

    class my_dbus:
        __spec__ = mock.Mock()

        def SessionBus(self):
            raise Exception

    sys.modules[module_name] = my_dbus

    with pytest.raises(SystemExit) as exit_e:
        import nf
        nf.main()
    assert exit_e.value.code == 0
    sys.modules[module_name] = module_backup
    sys.argv = sys_argv
    if ssh_client:
        os.environ['SSH_CLIENT'] = ssh_client


def test_main_module_all_mock():
    import os
    if 'SSH_CLIENT' in os.environ:
        ssh_client = os.environ['SSH_CLIENT']
        del os.environ['SSH_CLIENT']
    else:
        ssh_client = None

    sys_argv = sys.argv
    sys.argv = ['nf', '-p', 'ls']

    module_backup = {}
    modules = ['dbus', 'shutil']
    for module_name in modules:
        module_backup[module_name] = sys.modules[module_name] if module_name in sys.modules else None

        module_mock = mock.MagicMock()
        setattr(module_mock, '__spec__', module_mock)
        if module_name == 'shutil':
            from collections import namedtuple
            size = namedtuple("terminal_size", "columns lines")
            module_mock.get_terminal_size.return_value = size(80, 20)

        sys.modules[module_name] = module_mock

    with pytest.raises(SystemExit) as exit_e:
        import nf
        nf.main()
    assert exit_e.value.code == 0

    for module_name in modules:
        sys.modules[module_name] = module_backup[module_name]
    sys.argv = sys_argv
    if ssh_client:
        os.environ['SSH_CLIENT'] = ssh_client


def test_main_module_all_mock_custom_notification_title(capsys):
    import os
    if 'SSH_CLIENT' in os.environ:
        ssh_client = os.environ['SSH_CLIENT']
        del os.environ['SSH_CLIENT']
    else:
        ssh_client = None

    sys_argv = sys.argv
    my_text = 'my text'
    sys.argv = ['nf', '-p', '--custom_notification_title', my_text, 'ls']

    module_backup = {}
    modules = ['dbus']
    for module_name in modules:
        module_backup[module_name] = sys.modules[module_name] if module_name in sys.modules else None

        module_mock = mock.MagicMock()
        setattr(module_mock, '__spec__', module_mock)

        sys.modules[module_name] = module_mock

    with pytest.raises(SystemExit) as exit_e:
        import nf
        nf.main()
    assert exit_e.value.code == 0

    captured = capsys.readouterr()

    for module_name in modules:
        sys.modules[module_name] = module_backup[module_name]
    sys.argv = sys_argv
    if ssh_client:
        os.environ['SSH_CLIENT'] = ssh_client

    stdout = captured.out.splitlines()
    assert stdout[1] == my_text

def test_main_module_all_mock_custom_notification_text(capsys):
    import os
    if 'SSH_CLIENT' in os.environ:
        ssh_client = os.environ['SSH_CLIENT']
        del os.environ['SSH_CLIENT']
    else:
        ssh_client = None

    sys_argv = sys.argv
    my_text = 'my text'
    sys.argv = ['nf', '-p', '--custom_notification_text', my_text, 'ls']

    module_backup = {}
    modules = ['dbus']
    for module_name in modules:
        module_backup[module_name] = sys.modules[module_name] if module_name in sys.modules else None

        module_mock = mock.MagicMock()
        setattr(module_mock, '__spec__', module_mock)

        sys.modules[module_name] = module_mock

    with pytest.raises(SystemExit) as exit_e:
        import nf
        nf.main()
    assert exit_e.value.code == 0

    captured = capsys.readouterr()

    for module_name in modules:
        sys.modules[module_name] = module_backup[module_name]
    sys.argv = sys_argv
    if ssh_client:
        os.environ['SSH_CLIENT'] = ssh_client

    stdout = captured.out.splitlines()
    assert stdout[2] == my_text


def test_main_module_all_mock_custom_notification_exit_code():
    import os
    if 'SSH_CLIENT' in os.environ:
        ssh_client = os.environ['SSH_CLIENT']
        del os.environ['SSH_CLIENT']
    else:
        ssh_client = None

    sys_argv = sys.argv
    my_exit_code = 13
    sys.argv = ['nf', '-p', '--custom_notification_exit_code', str(my_exit_code), 'ls']

    module_backup = {}
    modules = ['dbus']
    for module_name in modules:
        module_backup[module_name] = sys.modules[module_name] if module_name in sys.modules else None

        module_mock = mock.MagicMock()
        setattr(module_mock, '__spec__', module_mock)

        sys.modules[module_name] = module_mock

    with pytest.raises(SystemExit) as exit_e:
        import nf
        nf.main()
    assert exit_e.value.code == my_exit_code

    for module_name in modules:
        sys.modules[module_name] = module_backup[module_name]
    sys.argv = sys_argv
    if ssh_client:
        os.environ['SSH_CLIENT'] = ssh_client


@pytest.mark.skipif(sys.platform == "win32", reason="Linux specific test")
def test_main_module_all_mock_ctrl_c():
    import os
    if 'SSH_CLIENT' in os.environ:
        ssh_client = os.environ['SSH_CLIENT']
        del os.environ['SSH_CLIENT']
    else:
        ssh_client = None

    sys_argv = sys.argv
    sys.argv = ['nf', '-n', '-p', 'sleep 2']

    import os
    import signal
    import time
    import threading

    pid = os.getpid()

    def trigger_signal():
        time.sleep(1)
        os.kill(pid, signal.SIGINT)

    thread = threading.Thread(target=trigger_signal)
    thread.start()

    with pytest.raises(SystemExit):
        import nf
        nf.main()

    sys.argv = sys_argv
    if ssh_client:
        os.environ['SSH_CLIENT'] = ssh_client


@pytest.mark.skipif(sys.platform == "win32", reason="Linux specific test")
def test_main_module_all_mock_ctrl_c_mock_signal():
    import os
    if 'SSH_CLIENT' in os.environ:
        ssh_client = os.environ['SSH_CLIENT']
        del os.environ['SSH_CLIENT']
    else:
        ssh_client = None

    sys_argv = sys.argv
    sys.argv = ['nf', '-n', '-p', '-d', 'sleep 2']

    import os
    import signal
    import time
    import threading

    pid = os.getpid()

    def trigger_signal():
        time.sleep(1)
        os.kill(pid, signal.SIGINT)

    thread = threading.Thread(target=trigger_signal)
    thread.start()

    module_backup = {}
    modules = ['signal']
    for module_name in modules:
        module_backup[module_name] = sys.modules[module_name] if module_name in sys.modules else None

        module_mock = mock.MagicMock()
        setattr(module_mock, '__spec__', module_mock)

        sys.modules[module_name] = None

    with pytest.raises(SystemExit) as exit_e:
        import nf
        nf.main()
    assert exit_e.value.code == 0

    for module_name in modules:
        sys.modules[module_name] = module_backup[module_name]
    sys.argv = sys_argv
    if ssh_client:
        os.environ['SSH_CLIENT'] = ssh_client


def test_main_module_all_mock_save():
    import os
    if 'SSH_CLIENT' in os.environ:
        ssh_client = os.environ['SSH_CLIENT']
        del os.environ['SSH_CLIENT']
    else:
        ssh_client = None

    with open('.nf', 'w'):
        pass

    sys_argv = sys.argv
    sys.argv = ['nf', '-s', 'ls']

    module_backup = {}
    modules = ['dbus']
    for module_name in modules:
        module_backup[module_name] = sys.modules[module_name] if module_name in sys.modules else None

        module_mock = mock.MagicMock()
        setattr(module_mock, '__spec__', module_mock)

        sys.modules[module_name] = module_mock

    with pytest.raises(SystemExit) as exit_e:
        import nf
        nf.main()
    assert exit_e.value.code == 0

    for module_name in modules:
        sys.modules[module_name] = module_backup[module_name]
    sys.argv = sys_argv

    with open('.nf') as f:
        line = f.read().splitlines()
        assert line[0] == 'ls'
        assert line[1] =='Exit code: 0'
        assert line[2][:6] =='Start '
        assert line[3][:6] =='Stop  '
        assert line[4][:6] =='Diff  '
        assert line[5] =='----------'
    if ssh_client:
        os.environ['SSH_CLIENT'] = ssh_client


@pytest.mark.parametrize("python_version", [(3, 4), (3,7)])
@pytest.mark.parametrize("backend", ['paramiko', 'ssh', 'dbus', 'notify-send', 'termux-notification', 'win10toast', 'plyer', 'plyer_toast', 'stdout'])
def test_main_module_all_mock_backend(backend, python_version):
    sys_argv = sys.argv
    sys.argv = ['nf', '--debug', '--label', 'test_label1', '--backend={}'.format(backend), 'ls']

    if sys.version_info < (3,5) and python_version >= (3,5):
        pytest.skip("Test require python {}, but you are {}".format(python_version, sys.version_info))

    sys_version_info = sys.version_info
    sys.version_info = python_version

    module_backup = {}
    modules = ['dbus', 'win10toast', 'subprocess', 'getpass', 'paramiko']
    for module_name in modules:
        module_backup[module_name] = sys.modules[module_name] if module_name in sys.modules else None

        module_mock = mock.MagicMock()
        setattr(module_mock, '__spec__', module_mock)

        if module_name == 'paramiko':
            module_mock.SSHClient.return_value.exec_command.return_value = (mock.MagicMock(), mock.MagicMock(), mock.MagicMock())

        sys.modules[module_name] = module_mock

    if backend == 'ssh' or backend == 'paramiko':
        import os
        if 'SSH_CLIENT' in os.environ:
            ssh_client = os.environ['SSH_CLIENT']
        else:
            ssh_client = None
        os.environ['SSH_CLIENT'] = '127.0.0.1 1234 5678'

    with pytest.raises(SystemExit) as exit_e:
        import nf
        nf.main()
    # assert exit_e.value.code == 0  # there is a mock (subprocess), so check this is useless

    if backend == 'ssh' or backend == 'paramiko':
        del os.environ['SSH_CLIENT']
        if ssh_client:
            os.environ['SSH_CLIENT'] = ssh_client

    for module_name in modules:
        sys.modules[module_name] = module_backup[module_name]
    sys.argv = sys_argv
    sys.version_info = sys_version_info

@pytest.mark.parametrize("python_version", [(3, 4), (3,7)])
@pytest.mark.parametrize("backend", ['paramiko', 'dbus', 'notify-send', 'termux-notification', 'win10toast', 'plyer', 'plyer_toast', 'stdout'])
def test_main_module_all_mock_bad_import_backend(backend, python_version):
    sys_argv = sys.argv
    sys.argv = ['nf', '--debug', '--label', 'test_label2', '--backend={}'.format(backend), 'ls']

    if sys.version_info < (3,5) and python_version >= (3,5):
        pytest.skip("Test require python {}, but you are {}".format(python_version, sys.version_info))

    sys_version_info = sys.version_info
    sys.version_info = python_version

    module_backup = {}
    modules = ['dbus', 'win10toast', 'shutil', 'plyer', 'getpass']
    for module_name in modules:
        module_backup[module_name] = sys.modules[module_name] if module_name in sys.modules else None

        sys.modules[module_name] = None

    with pytest.raises(SystemExit) as exit_e:
        import nf
        nf.main()
    assert exit_e.value.code == 0

    for module_name in modules:
        sys.modules[module_name] = module_backup[module_name]
    sys.argv = sys_argv
    sys.version_info = sys_version_info

def get_method_mocks():
    dbus_session_bus = mock.MagicMock()
    dbus_session_bus.SessionBus.return_value = None

    dbus_session_bus_get_object = mock.MagicMock()
    dbus_session_bus_get_object.SessionBus.return_value.get_object.return_value = None

    shutil_which_none = mock.MagicMock()
    shutil_which_none.which.return_value = None

    shutil_which_found = mock.MagicMock()
    shutil_which_found.which.return_value = '/dev/null'

    plyer = mock.MagicMock()
    plyer.notification.notify.side_effect = Exception()

    win10toast = mock.MagicMock()
    win10toast.ToastNotifier.return_value.show_toast.side_effect = Exception()

    return [
        ('dbus', dbus_session_bus),
        ('dbus', dbus_session_bus_get_object),
        ('notify-send', shutil_which_none),
        ('notify-send', shutil_which_found),
        ('termux-notification', shutil_which_none),
        ('termux-notification', shutil_which_found),
        ('win10toast', win10toast),
        ('plyer', plyer),
        ('plyer_toast', plyer),
        ('ssh', shutil_which_none),
        ('ssh', shutil_which_found),
        ('paramiko', mock.MagicMock()),
        ('stdout', mock.MagicMock())
    ]

@pytest.mark.parametrize("python_version", [(3, 4), (3,7)])
@pytest.mark.parametrize("backend, method_mock", get_method_mocks())
def test_main_module_all_mock_bad_functionality_backend(backend, method_mock, python_version):
    sys_argv = sys.argv
    sys.argv = ['nf', '--debug', '--label', 'test_label3_{}'.format(backend), '--backend={}'.format(backend), 'ls']

    if sys.version_info < (3,5) and python_version >= (3,5):
        pytest.skip("Test require python {}, but you are {}".format(python_version, sys.version_info))
    sys_version_info = sys.version_info
    sys.version_info = python_version

    import os
    path_backup = os.environ['PATH']
    os.environ['PATH'] = os.path.abspath('tests/fake_apps/') + ':' + os.environ['PATH']

    module_backup = {}
    modules = ['dbus', 'win10toast', 'shutil', 'plyer', 'getpass']
    for module_name in modules:
        module_backup[module_name] = sys.modules[module_name] if module_name in sys.modules else None

        module_mock=  method_mock
        setattr(module_mock, '__spec__', module_mock)

        sys.modules[module_name] = module_mock

    if backend == 'ssh' or backend == 'paramiko':
        if 'SSH_CLIENT' in os.environ:
            ssh_client = os.environ['SSH_CLIENT']
        else:
            ssh_client = None
        os.environ['SSH_CLIENT'] = '127.0.0.1 1234 5678'

    with pytest.raises(SystemExit) as exit_e:
        import nf
        nf.main()
    assert exit_e.value.code == 0

    if backend == 'ssh' or backend == 'paramiko':
        del os.environ['SSH_CLIENT']
        if ssh_client:
            os.environ['SSH_CLIENT'] = ssh_client

    for module_name in modules:
        sys.modules[module_name] = module_backup[module_name]

    os.environ['PATH'] = path_backup

    sys.argv = sys_argv
    sys.version_info = sys_version_info


def test_yakuake_support(capsys):
    import os
    environ_backup = []
    modules = []
    module_backup = {}

    def prepare():
        modules = ['psutil', 'dbus']
        for module_name in modules:
            module_backup[module_name] = sys.modules[module_name] if module_name in sys.modules else None

            module_mock = mock.MagicMock()

            if module_name == 'psutil':
                parent_process_mock = mock.MagicMock()

                parent_process_mock.exe.return_value = 'exe_text'
                parent_process_mock.cmdline.return_value = 'cmdline_text'
                parent_process_mock.name.return_value = 'yakuake'

                process_mock = mock.MagicMock()
                process_mock.exe.return_value = 'exe_text'
                process_mock.cmdline.return_value = 'cmdline_text'
                process_mock.name.return_value = 'nf_text'
                process_mock.parents.return_value = [parent_process_mock]

                module_mock.Process.return_value = process_mock
            elif module_name == 'dbus':
                module_mock.SessionBus.return_value.get_object.return_value.tabTitle.return_value = 'yakuake_tab_title'

            setattr(module_mock, '__spec__', module_mock)

            sys.modules[module_name] = module_mock

        environ_backup = os.environ.copy()

        if 'KONSOLE_VERSION' in os.environ:
            del os.environ['KONSOLE_VERSION']
        if 'KONSOLE_DBUS_SERVICE' in os.environ:
            del os.environ['KONSOLE_DBUS_SERVICE']
        if 'KONSOLE_DBUS_SESSION' in os.environ:
            del os.environ['KONSOLE_DBUS_SESSION']
        if 'STY' in os.environ:
            del os.environ['STY']
        if 'TMUX' in os.environ:
            del os.environ['TMUX']

    def post():
        os.environ.update(environ_backup)

        for module_name in modules:
            print('TEST_DEBUG: ', module_name, sys.modules[module_name].mock_calls)
            sys.modules[module_name] = module_backup[module_name]

    prepare()

    import nf
    nf.nf(['-ndp', 'echo'])

    captured = capsys.readouterr()

    stdout = [log for log in captured.out.splitlines() if not log.startswith('DEBUG')]
    print(captured.out)
    assert stdout[1] == 'echo [yakuake_tab_title]'

    post()


@pytest.mark.parametrize("is_case_ppid", [False, True])
def test_konsole_support(capsys, is_case_ppid):
    import os

    def prepare():
        test_environment = {'environ_backup': [],
                            'modules': ['psutil', 'dbus'],
                            'module_backup': {}}

        for module_name in test_environment['modules']:
            test_environment['module_backup'][module_name] = sys.modules[module_name] if module_name in sys.modules else None

            module_mock = mock.MagicMock()

            if module_name == 'psutil':
                parent_process_mock = mock.MagicMock()

                parent_process_mock.exe.return_value = 'exe_text'
                parent_process_mock.cmdline.return_value = 'cmdline_text'
                if is_case_ppid:
                    parent_process_mock.name.return_value = 'konsole'
                else:
                    parent_process_mock.name.return_value = 'fake_parent'

                process_mock = mock.MagicMock()
                process_mock.exe.return_value = 'exe_text'
                process_mock.cmdline.return_value = 'cmdline_text'
                process_mock.name.return_value = 'nf_text'
                process_mock.parents.return_value = [parent_process_mock]

                module_mock.Process.return_value = process_mock
            elif module_name == 'dbus':
                module_mock.SessionBus.return_value.get_object.return_value.title.return_value = 'konsole_tab_title'

            setattr(module_mock, '__spec__', module_mock)

            sys.modules[module_name] = module_mock

        test_environment['environ_backup'] = os.environ.copy()

        if 'KONSOLE_VERSION' in os.environ:
            del os.environ['KONSOLE_VERSION']
        if 'KONSOLE_DBUS_SERVICE' in os.environ:
            del os.environ['KONSOLE_DBUS_SERVICE']
        if 'KONSOLE_DBUS_SESSION' in os.environ:
            del os.environ['KONSOLE_DBUS_SESSION']
        if 'STY' in os.environ:
            del os.environ['STY']
        if 'TMUX' in os.environ:
            del os.environ['TMUX']

        os.environ['KONSOLE_VERSION'] = 'mock'
        os.environ['KONSOLE_DBUS_SERVICE'] = 'mock'
        os.environ['KONSOLE_DBUS_SESSION'] = 'mock'

        return test_environment

    def post(test_environment):
        os.environ.update(test_environment['environ_backup'])

        for module_name in test_environment['modules']:
            print('TEST_DEBUG: ', module_name, sys.modules[module_name].mock_calls)
            sys.modules[module_name] = test_environment['module_backup'][module_name]

    test_environment = prepare()

    import nf
    nf.nf(['-ndp', 'echo'])

    captured = capsys.readouterr()

    stdout = [log for log in captured.out.splitlines() if not log.startswith('DEBUG')]
    print(captured.out)

    assert stdout[1] == 'echo [konsole_tab_title]'

    post(test_environment)


def test_screen_support(capsys):
    import os
    environ_backup = []
    modules = []
    module_backup = {}

    def prepare():
        modules = ['psutil']
        for module_name in modules:
            module_backup[module_name] = sys.modules[module_name] if module_name in sys.modules else None

            module_mock = mock.MagicMock()
            process_mock = mock.MagicMock()
            process_mock.exe.return_value = "exe_text"
            process_mock.cmdline.return_value = "cmdline_text"
            process_mock.name.return_value = 'name_text'
            module_mock.Process.return_value = process_mock

            setattr(module_mock, '__spec__', module_mock)

            sys.modules[module_name] = module_mock

        environ_backup = os.environ.copy()

        if 'KONSOLE_VERSION' in os.environ:
            del os.environ['KONSOLE_VERSION']
        if 'KONSOLE_DBUS_SERVICE' in os.environ:
            del os.environ['KONSOLE_DBUS_SERVICE']
        if 'KONSOLE_DBUS_SESSION' in os.environ:
            del os.environ['KONSOLE_DBUS_SESSION']
        if 'STY' in os.environ:
            del os.environ['STY']
        if 'TMUX' in os.environ:
            del os.environ['TMUX']

        os.environ['STY'] = '/dev/null'

        my_app = '''#!/usr/bin/env python
import sys
if sys.argv[1:] == ['-q', '-Q', 'title']:
    print('screen_window_title')
else:
    sys.exit(2)
'''

        tmp_fake_apps = os.path.abspath(os.path.join('tests', 'tmp_fake_apps'))
        if os.path.exists(tmp_fake_apps):
            for root, dirs, files in os.walk(tmp_fake_apps, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(tmp_fake_apps)
        os.mkdir(tmp_fake_apps)

        test_app_name = 'screen'
        if sys.platform == "win32":
            app_py = os.path.abspath(os.path.join(tmp_fake_apps, '{}.py'.format(test_app_name)))
            with open(app_py, 'w') as f:
                f.write(my_app)

            import PyInstaller.__main__
            PyInstaller.__main__.run(['--name=%s' % test_app_name, '--onefile', '--distpath=%s' % tmp_fake_apps, app_py])

            os.environ['PATH'] = os.path.abspath(tmp_fake_apps) + ';' + os.environ['PATH']
        else:
            app = os.path.join(tmp_fake_apps, test_app_name)
            with open(app, 'w') as f:
                f.write(my_app)
            os.chmod(app, 0o777)

            os.environ['PATH'] = os.path.abspath(tmp_fake_apps) + ':' + os.environ['PATH']


    def post():
        os.environ.update(environ_backup)

        for module_name in modules:
            sys.modules[module_name] = module_backup[module_name]

    prepare()

    import nf
    nf.nf(['-ndp', 'echo'])

    captured = capsys.readouterr()

    stdout = [log for log in captured.out.splitlines() if not log.startswith('DEBUG')]
    print(captured.out)
    assert stdout[1] == 'echo [screen_window_title]'

    post()


@pytest.mark.parametrize("is_case_ppid", [False, True])
def test_tmux_support(capsys, is_case_ppid):
    import os
    environ_backup = []
    modules = []
    module_backup = {}

    def prepare():
        modules = ['psutil']
        for module_name in modules:
            module_backup[module_name] = sys.modules[module_name] if module_name in sys.modules else None

            module_mock = mock.MagicMock()
            process_mock = mock.MagicMock()
            if is_case_ppid:
                parent_process_mock = mock.MagicMock()

                parent_process_mock.exe.return_value = 'exe_text'
                parent_process_mock.cmdline.return_value = 'cmdline_text'
                parent_process_mock.name.return_value = 'tmux: server'

                process_mock.exe.return_value = 'exe_text'
                process_mock.cmdline.return_value = 'cmdline_text'
                process_mock.name.return_value = 'nf_text'
                process_mock.parents.return_value = [parent_process_mock]
            else:
                process_mock.exe.return_value = 'exe_text'
                process_mock.cmdline.return_value = 'cmdline_text'
                process_mock.name.return_value = 'name_text'
            module_mock.Process.return_value = process_mock

            setattr(module_mock, '__spec__', module_mock)

            sys.modules[module_name] = module_mock

        environ_backup = os.environ.copy()

        if 'KONSOLE_VERSION' in os.environ:
            del os.environ['KONSOLE_VERSION']
        if 'KONSOLE_DBUS_SERVICE' in os.environ:
            del os.environ['KONSOLE_DBUS_SERVICE']
        if 'KONSOLE_DBUS_SESSION' in os.environ:
            del os.environ['KONSOLE_DBUS_SESSION']
        if 'STY' in os.environ:
            del os.environ['STY']
        if 'TMUX' in os.environ:
            del os.environ['TMUX']

        os.environ['TMUX'] = '/dev/null'

        tmp_fake_apps = os.path.abspath(os.path.join('tests', 'tmp_fake_apps'))
        if os.path.exists(tmp_fake_apps):
            for root, dirs, files in os.walk(tmp_fake_apps, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(tmp_fake_apps)
        os.mkdir(tmp_fake_apps)

        my_app = '''#!/usr/bin/env python
import sys
if sys.argv[1] == 'list-window':
    print('window 1')
elif sys.argv[1] == 'list-pane':
    print('pane 1')
elif sys.argv[1:] == ['display-message', '-p', '"#{client_pid}"']:
    print('0')
elif sys.argv[1] == 'display-message':
    print('session -> 1 window -> 1 pane')
else:
    sys.exit(2)

'''
        test_app_name = 'tmux'
        if sys.platform == "win32":
            app_py = os.path.abspath(os.path.join(tmp_fake_apps, '{}.py'.format(test_app_name)))
            with open(app_py, 'w') as f:
                f.write(my_app)

            import PyInstaller.__main__
            PyInstaller.__main__.run(['--name=%s' % test_app_name, '--onefile', '--distpath=%s' % tmp_fake_apps, app_py])

            os.environ['PATH'] = os.path.abspath(tmp_fake_apps) + ';' + os.environ['PATH']
        else:
            app = os.path.join(tmp_fake_apps, test_app_name)
            with open(app, 'w') as f:
                f.write(my_app)
            os.chmod(app, 0o777)

            os.environ['PATH'] = os.path.abspath(tmp_fake_apps) + ':' + os.environ['PATH']

    def post():
        os.environ.update(environ_backup)

        for module_name in modules:
            sys.modules[module_name] = module_backup[module_name]

    prepare()

    import nf
    nf.nf(['-ndp', 'echo'])

    captured = capsys.readouterr()

    stdout = [log for log in captured.out.splitlines() if not log.startswith('DEBUG')]
    print(captured.out)
    assert stdout[1] == 'echo [session -> 1 window -> 1 pane]'

    post()

@pytest.fixture(scope='function')
def fixture_environment():
    import os

    environ_backup = os.environ.copy()

    if 'KONSOLE_VERSION' in os.environ:
        del os.environ['KONSOLE_VERSION']
    if 'KONSOLE_DBUS_SERVICE' in os.environ:
        del os.environ['KONSOLE_DBUS_SERVICE']
    if 'KONSOLE_DBUS_SESSION' in os.environ:
        del os.environ['KONSOLE_DBUS_SESSION']
    if 'STY' in os.environ:
        del os.environ['STY']
    if 'TMUX' in os.environ:
        del os.environ['TMUX']
    if 'SSH_CLIENT' in os.environ:
        del os.environ['SSH_CLIENT']

    yield

    os.environ.update(environ_backup)

@pytest.fixture(scope='function')
def fixture_python_version(request):
    import sys

    sys_version_info = sys.version_info

    def python_version(version):
        if sys.version_info < version:
            pytest.skip("Test require python {}, but you are {}".format(version, sys.version_info))
        sys.version_info = version

    yield python_version

    sys.version_info = sys_version_info

@pytest.mark.parametrize("ssh_script_index", [0, 1, 2])
@pytest.mark.parametrize("python_version", [(2, 7), (3,3)])
def test_backend_ssh(capsys, fixture_environment, fixture_python_version, ssh_script_index, python_version):
    import sys
    if sys.version_info < (3, 0):
        pytest.skip("Test unfortunately does not work with python < 3.0, python hangs anf this is related to sys.exit() in fake app script".format((3, 0), sys.version_info))
    fixture_python_version(python_version)
    import os
    modules = []
    module_backup = {}

    ssh_script = []

    ssh_script.append('''#!/usr/bin/env python
import sys
sys.exit(2)
''')

    ssh_script.append('''#!/usr/bin/env python
import time
import sys
print('password')
time.sleep(2)
sys.exit(0)
''')

    ssh_script.append('''#!/usr/bin/env python
import sys

if 'PreferredAuthentications=publickey' in sys.argv[1:]:
    sys.exit(2)
else:
    print('password')
    import time
    time.sleep(2)
    sys.exit(0)
''')

    def prepare():
        test_environment = {}
        modules = ['psutil']
        for module_name in modules:
            module_backup[module_name] = sys.modules[module_name] if module_name in sys.modules else None

            module_mock = mock.MagicMock()
            process_mock = mock.MagicMock()
            process_mock.exe.return_value = "exe_text"
            process_mock.cmdline.return_value = "cmdline_text"
            process_mock.name.return_value = 'name_text'
            module_mock.Process.return_value = process_mock

            setattr(module_mock, '__spec__', module_mock)

            sys.modules[module_name] = module_mock

        os.environ['SSH_CLIENT'] = '127.0.0.1 5555 6666'

        tmp_fake_apps = 'tests/tmp_fake_apps'
        if os.path.exists(tmp_fake_apps):
            for root, dirs, files in os.walk(tmp_fake_apps, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(tmp_fake_apps)
        os.mkdir(tmp_fake_apps)
        tmux_app = os.path.join(tmp_fake_apps, 'ssh')
        with open(tmux_app, 'w') as f:
            f.write(ssh_script[ssh_script_index])
        os.chmod(tmux_app, 0o777)

        os.environ['PATH'] = os.path.abspath('tests/tmp_fake_apps/') + ':' + os.environ['PATH']

        return test_environment

    def post(test_environment):
        for module_name in modules:
            sys.modules[module_name] = module_backup[module_name]
    test_environment = prepare()
    import nf
    nf.nf(['-dp', '--backend', 'ssh', 'echo'])

    captured = capsys.readouterr()
    stdout = [log for log in captured.out.splitlines() if not log.startswith('DEBUG')]
    print(captured.out)
    assert stdout[1] == 'echo'

    post(test_environment)


@pytest.mark.parametrize("backend", ['paramiko', 'ssh'])
def test_ssh_no_ssh_environment_variable(fixture_environment, backend):
    # below is done by: fixture_environment
    # import os
    # del os.environ['SSH_CLIENT']
    import nf
    nf.nf(['-dp', '--backend', backend, 'echo'])


def test_no_psutil(fixture_environment):
    import sys
    module_name = 'psutil'
    module_backup = {}
    if module_name in sys.modules:
        module_backup[module_name] = sys.modules[module_name]
        del sys.modules[module_name]
        sys.modules[module_name] = None
    else:
        module_backup[module_name] = None
        sys.modules[module_name] = None

# TODO: stubs for: os.readlink, open, f.read(), and tmux fake app

    import nf
    nf.nf(['-dp', '--backend', 'stdout', 'echo'])

    if module_backup[module_name] is not None:
        sys.modules[module_name] = module_backup[module_name]


@pytest.mark.slow
def test_readme_rst():
    import rstcheck
    with open('README.rst') as f:
        readme = f.read()
    errors = list(rstcheck.check(readme))

    assert errors == []
