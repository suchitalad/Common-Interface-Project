def CURV_f(outroot, attribid, ordering, geometry, parameters):
    func_name = 'CURV_f'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'intplt', 'DEFAULT',
                         func_name, 'c',
                         dependsOnT=1)

    addExprsNode(outnode, TYPE_DOUBLE, 0, parameters)

    return outnode


def get_from_CURV_f(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_DOUBLE)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)