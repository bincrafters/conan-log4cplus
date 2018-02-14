#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class Log4cplusConan(ConanFile):
    name = "log4cplus"
    version = "1.2.0"
    description = "simple to use C++ logging API, modelled after the Java log4j API"
    url = "https://github.com/bincrafters/conan-log4cplus"
    license = "BSD 2-clause, Apache-2.0"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    generators = 'cmake'
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"
    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = 'shared=False'

    def source(self):
        source_url = "https://github.com/log4cplus/log4cplus"
        archive_name = "REL_{}".format(self.version.replace(".","_"))
        tools.get("{0}/archive/{1}.tar.gz".format(source_url, archive_name))
        extracted_dir = self.name + "-" + archive_name
        os.rename(extracted_dir, self.source_subfolder)

    def build(self):
        cmake = CMake(self)
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
