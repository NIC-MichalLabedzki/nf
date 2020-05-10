from __future__ import print_function as _print_function

import mock
import pytest
import sys
import os

#===============================================================================
# fixtures and utils
#===============================================================================

tmp_fake_apps = os.path.abspath(os.path.join('tests', 'tmp_fake_apps'))

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


@pytest.fixture(scope='function')
def fixture_remove_fake_apps():

    def remove_fake_apps(tmp_fake_apps):
        if os.path.exists(tmp_fake_apps):
            for root, dirs, files in os.walk(tmp_fake_apps, topdown=False):
                for name in files:
                    try:
                        os.remove(os.path.join(root, name))
                    except Exception as e:
                        import time
                        time.sleep(1)
                        os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(tmp_fake_apps)

    remove_fake_apps(tmp_fake_apps)
    os.mkdir(tmp_fake_apps)
    yield
    remove_fake_apps(tmp_fake_apps)


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
        ('gdbus', shutil_which_none),
        ('gdbus', shutil_which_found),
        ('notify-send', shutil_which_none),
        ('notify-send', shutil_which_found),
        ('termux-notification', shutil_which_none),
        ('termux-notification', shutil_which_found),
        ('win10toast', win10toast),
        ('win10toast-persist', win10toast),
        ('plyer', plyer),
        ('plyer_toast', plyer),
        ('ssh', shutil_which_none),
        ('ssh', shutil_which_found),
        ('paramiko', mock.MagicMock()),
        ('stdout', mock.MagicMock())
    ]


#===============================================================================
# real tests
#===============================================================================

@pytest.mark.real
def test_main_ls(fixture_environment):
    sys_argv = sys.argv
    sys.argv = ['nf', 'ls']

    with pytest.raises(SystemExit) as exit_e:
        import nf
        nf.main()

    sys.argv = sys_argv

    assert exit_e.value.code == 0


@pytest.mark.real
def test_main_ls_not_exist(fixture_environment):
    sys_argv = sys.argv
    sys.argv = ['nf', 'ls not_exist']

    with pytest.raises(SystemExit) as exit_e:
        import nf
        nf.main()

    sys.argv = sys_argv

    assert exit_e.value.code != 0


@pytest.mark.real
def test_main_ls_print(fixture_environment):
    sys_argv = sys.argv
    sys.argv = ['nf', '-p', 'ls']

    with pytest.raises(SystemExit) as exit_e:
        import nf
        nf.main()

    sys.argv = sys_argv

    assert exit_e.value.code == 0


@pytest.mark.real
def test_main_ls_label(fixture_environment):
    sys_argv = sys.argv
    sys.argv = ['nf', '-l', 'this is label', 'ls']

    with pytest.raises(SystemExit) as exit_e:
        import nf
        nf.main()

    sys.argv = sys_argv

    assert exit_e.value.code == 0


@pytest.mark.real
def test_main_ls_no_notify(fixture_environment):
    sys_argv = sys.argv
    sys.argv = ['nf', '-n', 'ls']

    with pytest.raises(SystemExit) as exit_e:
        import nf
        nf.main()

    sys.argv = sys_argv

    assert exit_e.value.code == 0


@pytest.mark.real
def test_main_no_module_dbus(fixture_environment):
    sys_argv = sys.argv
    sys.argv = ['nf', 'ls']

    module_name = 'dbus'
    module_backup = sys.modules[module_name] if module_name in sys.modules else None
    sys.modules[module_name] = None

    with pytest.raises(SystemExit) as exit_e:
        import nf
        nf.main()

    sys.modules[module_name] = module_backup
    sys.argv = sys_argv

    assert exit_e.value.code == 0


@pytest.mark.real
def test_main_no_module_shutil(fixture_environment):
    sys_argv = sys.argv
    sys.argv = ['nf', '-p', 'ls']

    module_name = 'shutil'
    module_backup = sys.modules[module_name] if module_name in sys.modules else None
    sys.modules[module_name] = None

    with pytest.raises(SystemExit) as exit_e:
        import nf
        nf.main()

    sys.modules[module_name] = module_backup
    sys.argv = sys_argv

    assert exit_e.value.code == 0


@pytest.mark.real
def test_main_module_shutil_cannot_get_terminal_size(fixture_environment):
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

    sys.modules[module_name] = module_backup
    sys.argv = sys_argv

    assert exit_e.value.code == 0


