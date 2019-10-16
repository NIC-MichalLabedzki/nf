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

def test_main_ls():
    sys_argv = sys.argv
    sys.argv = ['nf', 'ls']
    with pytest.raises(SystemExit) as exit_e:
        import nf
        nf.main()
    assert exit_e.value.code == 0
    sys.argv = sys_argv

def test_main_ls():
    sys_argv = sys.argv
    sys.argv = ['nf', 'ls not_exist']
    with pytest.raises(SystemExit) as exit_e:
        import nf
        nf.main()
    assert exit_e.value.code != 0
    sys.argv = sys_argv

def test_main_ls_print():
    sys_argv = sys.argv
    sys.argv = ['nf', '-p', 'ls']
    with pytest.raises(SystemExit) as exit_e:
        import nf
        nf.main()
    assert exit_e.value.code == 0
    sys.argv = sys_argv

def test_main_ls_label():
    sys_argv = sys.argv
    sys.argv = ['nf', '-l', 'this is label', 'ls']
    with pytest.raises(SystemExit) as exit_e:
        import nf
        nf.main()
    assert exit_e.value.code == 0
    sys.argv = sys_argv


def test_main_ls_no_notify():
    sys_argv = sys.argv
    sys.argv = ['nf', '-n', 'ls']
    with pytest.raises(SystemExit) as exit_e:
        import nf
        nf.main()
    assert exit_e.value.code == 0
    sys.argv = sys_argv


def test_main_no_module_dbus():
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


def test_main_no_module_shutil():
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


def test_main_module_shutil_cannot_get_terminal_size():
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


def test_main_module_dbus_error():
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


def test_main_module_all_mock():
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


def test_main_module_all_mock_save():
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


@pytest.mark.parametrize("backend", ['dbus', 'notify-send', 'termux-notification', 'win10toast', 'stdout'])
def test_main_module_all_mock_backend(backend):
    sys_argv = sys.argv
    sys.argv = ['nf', '--backend={}'.format(backend), 'ls']

    module_backup = {}
    modules = ['dbus', 'win10toast', 'subprocess']
    for module_name in modules:
        module_backup[module_name] = sys.modules[module_name] if module_name in sys.modules else None

        module_mock = mock.MagicMock()
        setattr(module_mock, '__spec__', module_mock)

        sys.modules[module_name] = module_mock

    with pytest.raises(SystemExit) as exit_e:
        import nf
        nf.main()
    # assert exit_e.value.code == 0  # there is a mock (subprocess), so check this is useless

    for module_name in modules:
        sys.modules[module_name] = module_backup[module_name]
    sys.argv = sys_argv

@pytest.mark.parametrize("backend", ['dbus', 'notify-send', 'termux-notification', 'win10toast', 'plyer', 'plyer_toast', 'stdout'])
def test_main_module_all_mock_bad_backend(backend):
    sys_argv = sys.argv
    sys.argv = ['nf', '--debug', '--backend={}'.format(backend), 'ls']

    module_backup = {}
    modules = ['dbus', 'win10toast', 'shutil', 'plyer']
    for module_name in modules:
        module_backup[module_name] = sys.modules[module_name] if module_name in sys.modules else None

        #module_mock = mock.MagicMock()
        #setattr(module_mock, '__spec__', module_mock)

        sys.modules[module_name] = None

    with pytest.raises(SystemExit) as exit_e:
        import nf
        nf.main()
    assert exit_e.value.code == 0

    for module_name in modules:
        sys.modules[module_name] = module_backup[module_name]
    sys.argv = sys_argv

@pytest.mark.slow
def test_readme_rst():
    import rstcheck
    with open('README.rst') as f:
        readme = f.read()
    errors = list(rstcheck.check(readme))

    assert errors == []
