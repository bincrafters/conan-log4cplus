#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools


class Log4cplusConan(ConanFile):
    name = "log4cplus"
    version = "1.2.0"
    license = "BSD 2-clause, Apache-2.0"
    url = "https://github.com/bincrafters/conan-log4cplus"
    generators = 'cmake'
    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = 'shared=False'

    def source(self):
        base_url = "https://github.com/log4cplus/log4cplus/archive"
        zip_name = "REL_1_2_0.zip"
        tools.download("%s/%s" % (base_url, zip_name), zip_name)
        tools.unzip(zip_name)

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_dir='log4cplus-REL_1_2_0', build_dir='./')
        cmake.build()

    def package(self):
        self.copy("*.h", dst="include", src="log4cplus-REL_1_2_0/include")
        self.copy("*.hxx", dst="include", src="log4cplus-REL_1_2_0/include")
        self.copy("*.hxx", dst="include/boost", src="log4cplus-REL_1_2_0/include/boost")
        self.copy("*.h", dst="include/config", src="log4cplus-REL_1_2_0/include/config")
        self.copy("*.h", dst="include/helpers", src="log4cplus-REL_1_2_0/include/helpers")
        self.copy("*.h", dst="include/internal", src="log4cplus-REL_1_2_0/include/internal")
        self.copy("*.h", dst="include/spi", src="log4cplus-REL_1_2_0/include/spi")
        self.copy("*.h", dst="include/thread", src="log4cplus-REL_1_2_0/include/thread")
        self.copy("*.h", dst="include/thread/impl", src="log4cplus-REL_1_2_0/include/thread/impl")
        self.copy("*.hxx", dst="include/log4cplus/config", src="include/log4cplus/config")
        self.copy(pattern="*.a", dst="lib", src="src")