@pytest.mark.real
def test_main_module_dbus_error(fixture_environment):
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

    sys.modules[module_name] = module_backup
    sys.argv = sys_argv

    assert exit_e.value.code == 0

#===============================================================================
# CI tests
#===============================================================================

def test_tool_runable(fixture_environment):
    sys_argv = sys.argv
    sys.argv = ['nf']

    with pytest.raises(SystemExit) as exit_e:
        import runpy
        runpy.run_module('nf', run_name= "__main__")

    sys.argv = sys_argv

    assert exit_e.value.code == 0


def test_main_no_args(fixture_environment):
    sys_argv = sys.argv
    sys.argv = ['nf']

    with pytest.raises(SystemExit) as exit_e:
        import nf
        nf.main()

    sys.argv = sys_argv

    assert exit_e.value.code == 0


def test_main_module_all_mock(fixture_environment):
    sys_argv = sys.argv
    sys.argv = ['nf', '-p', 'echo']

    module_backup = {}
    modules = ['dbus', 'shutil', 'distutils.spawn']
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

    for module_name in modules:
        sys.modules[module_name] = module_backup[module_name]
    sys.argv = sys_argv

    assert exit_e.value.code == 0


def test_main_module_all_mock_custom_notification_title(fixture_environment, capsys):
    my_text = 'my text'
    sys_argv = sys.argv
    sys.argv = ['nf', '-p', '--custom_notification_title', my_text, 'echo']

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

    captured = capsys.readouterr()

    for module_name in modules:
        sys.modules[module_name] = module_backup[module_name]
    sys.argv = sys_argv

    stdout = captured.out.splitlines()

    assert exit_e.value.code == 0
    assert stdout[1] == my_text


def test_main_module_all_mock_custom_notification_text(fixture_environment, capsys):
    my_text = 'my text'
    sys_argv = sys.argv
    sys.argv = ['nf', '-p', '--custom_notification_text', my_text, 'echo']

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

    captured = capsys.readouterr()

    for module_name in modules:
        sys.modules[module_name] = module_backup[module_name]
    sys.argv = sys_argv

    stdout = captured.out.splitlines()

    assert exit_e.value.code == 0
    assert stdout[2] == my_text


def test_main_module_all_mock_custom_notification_exit_code(fixture_environment):
    my_exit_code = 13
    sys_argv = sys.argv
    sys.argv = ['nf', '-p', '--custom_notification_exit_code', str(my_exit_code), 'echo']

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

    for module_name in modules:
        sys.modules[module_name] = module_backup[module_name]
    sys.argv = sys_argv

    assert exit_e.value.code == my_exit_code


@pytest.mark.skipif(sys.platform == "win32", reason="Linux specific test")
def test_main_module_all_mock_ctrl_c(fixture_environment):
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


@pytest.mark.skipif(sys.platform == "win32", reason="Linux specific test")
def test_main_module_all_mock_ctrl_c_mock_signal(fixture_environment):
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

    for module_name in modules:
        sys.modules[module_name] = module_backup[module_name]
    sys.argv = sys_argv

    assert exit_e.value.code == 0


def test_main_module_all_mock_save(fixture_environment):
    with open('.nf', 'w'):
        pass

    sys_argv = sys.argv
    sys.argv = ['nf', '-s', 'echo']

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

    for module_name in modules:
        sys.modules[module_name] = module_backup[module_name]
    sys.argv = sys_argv

    assert exit_e.value.code == 0

    with open('.nf') as f:
        line = f.read().splitlines()
        assert line[0] == 'echo'
        assert line[1] =='Exit code: 0'
        assert line[2][:6] =='Start '
        assert line[3][:6] =='Stop  '
        assert line[4][:6] =='Diff  '
        assert line[5] =='----------'


