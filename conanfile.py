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

    def package(self):
        include_dir = os.path.join(self.source_subfolder, "include")
        
        self.copy("*.h", dst="include", src=include_dir)
        self.copy("*.hxx", dst="include", src=include_dir)
        # self.copy("*.hxx", dst="include/boost", src=os.path.join(include_dir, "boost")
        # self.copy("*.h", dst="include/config", src="log4cplus-REL_1_2_0/include/config")
        # self.copy("*.h", dst="include/helpers", src="log4cplus-REL_1_2_0/include/helpers")
        # self.copy("*.h", dst="include/internal", src="log4cplus-REL_1_2_0/include/internal")
        # self.copy("*.h", dst="include/spi", src="log4cplus-REL_1_2_0/include/spi")
        # self.copy("*.h", dst="include/thread", src="log4cplus-REL_1_2_0/include/thread")
        # self.copy("*.h", dst="include/thread/impl", src="log4cplus-REL_1_2_0/include/thread/impl")
        # self.copy("*.hxx", dst="include/log4cplus/config", src="include/log4cplus/config")
        self.copy("*.a", dst="lib", src="src")

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
