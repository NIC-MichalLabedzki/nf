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
    for module_name in ['dbus', 'shutil']:
        module_backup[module_name] = sys.modules[module_name] if module_name in sys.modules else None

        module_mock = mock.MagicMock()
        setattr(module_mock, '__spec__', module_mock)

        sys.modules[module_name] = module_mock

    with pytest.raises(SystemExit) as exit_e:
        import nf
        nf.main()
    assert exit_e.value.code == 0

    for module_name in ['dbus', 'shutil']:
        sys.modules[module_name] = module_backup[module_name]
    sys.argv = sys_argv

@pytest.mark.slow
def test_readme_rst():
    import rstcheck
    with open('README.rst') as f:
        readme = f.read()
    errors = list(rstcheck.check(readme))

    assert errors == []