@pytest.mark.parametrize("python_version", [(3, 4), (3,7)])
@pytest.mark.parametrize("backend", ['paramiko', 'ssh', 'dbus', 'gdbus', 'notify-send', 'termux-notification', 'win10toast-persist', 'win10toast', 'plyer', 'plyer_toast', 'stdout'])
def test_main_module_all_mock_backend(fixture_environment, backend, python_version):
    sys_argv = sys.argv
    sys.argv = ['nf', '--debug', '--label', 'test_label1', '--backend={}'.format(backend), 'echo']

    if sys.version_info < (3,5) and python_version >= (3,5):
        pytest.skip("Test require python {}, but you are {}".format(python_version, sys.version_info))

    sys_version_info = sys.version_info

    from collections import namedtuple
    fake_python_version = namedtuple('version_info', 'major minor micro releaselevel serial')
    sys.version_info = fake_python_version(python_version[0], python_version[1], sys.version_info.micro, sys.version_info.releaselevel, sys.version_info.serial)


    module_backup = {}
    modules = ['dbus', 'win10toast-persist', 'win10toast', 'subprocess', 'getpass', 'paramiko']
    for module_name in modules:
        module_backup[module_name] = sys.modules[module_name] if module_name in sys.modules else None

        module_mock = mock.MagicMock()
        setattr(module_mock, '__spec__', module_mock)

        if module_name == 'paramiko':
            module_mock.SSHClient.return_value.exec_command.return_value = (mock.MagicMock(), mock.MagicMock(), mock.MagicMock())

        sys.modules[module_name] = module_mock

    if backend == 'ssh' or backend == 'paramiko':
        import os
        os.environ['SSH_CLIENT'] = '127.0.0.1 1234 5678'

    with pytest.raises(SystemExit) as exit_e:
        import nf
        nf.main()
    # assert exit_e.value.code == 0  # there is a mock (subprocess), so check this is useless

    if backend == 'ssh' or backend == 'paramiko':
        del os.environ['SSH_CLIENT']

    for module_name in modules:
        sys.modules[module_name] = module_backup[module_name]
    sys.argv = sys_argv
    sys.version_info = sys_version_info


@pytest.mark.parametrize("python_version", [(3, 4), (3,7)])
@pytest.mark.parametrize("backend", ['paramiko', 'dbus', 'gdbus', 'notify-send', 'termux-notification', 'win10toast-persist', 'win10toast', 'plyer', 'plyer_toast', 'stdout'])
def test_main_module_all_mock_bad_import_backend(fixture_environment, backend, python_version):
    sys_argv = sys.argv
    sys.argv = ['nf', '--debug', '--label', 'test_label2', '--backend={}'.format(backend), 'echo']

    if sys.version_info < (3,5) and python_version >= (3,5):
        pytest.skip("Test require python {}, but you are {}".format(python_version, sys.version_info))

    sys_version_info = sys.version_info

    from collections import namedtuple
    fake_python_version = namedtuple('version_info', 'major minor micro releaselevel serial')
    sys.version_info = fake_python_version(python_version[0], python_version[1], sys.version_info.micro, sys.version_info.releaselevel, sys.version_info.serial)

    module_backup = {}
    modules = ['dbus', 'win10toast-persist', 'win10toast', 'shutil', 'distutils.spawn', 'plyer', 'getpass']
    for module_name in modules:
        module_backup[module_name] = sys.modules[module_name] if module_name in sys.modules else None

        if sys_version_info.major == 3 and sys_version_info.minor == 9 and module_name == 'shutil':
            # TODO: better solution?
            pass
        else:
            sys.modules[module_name] = None

    with pytest.raises(SystemExit) as exit_e:
        import nf
        nf.main()

    for module_name in modules:
        sys.modules[module_name] = module_backup[module_name]
    sys.argv = sys_argv
    sys.version_info = sys_version_info

    assert exit_e.value.code == 0


@pytest.mark.parametrize("python_version", [(3, 4), (3,7)])
@pytest.mark.parametrize("backend, method_mock", get_method_mocks())
def test_main_module_all_mock_bad_functionality_backend(fixture_environment, backend, method_mock, python_version):
    sys_argv = sys.argv
    sys.argv = ['nf', '--debug', '--label', 'test_label3_{}'.format(backend), '--backend={}'.format(backend), 'echo']

    if sys.version_info < (3,5) and python_version >= (3,5):
        pytest.skip("Test require python {}, but you are {}".format(python_version, sys.version_info))
    sys_version_info = sys.version_info

    from collections import namedtuple
    fake_python_version = namedtuple('version_info', 'major minor micro releaselevel serial')
    sys.version_info = fake_python_version(python_version[0], python_version[1], sys.version_info.micro, sys.version_info.releaselevel, sys.version_info.serial)

    import os
    os.environ['PATH'] = os.path.abspath('tests/fake_apps/') + ':' + os.environ['PATH']

    module_backup = {}
    modules = ['dbus', 'win10toast-persist', 'win10toast', 'shutil', 'distutils.spawn', 'plyer', 'getpass']
    for module_name in modules:
        module_backup[module_name] = sys.modules[module_name] if module_name in sys.modules else None

        if sys_version_info.major == 3 and sys_version_info.minor == 9 and module_name == 'shutil':
            # TODO: better solution?
            pass
        else:
            module_mock = method_mock
            setattr(module_mock, '__spec__', module_mock)
            sys.modules[module_name] = module_mock

    if backend == 'ssh' or backend == 'paramiko':
        os.environ['SSH_CLIENT'] = '127.0.0.1 1234 5678'

    with pytest.raises(SystemExit) as exit_e:
        import nf
        nf.main()

    if backend == 'ssh' or backend == 'paramiko':
        del os.environ['SSH_CLIENT']

    for module_name in modules:
        sys.modules[module_name] = module_backup[module_name]

    sys.argv = sys_argv
    sys.version_info = sys_version_info

    assert exit_e.value.code == 0


