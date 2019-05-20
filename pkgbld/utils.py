"""
Package-Builder utility functions.
"""
# CODING-STYLE CHECKS:
# pycodestyle utils.py
# pylint --disable=locally-disabled utils.py

import subprocess
import re
import platform
import sys


def os_call(cmd, ignore_error=False):
    """
    Execute specified cmd string in operating-system subprocess.

    Returns: stdout from command.
    """
    assert isinstance(cmd, str)
    try:
        proc = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE)
    except subprocess.CalledProcessError as err:
        if not ignore_error:
            msg = ('non-zero return code {} generated by '
                   'command:\n{}\n>output: {}')
            raise OSError(msg.format(err.returncode, cmd, err.output))
    return proc.stdout


def file_revision(filename, pattern, replacement):
    """
    Replace repattern with replacement on each line of file using re.sub().
    """
    lines = list()
    with open(filename, 'r') as file_:
        for line in file_.readlines():
            lines.append(re.sub(pattern, replacement, line))
    with open(filename, 'w') as file_:
        for line in lines:
            file_.write(line)


def conda_platform_name():
    """
    Return conda name of local operating-system platform.
    """
    system_ = platform.system()
    if system_ == 'Darwin':
        conda_name = 'osx'
    elif system_ == 'Linux':
        conda_name = 'linux'
    elif system_ == 'Windows':
        conda_name = 'win'
    else:
        msg = 'OS=<{}> is not Windows, Linux, or Darwin(OSX).'
        raise OSError(msg.format(system_))
    # For the following bit-size code, see this link:
    # https://docs.python.org/3.6/library/platform.html#platform.architecture
    is_64bit = sys.maxsize > 2 ** 32
    n_bits = '64' if is_64bit else '32'
    return conda_name + '-' + n_bits
