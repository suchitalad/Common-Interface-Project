def GENERAL_f(outroot, attribid, ordering, geometry, parameters):
    func_name = 'GENERAL_f'

    outnode = addNode(outroot, 'BasicBlock', **{'id': attribid},
                      interfaceFunctionName=func_name,
                      ordering=ordering,
                      parent=1,
                      dependsOnU=1,
                      blockType='z',
                      simulationFunctionName='zcross',
                      simulationFunctionType='TYPE_1',
                      style=func_name)

    node = addExprsNode(outnode, 'ScilabString', 2, parameters)

    return outnode
