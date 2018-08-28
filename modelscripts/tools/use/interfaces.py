
# TODO:3 restore the ability to call use
#   this could be
#   1. for the user interface (drawing diagrams, OCL queries)
#   2. for the CLI (OCL queries)
#   3. as a compiler (not useful with new syntax)
#  The code below should be useful
#
        # def processUseCommand(command, sources):
        #
        #     def _useInterface(interface, files):
        #         terminal_cmd = 'gnome-terminal -e "%s"'
        #         if interface=='gui':
        #             use_cmd='use -nr %s' % ' '.join(files)
        #             full_cmd=terminal_cmd % use_cmd
        #         elif interface=='cli':
        #             use_cmd='use -nogui -nr %s' % ' '.join(files)
        #             full_cmd=terminal_cmd % use_cmd
        #         elif interface=='c':
        #             if len(files)==0:
        #                 full_cmd='use -V'
        #             elif len(files)==1: # means use
        #                 full_cmd='use -c %s' % files[0]
        #             elif len(files)==2: # means use soil
        #                 full_cmd='use -qv %s %s' % (files[0], files[1])
        #             else:
        #                 assert False
        #         else:
        #             raise NotImplementedError('"%s" invalid USE interface')
        #         print('mdc: %s' % full_cmd)
        #         os.system(full_cmd)
        #
        #     def _getSourcesForUSE(sources):
        #         #type: (List[Text]) -> List[Text]
        #         def _toUse(files, originalExtensions, useExtension):
        #             return [Environment.getWorkerFileName(
        #                         replaceExtension(f, useExtension))
        #                     for f in sources
        #                     if extension(f) in originalExtensions]
        #         uses=_toUse(sources, ['.cls'], '.use')
        #         soils=_toUse(sources, ['.obs','.scs'], '.soil')
        #
        #         (nu,ns)=(len(uses), len(soils))
        #         if len(sources)>len(uses)+len(soils):
        #             raise ValueError('ERROR: USE can only process .cls/.obs/.scs sources')
        #         if (nu,ns)==(0,0):
        #             return []
        #         elif (nu,ns)==(1,0):
        #             return uses
        #         elif (nu,ns)==(1,1):
        #             # order matter
        #             return uses+soils
        #         elif (nu,ns)==(0,1):
        #             raise ValueError('ERROR: .cls source is missing')
        #         else:
        #             raise ValueError('ERROR: too many .cls/.obs/.scs sources for USE')
        #
        #
        #     if command=='version':
        #         print('USE OCL version %s -- %s' % (
        #             USEEngine.useVersion(),
        #             'Copyright (C) 1999-2015 University of Bremen'))
        #     elif command in ['c', 'cli', 'gui']:
        #         files_for_use=_getSourcesForUSE(sources)
        #         _useInterface(
        #             interface=command,
        #             files=files_for_use
        #         )
