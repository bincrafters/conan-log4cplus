#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
from conans.errors import ConanInvalidConfiguration
import os


class Log4cplusConan(ConanFile):
    name = "log4cplus"
    version = "2.0.0"
    description = "simple to use C++ logging API, modelled after the Java log4j API"
    url = "https://github.com/bincrafters/conan-log4cplus"
    homepage = "https://github.com/log4cplus/log4cplus"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "BSD-2-Clause, Apache-2.0"
    topics = ("conan", "log4cplus", "logging", "log", "logging-library")
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    generators = 'cmake'
    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {
        'shared': [True, False],
        "fPIC": [True, False],
        "single_threaded": [True, False],
        "build_logging_server": [True, False],
        "with_iconv": [True, False],
        "working_locale": [True, False],
        "working_c_locale": [True, False],
        "decorated_name": [True, False],
        "qt4_debug_appender": [True, False],
        "qt5_debug_appender": [True, False]
    }
    default_options = {
        'shared': False,
        'fPIC': True,
        'single_threaded': False,
        'build_logging_server': False,
        'with_iconv': False,
        'working_locale': False,
        'working_c_locale': False,
        'decorated_name': False,
        'qt4_debug_appender': False,
        'qt5_debug_appender': False
    }
    short_paths = True
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def requirements(self):
        if self.options.with_iconv:
            self.requires.add('libiconv/1.15@bincrafters/stable')

    def config_options(self):
        if self.settings.compiler == 'Visual Studio':
            del self.options.fPIC

    def configure(self):
        if self.options.qt4_debug_appender:
            raise ConanInvalidConfiguration('Qt4 debug appender is not supported yet!')
        if self.options.qt5_debug_appender:
            raise ConanInvalidConfiguration('Qt5 debug appender is not supported yet!')

    def source(self):
        archive_name = self.name + "-" + self.version
        sha256 = "cd10e355a30ffe0710e3319a011925889ffd78d61d15217d477cb2890217dba2"
        tools.get("{}/releases/download/REL_{}/{}.zip".format(self.homepage, self.version.replace(".", "_"), archive_name), sha256=sha256)
        os.rename(archive_name, self._source_subfolder)

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions['LOG4CPLUS_BUILD_TESTING'] = False
        cmake.definitions['WITH_UNIT_TESTS'] = False
        cmake.definitions["LOG4CPLUS_ENABLE_DECORATED_LIBRARY_NAME"] = self.options.decorated_name
        cmake.definitions['LOG4CPLUS_QT4'] = self.options.qt4_debug_appender
        cmake.definitions['LOG4CPLUS_QT5'] = self.options.qt5_debug_appender
        cmake.definitions['LOG4CPLUS_SINGLE_THREADED'] = self.options.single_threaded
        cmake.definitions['LOG4CPLUS_BUILD_LOGGINGSERVER'] = self.options.build_logging_server
        cmake.definitions['WITH_ICONV'] = self.options.with_iconv
        cmake.definitions['LOG4CPLUS_WORKING_LOCALE'] = self.options.working_locale
        cmake.definitions['LOG4CPLUS_WORKING_C_LOCALE'] = self.options.working_c_locale
        cmake.configure(build_dir=self._build_subfolder)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Linux":
            self.cpp_info.libs.extend(["dl", "pthread"])

        if self.settings.compiler == "Visual Studio":
            self.cpp_info.libs.append('Ws2_32')
