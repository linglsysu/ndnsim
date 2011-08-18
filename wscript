## -*- Mode: python; py-indent-offset: 4; indent-tabs-mode: nil; coding: utf-8; -*-

import os
import Logs
import Utils
import Options

def set_options(opt):
    opt.tool_options('boost')

def configure(conf):
    conf.check_tool('boost')
    conf.env['BOOST'] = conf.check_boost(lib = '', # need only base
                                         min_version='1.40.0' )
    if not conf.env['BOOST']:
        conf.report_optional_feature("ndn-abstract", "NDN abstraction", False,
                                     "Required boost libraries not found")
        conf.env['ENABLE_NDN_ABSTRACT']=False;
        return
    
    conf.env['ENABLE_NDN_ABSTRACT']=True;


def build(bld):
    module = bld.create_ns3_module ('NDNabstraction', ['applications', 'core', 'network', 'point-to-point','topology-read','visualizer'])

    tests = bld.create_ns3_module_test_library('NDNabstraction')
    headers = bld.new_task_gen('ns3header')
    headers.module = 'NDNabstraction'

    if not bld.env['ENABLE_NDN_ABSTRACT']:
        return
   
    module.find_sources_in_dirs (['model', 'apps', 'helper'],[],['.cc']);
    tests.find_sources_in_dirs( ['test'], [], ['.cc'] );
    headers.find_sources_in_dirs( ['model', 'apps', 'helper'], [], ['.h'] );


    for path in ["examples"]:
        anode = bld.path.find_dir (path)
        if not anode or not anode.is_child_of(bld.srcnode):
            raise Utils.WscriptError("Unable to use '%s' - either because \
            it's not a relative path"", or it's not child of \
            '%s'."%(name,bld.srcnode))
        bld.rescan(anode)
        for filename in bld.cache_dir_contents[anode.id]:
            if filename.startswith('.') or not filename.endswith(".cc"):
                continue
            name = filename[:-len(".cc")]
            obj = bld.create_ns3_program(name, ['NDNabstraction'])
            obj.path = obj.path.find_dir (path)
            obj.source = filename
            obj.target = name
            obj.name = obj.target

    if bld.env['ENABLE_OPENSSL']:
        module.uselib = 'OPENSSL'

    if bld.env['ENABLE_EXAMPLES']:
        bld.add_subdirs('examples')

    bld.ns3_python_bindings()
    