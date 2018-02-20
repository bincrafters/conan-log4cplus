#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class Log4cplusConan(ConanFile):
    name = "log4cplus"
    version = "1.2.1"
    description = "simple to use C++ logging API, modelled after the Java log4j API"
    url = "https://github.com/bincrafters/conan-log4cplus"
    license = "BSD 2-clause, Apache-2.0"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    generators = 'cmake'
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"
    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], "fPIC": [True, False]}
    default_options = 'shared=False', 'fPIC=True'
    short_paths = True

    def config(self):
        if self.settings.compiler == 'Visual Studio':
            del self.options.fPIC

    def source(self):
        source_url = "https://downloads.sourceforge.net/project/log4cplus/log4cplus-stable"
        archive_name = self.name + "-" + self.version
        tools.get("{0}/1.2.1/{1}.zip".format(source_url, archive_name))
        os.rename(archive_name, self.source_subfolder)
        
    def build(self):
        cmake = CMake(self)
        if self.settings.compiler != 'Visual Studio':
            cmake.definitions['CMAKE_POSITION_INDEPENDENT_CODE'] = self.options.fPIC
        cmake.configure(build_dir=self.build_subfolder)
        cmake.definitions['LOG4CPLUS_BUILD_TESTING'] = 'False'
        cmake.definitions['WITH_UNIT_TESTS'] = 'False'
        cmake.definitions["LOG4CPLUS_ENABLE_DECORATED_LIBRARY_NAME"] = 'False'
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
