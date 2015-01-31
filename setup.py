#!/usr/bin/env python

import sys
from os import getcwd, listdir
from os.path import abspath, join

from distutils.core import setup, Distribution, Extension, Command, DistutilsSetupError
from distutils.command import build, build_ext, clean

boost_python='boost_python-mt-py%s%s'%(sys.version_info.major,sys.version_info.minor)

class GenPyPP(Command):
    """run gen.py to create py++ wrappers
    """
    user_options = []

    def initialize_options(self):
        self.gccxml  = 'gccxml'
        self.modules = None
        self.build_temp = None

    def finalize_options(self):
        self.modules = self.distribution.x_modules or {}

        self.set_undefined_options('build',
            ('build_temp', 'build_temp'),
        )

        self.build_temp = abspath(self.build_temp)

    def run(self):
        from distutils.dir_util import remove_tree
        srcdir = getcwd()

        for mname, opts in self.modules.items():
            # run gen.py 
            mtemp = join(self.build_temp, mname)
            self.mkpath(mtemp)

            # Note: we don't use sys.executable here because
            # debian doesn't provide the code generator for py3 (don't know why).
            # However, the generated code will build against py3 if boost::python supports it
            cmd = ['./gen.py', '--name', mname, '--chdir', mtemp, '-I', srcdir]
            if 'mangle' in opts:
                cmd.extend(['--mangle',opts['mangle']])
            cmd.append(mname+'_gen.cpp')
            cmd.extend(opts['headers'])
            self.spawn(cmd)

            # copy out result
            self.copy_file(join(mtemp,mname+'_gen.cpp'),
                           self.build_temp)
            # also any generated headers
            for F in listdir(mtemp):
                if F.endswith('.pypp.hpp'):
                    self.copy_file(join(mtemp,F), self.build_temp)

            remove_tree(mtemp)

class BuildExtGen(build_ext.build_ext):
    """find and fixup paths of generated files.
    """
    def initialize_options(self):
        build_ext.build_ext.initialize_options(self)
        self.modules = None

    def finalize_options(self):
        build_ext.build_ext.finalize_options(self)
        self.modules = self.distribution.x_modules or {}
        # find generated header files
        self.include_dirs.append(self.build_temp)
        # TODO: why is this needed to find non-generated headers?
        self.include_dirs.append(getcwd())

    def swig_sources(self, srcs, ext):
        """Abuse swig extension point to fix-up our generated source locations
        """
        srcs = build_ext.build_ext.swig_sources(self, srcs, ext)
        newsrcs = []
        for src in srcs:
            if src.endswith('_gen.cpp'):
                newsrcs.append(join(self.build_temp, src))
            else:
                newsrcs.append(src)
        return newsrcs

# allow setup(x_modules={})
Distribution.x_modules = None

# Insert sub-command before build_ext
build.build.sub_commands.insert(0, ('build_pypp', lambda cmd:True))

setup(
  name='bppwrap',
  description='Example of using py++ to generate Boost python boilerplate',
  x_modules={
    'mylib':{'headers':['mylib.h']},
  },
  ext_modules=[
    Extension('mylib',
      ['mylib_gen.cpp', 'mylib_extra.cpp'],
      libraries=[boost_python],
    ),
  ],

  cmdclass={
    'build_pypp':GenPyPP,
    'build_ext':BuildExtGen,
  },
)
