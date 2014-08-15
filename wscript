#! /usr/bin/env python
# encoding: utf-8

APPNAME = 'yaml-cpp'
VERSION = '1.0.1'


def recurse_helper(ctx, name):
    if not ctx.has_dependency_path(name):
        ctx.fatal('Load a tool to find %s as system dependency' % name)
    else:
        p = ctx.dependency_path(name)
        ctx.recurse([p])


def options(opt):

    import waflib.extras.wurf_dependency_bundle as bundle
    import waflib.extras.wurf_dependency_resolve as resolve

    bundle.add_dependency(opt, resolve.ResolveGitMajorVersion(
        name='boost',
        git_repository='github.com/steinwurf/external-boost-light.git',
        major_version=1))

    bundle.add_dependency(opt, resolve.ResolveGitMajorVersion(
        name='waf-tools',
        git_repository='github.com/steinwurf/external-waf-tools.git',
        major_version=2))

    opt.load('wurf_configure_output')
    opt.load('wurf_dependency_bundle')
    opt.load('wurf_dependency_resolve')
    opt.load('wurf_tools')


def configure(conf):

    if conf.is_toplevel():

        conf.load('wurf_dependency_bundle')
        conf.load('wurf_tools')

        conf.load_external_tool('install_path', 'wurf_install_path')
        conf.load_external_tool('mkspec', 'wurf_cxx_mkspec_tool')
        conf.load_external_tool('project_gen', 'wurf_project_generator')
        conf.load_external_tool('runners', 'wurf_runner')

        recurse_helper(conf, 'boost')


def build(bld):

    if bld.is_toplevel():

        bld.load('wurf_dependency_bundle')

        recurse_helper(bld, 'boost')

    bld.stlib(features='cxx',
              source=bld.path.ant_glob('src/*.cpp'),
              includes=['src', 'include'],
              export_includes=['include'],
              use=['boost_includes'],
              target=APPNAME,
              lib='dl pthread')
