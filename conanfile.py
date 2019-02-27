#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
from conans.errors import ConanException
import os


class Log4cplusConan(ConanFile):
    name = "log4cplus"
    version = "1.2.1"
    description = "simple to use C++ logging API, modelled after the Java log4j API"
    url = "https://github.com/bincrafters/conan-log4cplus"
    homepage = "https://downloads.sourceforge.net/project/log4cplus/log4cplus-stable"
    license = "BSD 2-clause, Apache-2.0"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    generators = 'cmake'
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"
    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False],
               "fPIC": [True, False],
               "single_threaded": [True, False],
               "build_logging_server": [True, False],
               "with_iconv": [True, False],
               "working_locale": [True, False],
               "working_c_locale": [True, False],
               "decorated_name": [True, False],
               "qt4_debug_appender": [True, False],
               "qt5_debug_appender": [True, False]}
    default_options = ('shared=False',
                       'fPIC=True',
                       "single_threaded=False",
                       "build_logging_server=False",
                       "with_iconv=False",
                       "working_locale=False",
                       "working_c_locale=False",
                       "decorated_name=False",
                       "qt4_debug_appender=False",
                       "qt5_debug_appender=False")
    short_paths = True

    def requirements(self):
        if self.options.with_iconv:
            self.requires.add('libiconv/1.15@bincrafters/stable')

    def config_options(self):
        if self.settings.compiler == 'Visual Studio':
            del self.options.fPIC

    def configure(self):
        if self.options.qt4_debug_appender:
            raise ConanException('Qt4 debug appender is not supported yet!')
        if self.options.qt5_debug_appender:
            raise ConanException('Qt5 debug appender is not supported yet!')

    def source(self):
        source_url = "https://downloads.sourceforge.net/project/log4cplus/log4cplus-stable"
        archive_name = self.name + "-" + self.version
        tools.get("{0}/{1}/{2}.zip".format(source_url, self.version, archive_name))
        os.rename(archive_name, self.source_subfolder)

    def build(self):
        cmake = CMake(self)
        if self.settings.compiler != 'Visual Studio':
            cmake.definitions['CMAKE_POSITION_INDEPENDENT_CODE'] = self.options.fPIC

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

        if self.settings.os == 'Android':
            cmake.definitions['CONAN_CMAKE_FIND_ROOT_PATH_MODE_PROGRAM'] = 'ONLY'
            cmake.definitions['CONAN_CMAKE_FIND_ROOT_PATH_MODE_LIBRARY'] = 'ONLY'
            cmake.definitions['CONAN_CMAKE_FIND_ROOT_PATH_MODE_INCLUDE'] = 'ONLY'

        cmake.configure(build_dir=self.build_subfolder)
        cmake.build()
        cmake.install()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self.source_subfolder)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Linux":
            self.cpp_info.libs.extend(["dl", "pthread"])

        if self.settings.compiler == "Visual Studio":
            self.cpp_info.libs.append('Ws2_32')