def test_yakuake_support(fixture_environment, capsys):
    def prepare():
        test_environment = {'modules': ['psutil', 'dbus'],
                            'module_backup': {}}

        for module_name in test_environment['modules']:
            test_environment['module_backup'][module_name] = sys.modules[module_name] if module_name in sys.modules else None

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

        return test_environment

    def post(test_environment):
        for module_name in test_environment['modules']:
            print('TEST_DEBUG: ', module_name, sys.modules[module_name].mock_calls)
            sys.modules[module_name] = test_environment['module_backup'][module_name]

    test_environment = prepare()

    import nf
    exit_code = nf.nf(['-ndp', 'echo'])

    post(test_environment)

    captured = capsys.readouterr()

    stdout = [log for log in captured.out.splitlines() if not log.startswith('DEBUG')]
    print(captured.out)

    assert exit_code == 0
    assert stdout[1] == 'echo [yakuake_tab_title]'


@pytest.mark.parametrize("is_case_ppid", [False, True])
def test_konsole_support(fixture_environment, capsys, is_case_ppid):

    def prepare():
        test_environment = {'modules': ['psutil', 'dbus'],
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

        import os

        os.environ['KONSOLE_VERSION'] = 'mock'
        os.environ['KONSOLE_DBUS_SERVICE'] = 'mock'
        os.environ['KONSOLE_DBUS_SESSION'] = 'mock'


        return test_environment

    def post(test_environment):
        import os

        del os.environ['KONSOLE_VERSION']
        del os.environ['KONSOLE_DBUS_SERVICE']
        del os.environ['KONSOLE_DBUS_SESSION']


        for module_name in test_environment['modules']:
            print('TEST_DEBUG: ', module_name, sys.modules[module_name].mock_calls)
            sys.modules[module_name] = test_environment['module_backup'][module_name]

    test_environment = prepare()

    import nf
    exit_code = nf.nf(['-ndp', 'echo'])

    post(test_environment)

    captured = capsys.readouterr()

    stdout = [log for log in captured.out.splitlines() if not log.startswith('DEBUG')]
    print(captured.out)

    assert exit_code == 0
    assert stdout[1] == 'echo [konsole_tab_title]'


def test_screen_support(fixture_remove_fake_apps, fixture_environment, capsys):
    import os

    def prepare():
        test_environment = {'modules': ['psutil'],
                            'module_backup': {}}
        for module_name in test_environment['modules']:
            test_environment['module_backup'][module_name] = sys.modules[module_name] if module_name in sys.modules else None

            module_mock = mock.MagicMock()
            process_mock = mock.MagicMock()
            process_mock.exe.return_value = "exe_text"
            process_mock.cmdline.return_value = "cmdline_text"
            process_mock.name.return_value = 'name_text'
            module_mock.Process.return_value = process_mock

            setattr(module_mock, '__spec__', module_mock)

            sys.modules[module_name] = module_mock

        os.environ['STY'] = '/dev/null'

        my_app = '''#!/usr/bin/env python
import sys
if sys.argv[1:] == ['-q', '-Q', 'title']:
    print('screen_window_title')
else:
    sys.exit(2)
'''
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

        return test_environment


    def post(test_environment):
        for module_name in test_environment['modules']:
            sys.modules[module_name] = test_environment['module_backup'][module_name]

    test_environment = prepare()

    import nf
    exit_code = nf.nf(['-ndp', 'echo'])

    captured = capsys.readouterr()

    stdout = [log for log in captured.out.splitlines() if not log.startswith('DEBUG')]
    print(captured.out)

    post(test_environment)

    assert exit_code == 0
    assert stdout[1] == 'echo [screen_window_title]'


@pytest.mark.parametrize("is_case_ppid", [False, True])
def test_tmux_support(fixture_remove_fake_apps, fixture_environment, capsys, is_case_ppid):
    import os

    def prepare():
        test_environment = {'modules': ['psutil', 'dbus'],
                            'module_backup': {}}
        for module_name in test_environment['modules']:
            test_environment['module_backup'][module_name] = sys.modules[module_name] if module_name in sys.modules else None

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

        os.environ['TMUX'] = '/dev/null'

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

        return test_environment

    def post(test_environment):
        for module_name in test_environment['modules']:
            sys.modules[module_name] = test_environment['module_backup'][module_name]

    test_environment = prepare()

    import nf
    exit_code = nf.nf(['-ndp', 'echo'])

    captured = capsys.readouterr()

    stdout = [log for log in captured.out.splitlines() if not log.startswith('DEBUG')]
    print(captured.out)

    post(test_environment)

    assert exit_code == 0
    assert stdout[1] == 'echo [session -> 1 window -> 1 pane]'


@pytest.mark.parametrize("ssh_script_index", [0, 1, 2])
@pytest.mark.parametrize("python_version", [(2, 7), (3,3)])
def test_backend_ssh(capsys, fixture_remove_fake_apps, fixture_environment, fixture_python_version, ssh_script_index, python_version):
    import sys
    if sys.version_info < (3, 0):
        pytest.skip("Test unfortunately does not work with python < 3.0, python hangs anf this is related to sys.exit() in fake app script".format((3, 0), sys.version_info))
    fixture_python_version(python_version)
    import os

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
        test_environment = {'modules': ['psutil'],
                            'module_backup': {}}
        for module_name in test_environment['modules']:
            test_environment['module_backup'][module_name] = sys.modules[module_name] if module_name in sys.modules else None

            module_mock = mock.MagicMock()
            process_mock = mock.MagicMock()
            process_mock.exe.return_value = "exe_text"
            process_mock.cmdline.return_value = "cmdline_text"
            process_mock.name.return_value = 'name_text'
            module_mock.Process.return_value = process_mock

            setattr(module_mock, '__spec__', module_mock)

            sys.modules[module_name] = module_mock

        os.environ['SSH_CLIENT'] = '127.0.0.1 5555 6666'

        ssh_app = os.path.join(tmp_fake_apps, 'ssh')
        with open(ssh_app, 'w') as f:
            f.write(ssh_script[ssh_script_index])
        os.chmod(ssh_app, 0o777)

        os.environ['PATH'] = os.path.abspath(tmp_fake_apps) + ':' + os.environ['PATH']

        return test_environment

    def post(test_environment):
        for module_name in test_environment['modules']:
            sys.modules[module_name] = test_environment['module_backup'][module_name]


    test_environment = prepare()

    import nf
    exit_code = nf.nf(['-dp', '--backend', 'ssh', 'echo'])

    captured = capsys.readouterr()
    stdout = [log for log in captured.out.splitlines() if not log.startswith('DEBUG')]
    print(captured.out)

    post(test_environment)

    assert exit_code == 0
    assert stdout[1] == 'echo'


@pytest.mark.parametrize("backend", ['paramiko', 'ssh'])
def test_ssh_no_ssh_environment_variable(fixture_environment, backend):
    # below is done by: fixture_environment
    # import os
    # del os.environ['SSH_CLIENT']
    import nf
    exit_code = nf.nf(['-dp', '--backend', backend, 'echo'])

    assert exit_code == 0


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
    exit_code = nf.nf(['-dp', '--backend', 'stdout', 'echo'])

    if module_backup[module_name] is not None:
        sys.modules[module_name] = module_backup[module_name]

    assert exit_code == 0


@pytest.mark.skipif(sys.platform == "win32", reason="Linux specific test")
def test_detach_unix_parent(fixture_environment):
    import os

    fork = os.fork
    os.fork = mock.Mock()
    os.fork.return_value = 5

    os_exit = os._exit
    os._exit = mock.Mock()

    import nf
    exit_code = nf.nf(['-dp', '--detach', '--backend', 'stdout', 'echo'])

    os.fork = fork
    os._exit = os_exit

    assert exit_code == 'detached'


@pytest.mark.skipif(sys.platform == "win32", reason="Linux specific test")
def test_detach_unix_child(fixture_environment):
    import os

    fork = os.fork
    os.fork = mock.Mock()
    os.fork.return_value = 0

    import nf
    exit_code = nf.nf(['-dp', '--detach', '--backend', 'stdout', 'echo'])

    os.fork = fork

    assert exit_code == 0


@pytest.mark.parametrize("python_version", [(3, 5), (3, 7)])
def test_detach_win(fixture_environment, fixture_python_version, python_version):
    import sys
    import subprocess

    fixture_python_version(python_version)

    platform = sys.platform
    sys.platform = 'win32'

    popen = subprocess.Popen
    subprocess.Popen = mock.Mock()

    old_CREATE_NEW_PROCESS_GROUP =  getattr(subprocess, 'CREATE_NEW_PROCESS_GROUP') if hasattr(subprocess, 'CREATE_NEW_PROCESS_GROUP') else None
    old_DETACHED_PROCESS =  getattr(subprocess, 'DETACHED_PROCESS') if hasattr(subprocess, 'DETACHED_PROCESS') else None
    subprocess.CREATE_NEW_PROCESS_GROUP = -1
    subprocess.DETACHED_PROCESS = -1

    import nf
    exit_code = nf.nf(['-dp', '--detach', '--backend', 'stdout', 'echo'])

    sys.platform = platform
    subprocess.Popen = popen
    subprocess.CREATE_NEW_PROCESS_GROUP = old_CREATE_NEW_PROCESS_GROUP
    subprocess.DETACHED_PROCESS = old_DETACHED_PROCESS

    assert exit_code == 0


def test_wait_for_pid(fixture_environment, capsys):
    import time
    import subprocess
    import sys

    pid1 = subprocess.Popen([sys.executable, '-c', 'import time;time.sleep(1)']).pid
    pid2 = subprocess.Popen([sys.executable, '-c', 'import time;time.sleep(1)']).pid

    import nf
    start = time.time()
    exit_code = nf.nf(['-dp', '--wait-for-pid', str(pid1), '--wait-for-pid', str(pid2), '--backend', 'stdout', 'echo'])
    end = time.time()

    captured = capsys.readouterr()
    stdout = [log for log in captured.out.splitlines() if not log.startswith('DEBUG')]

    spent = end - start
    assert exit_code == 0
    assert spent > 0.5


@pytest.mark.skipif(sys.platform == "win32" or sys.platform == "darwin", reason="Linux specific test")
def test_wait_for_pid_no_psutil(fixture_environment, capsys):
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

    import time
    import subprocess
    import sys

    pid1 = subprocess.Popen([sys.executable, '-c', 'import time;time.sleep(1)']).pid
    pid2 = subprocess.Popen([sys.executable, '-c', 'import time;time.sleep(1)']).pid

    import nf
    start = time.time()
    exit_code = nf.nf(['-dp', '--wait-for-pid', str(pid1), '--wait-for-pid', str(pid2), '--backend', 'stdout', 'echo'])
    end = time.time()

    captured = capsys.readouterr()
    stdout = [log for log in captured.out.splitlines() if not log.startswith('DEBUG')]

    if module_backup[module_name] is not None:
        sys.modules[module_name] = module_backup[module_name]

    assert exit_code == 0
    assert end - start > 0.5


def test_debugfile(fixture_environment):
    test_file = 'tmp_debugfile'

    import nf
    exit_code = nf.nf(['-dp', '--debugfile', test_file, '--backend', 'stdout', 'echo'])
    import os

    try:
        os.remove(test_file)
    except:
        import time
        time.sleep(1)
        os.remove(test_file)

    assert exit_code == 0


def test_closed_stdout(fixture_environment):
    test_file = 'tmp_debugfile'
    stdout = sys.stdout
    sys.stdout = 0 # cause AttributeError: 'int' object has no attribute 'write'

    import nf
    exit_code = nf.nf(['-dp', '--debugfile', test_file, '--backend', 'stdout', 'echo'])

    sys.stdout = stdout
    import os
    with open(test_file) as f:
        print(f.read())
    try:
        os.remove(test_file)
    except:
        import time
        time.sleep(1)
        os.remove(test_file)

    assert exit_code == 0


def test_wsl(fixture_environment):
    test_file = 'tmp_debugfile'

    import nf
    exit_code = nf.nf(['-dp', '--debugfile', test_file, '--backend', 'wsl', 'echo'])
    import os

    try:
        os.remove(test_file)
    except:
        import time
        time.sleep(1)
        os.remove(test_file)

    assert exit_code == 0


@pytest.mark.slow
def test_readme_rst():
    import rstcheck
    with open('README.rst') as f:
        readme = f.read()
    errors = list(rstcheck.check(readme))

    assert errors == []
