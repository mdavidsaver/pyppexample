#!/usr/bin/env python

def getargs():
    import argparse
    from os.path import basename, splitext
    P = argparse.ArgumentParser()
    P.add_argument('output', help='output .cpp file')
    P.add_argument('input', nargs='+', help='input .h files')
    P.add_argument('--include','-I', action='append', default=[])
    P.add_argument('--name', help='module name')
    P.add_argument('--mangle', help='python file with callbacks to modify the output')
    P.add_argument('--chdir', help='Switch to this directory before generating')
    A = P.parse_args()
    if not A.name:
        A.name = splitext(basename(A.output))[0]
    return A

def main(args):
    from pyplusplus import module_builder
    from pyplusplus.module_builder import call_policies

    if args.chdir:
        from os import chdir
        chdir(args.chdir)

    builder = module_builder.module_builder_t(args.input,
                                              include_paths=args.include)

    if args.mangle:
        from runpy import runpy
        M = runpy(args.mangle)
        M['mangle'](builder)

        #eg. things a mangle might do
        #Cell = builder.class_('Cell')
        #Cell.member_function('getelem').call_policies = call_policies.return_internal_reference()
        # The Elem* pointer passed to setelem(P) is now "owned" by the Cell
        #Cell.member_function('setelem').call_policies = call_policies.with_custodian_and_ward(1,2)

        #Cell.var('elem').expost_value = False

    builder.build_code_creator(module_name=args.name)
    builder.write_module(args.output)

if __name__=='__main__':
    main(getargs())
