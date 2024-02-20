import xml.etree.ElementTree as ET


# Load the XML file
tree = ET.parse("/home/spoken/Common-Interface-Project/blocks/ex_test_1.xml")
root = tree.getroot()

# Define the namespace
# namespace = {'mx': 'http://www.w3.org/2001/XMLSchema-instance'}
namespace = {'': ''}

# Find all elements with 'style' attribute containing 'STARTBLK'
startblk_elements = root.findall(".//mxCell[@style='STARTBLK']", namespace)
# print(startblk_elements)


# Print the IDs of the elements
for element in startblk_elements:
    # print("Startblk found with ID:", element.get('explicitOutputPorts'))
    explicit_output_port = root.find('.//mxCell[@style="ExplicitOutputPort"]')
    
    if explicit_output_port.get('ParentComponent') == element.get('id'):
        sourceVertex = explicit_output_port.get('id')
        edge = root.find('.//mxCell[@edge="1"]')
        
        if sourceVertex == edge.get('sourceVertex'):
            targetVertex = edge.get('targetVertex')
            id = root.find(f".//mxCell[@id='{targetVertex}']")
            pid = id.get('ParentComponent')
            parent_component = root.find(f".//mxCell[@id='{pid}']")
            blk_name = parent_component.get('style')
            print(blk_name, pid)
            explicit_output = root.findall('.//mxCell[@style="ExplicitOutputPort"]')

            for elem in explicit_output:
                if elem.get('ParentComponent') == pid:
                    sourceVertex1 = elem.get('id')
                    print(sourceVertex1)
                    edge = root.findall('.//mxCell[@edge="1"]')
                    
                    for ele in edge:
                        if sourceVertex1 == ele.get('sourceVertex'):
                            targetVertex1 = ele.get('targetVertex')
                            id = root.find(f".//mxCell[@id='{targetVertex1}']")
                            pid = id.get('ParentComponent')
                            parent_component = root.find(f".//mxCell[@id='{pid}']")
                            blk_name = parent_component.get('style')
                            print(blk_name, pid)


        

#                 print("Style of parent component (ID: %s): %s" % (parent_component_id, parent_component_style))
#         else:
#             print("ExplicitInputPort with ID '%s' not found." % explicit_input_port_id)
#     else:
#         print("No explicitInputPort found for the component with ID '60'.")
# else:
#     print("No component found with ID '4'.")  


# def generate_python_output(input_file):
#     tree = ET.parse(input_file)
#     root = tree.getroot()
    

#     output = ""

#     for mxCell in root.iter('mxCell'):
#         style = mxCell.attrib.get('style', None)
        
#         p000_value = mxCell.find(".//Object[@p000_value]")
#         p001_value = mxCell.find(".//Object[@p001_value]")
        
#         if style is not None and style == 'ASSIGNMENT':
#             if p000_value is not None and p001_value is not None:
#                 value_1 = p000_value.attrib.get('p000_value', '')
#                 value_2 = p001_value.attrib.get('p001_value', '')
#                 output += f"{value_1} = {value_2}\n"

#         if style is not None and style == 'IF':
#             if p000_value is not None: 
#                 value_1 = p000_value.attrib.get('p000_value', '')      
#                 output += f"if {value_1}:\n"
#                 # output += f"    True\n"  # Print "True"
#                 # print(value_1)
#                 if value_1:  # Check if value_1 evaluates to True
#                     output += f" {value_1}    # Code in if \n"  # Execute code inside if block
#                 else:
#                     output += f"check the value # Code outside if block \n"  # Execute code outside if block

#         if style is not None and style == 'ELIF':
#             if p000_value is not None: 
#                 value_1 = p000_value.attrib.get('p000_value', '')      
#                 output += f"elif {value_1}:\n"
                
#                 if value_1:  # Check if value_1 evaluates to True
#                     output += f" {value_1}    # Code in if \n"  # Execute code inside if block
#                 else:
#                     output += f"check the value # Code outside if block \n"  # Execute code outside if block

#         if style is not None and style == 'FOR':
#             if p000_value is not None: 
#                 value_1 = p000_value.attrib.get('p000_value', '')
#                 value_2 = p001_value.attrib.get('p001_value', '')      
#                 output += f"for {value_1} in {value_2}:\n"
#                 my_range = range(10)
#                 integer_10 = list(my_range)[-1]
#                 for value_1 in range(integer_10):
#                     output += f" {value_1} \n"
                
#         if style is not None and style == 'WHILE':
#             if p000_value is not None:
#                 value_1 = p000_value.attrib.get('p000_value', '')
#                 output += f"while {value_1}:\n"
#                 output += f"    # Code \n"

#     return output

# input_file = "/home/spoken/Common-Interface-Project/blocks/ex_test_1.xml"
# output = generate_python_output(input_file)

# with open("/home/spoken/Common-Interface-Project/blocks/output.py", "w") as f:
#     f.write(output)

# print("Python file 'output.py' generated successfully.")
