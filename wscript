#! /usr/bin/env python
# encoding: utf-8

APPNAME = 'yaml-cpp'
VERSION = '3.0.0'

import waflib.extras.wurf_options


def options(opt):

    opt.load('wurf_common_tools')


def resolve(ctx):

    import waflib.extras.wurf_dependency_resolve as resolve

    ctx.load('wurf_common_tools')

    ctx.add_dependency(resolve.ResolveVersion(
        name='waf-tools',
        git_repository='github.com/steinwurf/waf-tools.git',
        major=3))

    ctx.add_dependency(resolve.ResolveVersion(
        name='boost',
        git_repository='github.com/steinwurf/boost.git',
        major=2))


def configure(conf):

    conf.load("wurf_common_tools")


def build(bld):

    bld.load("wurf_common_tools")

    bld.env.append_unique(
        'DEFINES_STEINWURF_VERSION',
        'STEINWURF_YAML_CPP_VERSION="{}"'.format(VERSION))

    bld.stlib(features='cxx',
              source=bld.path.ant_glob('src/*.cpp'),
              includes=['src', 'include'],
              export_includes=['include'],
              use=['boost_includes'],
              target=APPNAME,
              lib='dl pthread')
