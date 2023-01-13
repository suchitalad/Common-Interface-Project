def TOWS_c(outroot, attribid, ordering, geometry, parameters):
    func_name = 'TOWS_c'

    para3 = int(parameters[2])

    b_type = ''
    if para3 == 1:
        b_type = 'x'
    else:
        b_type = 'd'

    outnode = addOutNode(outroot, BLOCK_BASIC,
                         attribid, ordering, 1,
                         func_name, 'tows_c', 'C_OR_FORTRAN',
                         func_name, b_type)

    addExprsNode(outnode, TYPE_STRING, 3, parameters)

    return outnode


def get_from_TOWS_c(cell):
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