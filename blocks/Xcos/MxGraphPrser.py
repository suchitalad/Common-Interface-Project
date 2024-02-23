import xml.etree.ElementTree as ET


# Load the XML file
tree = ET.parse("/home/spoken/Common-Interface-Project/blocks/ex_test_1.xml")
root = tree.getroot()

# Define the namespace
namespace = {'': ''}
        
def get_block_elements(style):
    return root.findall(f".//mxCell[@style='{style}']")
    
def get_explicit_output_ports(block_id):
    explicit_output = f".//mxCell[@style='ExplicitOutputPort'][@ParentComponent='{block_id}']"
    return root.findall(explicit_output)
    
def get_next_block_name(block_id):
    parent_component = root.find(f".//mxCell[@id='{block_id}']") 
    if parent_component is not None: 
        return parent_component.get('style') 
    else:
        return None
        
def get_next_block_explicit_output_ports(block_id):
    next_blk_name = get_next_block_name(block_id) 
    if next_blk_name:
        next_blk = root.find(f".//mxCell[@id='{block_id}']")
        if next_blk:
            explicit_output_ports = next_blk.get('explicitOutputPorts')
            if explicit_output_ports and int(explicit_output_ports) > 0:
                return get_explicit_output_ports(next_blk.get('id'))
    return []
    
def print_source_target(source_vertex, target_vertex):
    print(f"Source: {source_vertex}, Target: {target_vertex}")

def find_block_by_target_value(target_vertex):
    parent_component = root.find(f".//mxCell[@id='{target_vertex}']")
    if parent_component is not None:
        target = parent_component.get('targetVertex')
        id = root.find(f".//mxCell[@id='{target}']")
        pid = id.get('ParentComponent')
        parent_components = root.find(f".//mxCell[@id='{pid}']")
        if parent_components is not None:
            blk_name = parent_components.get('style')
            print(blk_name, pid)
        # else:
        #     find_block_by_target_value(target_vertex)

def process_block_recursive(block_id, depth=0, processed_blocks=set()):
    if block_id in processed_blocks:
        return  # Stop processing if the block has already been processed
    processed_blocks.add(block_id)
    
    next_block_explicit_output_ports = get_next_block_explicit_output_ports(block_id)
    # print(next_block_explicit_output_ports) # Number of ports in block
    for port in next_block_explicit_output_ports:
        source_vertex = port.get('id') 
        edges = root.findall(f".//mxCell[@edge='1'][@sourceVertex='{source_vertex}']")
        for edge in edges:
            target_vertex = edge.get('targetVertex')
            print_source_target(source_vertex, target_vertex)
            next_block_id = root.find(f".//mxCell[@id='{target_vertex}']").get('ParentComponent')
            next_block_name = get_next_block_name(next_block_id)
            print(next_block_name, next_block_id)
            if next_block_name:
                process_block_recursive(next_block_id, depth + 1, processed_blocks)  # Pass the set of processed blocks
            else:
                find_block_by_target_value(target_vertex)

def process_blocks(style):
    blocks = get_block_elements(style)
    for block in blocks:
        block_id = block.get('id')
        print(f"{style} having explicitOutputPorts: {block.get('explicitOutputPorts')} and block ID: {block_id}")
        process_block_recursive(block_id)

process_blocks('STARTBLK')