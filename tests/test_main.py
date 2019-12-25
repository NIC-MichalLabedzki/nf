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

    stdout = captured.out.split('\n')
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

    stdout = captured.out.split('\n')
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
        line = f.read().split('\n')
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
    sys.argv = ['nf', '--label', 'test_label1', '--backend={}'.format(backend), 'ls']

    if sys.version_info < (3,5) and python_version >= (3,5):
        pytest.skip("Test require python {}, but you are {}".format(python_version, sys.version_info))

    sys_version_info = sys.version_info
    sys.version_info = python_version

    module_backup = {}
    modules = ['dbus', 'win10toast', 'subprocess', 'getpass']
    for module_name in modules:
        module_backup[module_name] = sys.modules[module_name] if module_name in sys.modules else None

        module_mock = mock.MagicMock()
        setattr(module_mock, '__spec__', module_mock)

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
@pytest.mark.parametrize("backend", ['dbus', 'notify-send', 'termux-notification', 'win10toast', 'plyer', 'plyer_toast', 'stdout'])
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

@pytest.mark.slow
def test_readme_rst():
    import rstcheck
    with open('README.rst') as f:
        readme = f.read()
    errors = list(rstcheck.check(readme))

    assert errors == []
