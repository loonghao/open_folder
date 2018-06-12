# -*- coding: utf-8 -*-
"""
module author: Long Hao <hoolongvfx@gmail.com>
"""

# Import built-in modules
import os
import subprocess
import sys

# Import Houdini modules
import hou


def start(file_path):
    """
    file_path (str): Absolute path.

    Examples:
        >>>start("c:/test")

    """
    cmd = "cmd /c start "
    if sys.platform == "darwin":
        cmd = "open "
    elif sys.platform == "linux2":
        cmd = "xdg-open "
    else:
        file_path = file_path.replace('/', '\\')
        if os.path.isfile(file_path):
            os.startfile(file_path)
            return
    command = (cmd + file_path)
    subprocess.call(command)


def run():
    node_types = {'default': 'file',
                  'rop_geometry': 'sopoutput',
                  'rop_alembic': 'filename',
                  'ifd': 'vm_picture',
                  'alembic': 'fileName',
                  }
    nodes = hou.selectedNodes()
    if nodes:
        hou_node = hou.node(nodes[0].path())
        type_ = nodes[0].type().name()
        if type_ not in node_types:
            parm_ = node_types['default']
        else:
            parm_ = node_types[type_]
        hou_parm = hou_node.parm(parm_)
        if hou_parm:
            hou_parm.lock(False)
            file_path = hou_parm.eval()
            if os.path.isdir(file_path):
                file_dir = file_path
            else:
                file_dir = os.path.dirname(file_path)
            file_dir = os.path.normcase(file_dir)
            if os.path.exists(file_dir):
                start(file_dir)
            else:
                print 'not find the folder'
    else:
        hou.ui.displayMessage('Not selected Nodes', buttons=('OK',),
                              title="Houdini")
