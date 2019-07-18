#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class TestPackageConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    options = {"unicode": [True, False]}
    default_options = ("unicode=False")

    def build(self):
        cmake = CMake(self)
        cmake.definitions['WITH_ICONV'] = self.options['log4cplus'].with_iconv
        cmake.definitions['UNICODE'] = self.options['log4cplus'].unicode
        cmake.configure()
        cmake.build()

    def test(self):
        if not tools.cross_building(self.settings):
            bin_path = os.path.join("bin", "test_package")
            self.run(bin_path, run_environment=True)
