def MATDIV(outroot, attribid, ordering, geometry, parameters):
    func_name = 'MATDIV'

    data_type = ['', 'mat_div', 'matz_div']

    simulation_func_name = data_type[int(parameters[0])]

    outnode = addNode(outroot, 'BasicBlock', **{'id': attribid},
                      parent=1,
                      interfaceFunctionName=func_name,
                      blockType='c',
                      dependsOnU=1,
                      ordering=ordering,
                      simulationFunctionName=simulation_func_name,
                      simulationFunctionType='C_OR_FORTRAN',
                      style=func_name)

    node = addExprsNode(outnode, 'ScilabString', 1, parameters)

    return outnode
