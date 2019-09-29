#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Initialization module for solstice-tools-snowgenerator
"""

import os
import inspect

import sentry_sdk
sentry_sdk.init("https://32d16a6960cd413fad0a4be211e6972b@sentry.io/1764702")

from tpPyUtils import importer

from artellapipe.utils import resource, exceptions


class SnowGenerator(importer.Importer, object):
    def __init__(self):
        super(SnowGenerator, self).__init__(module_name='solstice.tools.snowgenerator')

    def get_module_path(self):
        """
        Returns path where tpNameIt module is stored
        :return: str
        """

        try:
            mod_dir = os.path.dirname(inspect.getframeinfo(inspect.currentframe()).filename)
        except Exception:
            try:
                mod_dir = os.path.dirname(__file__)
            except Exception:
                try:
                    import tpDccLib
                    mod_dir = tpDccLib.__path__[0]
                except Exception:
                    return None

        return mod_dir


def init(do_reload=False):
    """
    Initializes module
    """

    packages_order = []

    snowgenerator_importer = importer.init_importer(importer_class=SnowGenerator, do_reload=False)
    snowgenerator_importer.import_packages(order=packages_order, only_packages=False)
    if do_reload:
        snowgenerator_importer.reload_all()

    create_logger_directory()

    resources_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'resources')
    resource.ResourceManager.instance().register_resource(resources_path)


@exceptions.sentry_exception
def run(do_reload=False):
    """
    Run SnowGenerator Tool
    :param do_reload: bool
    :return: AssetsManager
    """

    init(do_reload=do_reload)
    from solstice.tools.snowgenerator import snowgenerator
    win = snowgenerator.run()
    return win


def create_logger_directory():
    """
    Creates artellapipe-gui logger directory
    """

    artellapipe_logger_dir = os.path.normpath(os.path.join(os.path.expanduser('~'), 'solstice', 'logs'))
    if not os.path.isdir(artellapipe_logger_dir):
        os.makedirs(artellapipe_logger_dir)


def get_logging_config():
    """
    Returns logging configuration file path
    :return: str
    """

    return os.path.normpath(os.path.join(os.path.dirname(__file__), '__logging__.ini'))


def get_logging_level():
    """
    Returns logging level to use
    :return: str
    """

    if os.environ.get('SOLSTICE_TOOLS_SNOWGENERATOR_LOG_LEVEL', None):
        return os.environ.get('SOLSTICE_TOOLS_SNOWGENERATOR_LOG_LEVEL')

    return os.environ.get('SOLSTICE_TOOLS_SNOWGENERATOR_LOG_LEVEL', 'WARNING')
