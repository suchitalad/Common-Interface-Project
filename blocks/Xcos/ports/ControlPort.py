from common.AAAAAA import *


def ControlPort(outroot, attribid, parentattribid, ordering, geometry,
                value='', forSplitBlock=False,
                style=None):
    func_name = 'ControlPort'
    if style is None:
        style = func_name

    if forSplitBlock:
        outnode = addNode(outroot, func_name, connectable=0,
                          dataType='UNKNOW_TYPE', **{'id': attribid},
                          ordering=ordering, parent=parentattribid,
                          style=style, visible=0)
    else:
        outnode = addNode(outroot, func_name, **{'id': attribid},
                          parent=parentattribid, ordering=ordering,
                          initialState="-1.0",
                          style=style, value=value)

    return outnode


def addControlPortForSplit(outroot, splitBlock, sourceVertex, targetVertex,
                           sourceType, targetType, inputCount,
                           outputCount, nextAttrib, nextAttribForSplit, waypoints):
    inputCount += 1
    geometry = {}
    geometry['width'] = 8
    geometry['height'] = 8
    geometry['x'] = -8
    geometry['y'] = -4
    ControlPort(outroot, nextAttrib, splitBlock, inputCount, geometry,
                forSplitBlock=True)
    nextAttrib += 1
    nextAttribForSplit += 1
    return (inputCount, outputCount, nextAttrib, nextAttribForSplit)
