from common.AAAAAA import *


def CSCOPE(outroot, attribid, ordering, geometry, parameters, parent=1, style=None):
    func_name = 'CSCOPE'
    if style is None:
        style = func_name

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, parent,
                         func_name, 'cscope', 'C_OR_FORTRAN',
                         style, BLOCKTYPE_C,
                         dependsOnU='1')

    addExprsNode(outnode, TYPE_STRING, 10, parameters)
    addScilabDNode(outnode, AS_REAL_PARAM, width=4, realParts=[
        format_real_number(parameters[8]),
        format_real_number(parameters[4]),
        format_real_number(parameters[5]),
        format_real_number(parameters[6])])
    param = strarray(parameters)
    addPrecNode(outnode, TYPE_INTEGER, AS_INT_PARAM, 15, param)
    addObjNode(outnode, TYPE_ARRAY, CLASS_LIST, AS_OBJ_PARAM, parameters)
    array = ['0']
    addPrecisionNode(outnode, TYPE_INTEGER, AS_NBZERO, 1, array)
    addPrecisionNode(outnode, TYPE_INTEGER, AS_NMODE, 1, array)
    addTypeNode(outnode, TYPE_DOUBLE, AS_STATE, 0, [])
    addTypeNode(outnode, TYPE_DOUBLE, AS_DSTATE, 0, [])
    addObjNode(outnode, TYPE_ARRAY, CLASS_LIST, AS_ODSTATE, parameters)
    addObjNode(outnode, TYPE_ARRAY,
               CLASS_LIST, AS_EQUATIONS, parameters)
    addgeometryNode(outnode, GEOMETRY, geometry['height'],
                    geometry['width'], geometry['x'], geometry['y'])

    return outnode


def get_from_CSCOPE(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = 1 if int(float(parameters[8])) == 0 else 0
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)
