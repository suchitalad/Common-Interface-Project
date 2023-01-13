def INTEGRAL_f(outroot, attribid, ordering, geometry, parameters):
    func_name = 'INTEGRAL_f'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'integr', 'DEFAULT',
                         func_name, 'c',
                         dependsOnT=1)

    addExprsNode(outnode, TYPE_STRING, 1, parameters)

    return outnode


def get_from_INTEGRAL_f(cell):
    parameters = getParametersFromExprsNode(cell, TYPE_STRING)

    display_parameter = ''

    eiv = ''
    iiv = ''
    con = ''
    eov = ''
    iov = ''
    com = ''

    ports = [eiv, iiv, con, eov, iov, com]

    return (parameters, display_parameter, ports)