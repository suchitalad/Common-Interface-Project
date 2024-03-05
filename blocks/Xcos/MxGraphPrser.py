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
            return (blk_name, pid)
        else:
            pass
            # find_block_by_target_value(target_vertex)
            
class PythonBlock:
    def __init__(self, block_id, block_type, level=0):
        self.id = block_id
        self.type = block_type
        self.level = level
        self.else_inner_block = None
        self.if_inner_block = None
        self.if_node = False
        self.next_block = None

    def add_block(self, block_id, block_type, level):
        if self.type == "IF":
            print("EQUAL TO IF\n",level)
            if self.if_node is True:
                print("TRUE NODE")
                if self.if_inner_block is None:
                    self.if_inner_block = PythonBlock(block_id, block_type, level + 1) #create new
                    print("TRUE INNER NODE:",self.if_inner_block)
                    return self.if_inner_block
                else:
                    return self.if_inner_block.add_block(block_id, block_type, level + 1) # add to existing
                    print("FALSE INNER NODE:",self.if_inner_block)
                    
            else:
                print("FALSE NODE",self.else_inner_block,block_id, block_type, level)
                if self.else_inner_block is None:
                    self.else_inner_block = PythonBlock(block_id, block_type, level+1) # 7, IF, 1
                    print("true inner node",self.else_inner_block)
                    return self.else_inner_block
                else:
                    return self.else_inner_block.add_block(block_id, block_type, level + 1)
                    print("false inner node",self.else_inner_block)
        else:
            print("OTHER BLOCK TYPE\n",self.next_block)
            if self.next_block is None:
                self.next_block = PythonBlock(block_id, block_type, level)
                print("NXT:",self.next_block)
                return self.next_block
            else:
                return self.next_block.add_block(block_id, block_type, level)
    
    def __str__(self):
        print(self.id, self.type, self.level)
        s = str(self.id) + " " + self.type + " " + str(self.level) + "\n"
        if self.if_inner_block is not None:
            s += str(self.if_inner_block)
        if self.else_inner_block is not None:
            s += str(self.else_inner_block)
        if self.next_block is not None:
            next_block_str = str(self.next_block)
            if next_block_str is not None:
                s += next_block_str
        return s
        
    def switch(self):
        self.if_node = True

# processed_blocks = set()
block_processed_order = []
if_encountered = False
previous_if_id = None

def process_block_recursive(block, depth=0): #2, startblk, 0
    global if_encountered, previous_if_id
    print("ORDER:",block_processed_order,if_encountered)

    # Check if the current block is encountered before the previously encountered "IF" statement
    if previous_if_id and block.id in block_processed_order and block_processed_order.index(block.id) < block_processed_order.index(previous_if_id):
        # print(f"Alert: Block {block.id} encountered before the previously encountered IF statement!")
        raise ValueError(f"Invalid connection!!!")
        return

    # Check if the current block is processed after encountering an "IF" statement
    if if_encountered:
        if block.id in block_processed_order:
            if block.type == 'IF':
                # print(f"Alert: Block {block.id} encountered before IF statement!!")
                raise ValueError(f"Invalid connection!!!")
            else:
                print(f"Alert: Block {block.id} encountered again after IF statement!")
                block_processed_order.remove(block.id)
                second_node = True
                # raise ValueError(f"Block {block.id} encountered again after IF statement!")
                    
    else:
        if block.id in block_processed_order:
            # print(f"Alert: Block {block.id} encountered before IF statement!")
            raise ValueError(f"Invalid connection!!!")
            
    block_processed_order.append(block.id)

    if block.type == "IF":
        if_encountered = True
        previous_if_id = block.id

    print("BLK:\n", block.id, block.type, block.level) # 7, IF , 1

    next_block_explicit_output_ports = get_next_block_explicit_output_ports(block.id)
    print(next_block_explicit_output_ports)
    second_node = False
    for port in next_block_explicit_output_ports:
        source_vertex = port.get('id')
        edges = root.findall(f".//mxCell[@edge='1'][@sourceVertex='{source_vertex}']")
        
        for edge in edges:
            if second_node == True:
                print("This is second_node")
                block.switch()
            target_vertex = edge.get('targetVertex')
            print(f"Source: {source_vertex}, Target: {target_vertex}")
            next_block_id = root.find(f".//mxCell[@id='{target_vertex}']").get('ParentComponent')
            next_block_name = get_next_block_name(next_block_id)
            print(next_block_name, next_block_id) 

            if next_block_id:
                print("IF TRUE")
            else:
                blocks = find_block_by_target_value(target_vertex)
                print("AAA:", blocks)
                next_block_id = blocks[1]
                next_block_name = blocks[0]
                # if isinstance(blocks, tuple) and len(blocks) == 2:
                #     block_name, block_id = blocks
                #     # if block.id in PythonBlock:
                #     #     if block_name in ["WHILE", "FOR"]:
                #     #         print("in if")
                #     #         pass
                #     #     else:
                #     #         print("else")
                #     #         raise ValueError(f"Block {block_name} has already been processed.")
                #     # else:
                #     #     print("PROCESSED:", PythonBlock)
                #     #     next_block = PythonBlock(block_id, block_name)
                #     #     process_block_recursive(next_block, depth + 1)
                # else:
                #     process_block_recursive(blocks, depth)
                    # print("Unexpected format for block:", block)
            
            new_block = block.add_block(next_block_id, next_block_name, block.level)  # Add block to current block 4 INPUT 0
            print("TEST",new_block.level)
            # processed_blocks.add(new_block.id)
            # print("PROCESSED:",processed_blocks)
            process_block_recursive(new_block)
            second_node = True
    if block.type == "IF":
        if_encountered = False
        previous_if_id = None
            # print("PROCESSED:",processed_blocks)
    return 
    

def process_blocks(style):
    # Define the styles to process
    styles_to_process = ["STARTBLK", "STOPBLK"]

    # Count occurrences of each block style
    style_counts = {style: 0 for style in styles_to_process}

    for style_to_process in styles_to_process:
        blocks = get_block_elements(style_to_process)

        for block in blocks:
            block_id = block.get('id')
            block_style = block.get('style')
            if block_style in style_counts:
                style_counts[block_style] += 1

    # Check for multiple occurrences of STARTBLK or STOPBLK styles
    for style, count in style_counts.items():
        if count > 1:
            raise ValueError(f"Multiple occurrences of {style} style found.")

    # Process the blocks
    for style_to_process in styles_to_process:
        blocks = get_block_elements(style_to_process)
        
        for block in blocks:
            block_id = block.get('id')
            # print(f"{style_to_process} having explicitOutputPorts: {block.get('explicitOutputPorts')} and block ID: {block_id}")
            start_block = PythonBlock(block_id, style_to_process)
            # processed_blocks.add(block_id)
            process_block_recursive(start_block)
            print(start_block)

try:
    process_blocks("STARTBLK")
except ValueError as e:
    print(e)

# def process_block_recursive(block_id, processed_blocks, processed_blocks_after_if, depth=0):
#     next_block_name = get_next_block_name(block_id)
#     if (block_id,next_block_name) in processed_blocks:
#         print(f"Block {block_id,next_block_name} has already been processed.")
#         for item in processed_blocks:
#             if item[1] == 'IF':
#                 if_id = item[0]
#                 if int(block_id) > int(if_id):
#                     print(block_id)
#                     processed_blocks_after_if.add((block_id,next_block_name))
#                     exit()
#                 else:
#                     raise ValueError(f"Block {next_block_name} is Invalid.")
#                     # pass
#             else:
#                 pass        
        
#         pass

#     processed_blocks.add((block_id,next_block_name))
#     print("PBlock:",processed_blocks)
#     print("P_AFTER:",processed_blocks_after_if)

#     next_block_explicit_output_ports = get_next_block_explicit_output_ports(block_id)

#     for port in next_block_explicit_output_ports:
#         source_vertex = port.get('id')
#         edges = root.findall(f".//mxCell[@edge='1'][@sourceVertex='{source_vertex}']")
#         for edge in edges:
#             target_vertex = edge.get('targetVertex')
#             print(f"Source: {source_vertex}, Target: {target_vertex}")
#             next_block_id = root.find(f".//mxCell[@id='{target_vertex}']").get('ParentComponent')
#             next_block_name = get_next_block_name(next_block_id)
#             print(next_block_name, next_block_id)

#             if next_block_id:
#                 print("PROCESSED:", processed_blocks)
#                 print("AFTER:", processed_blocks_after_if)
#                 process_block_recursive(next_block_id, processed_blocks, processed_blocks_after_if, depth + 1)
#             else:
#                 block = find_block_by_target_value(target_vertex)
#                 print("AAA:", block)
#                 if isinstance(block, tuple) and len(block) == 2:
#                     block_name, block_id = block
#                     # print("BLOCKS:", block_id, block_name, processed_blocks)
#                     if block_id in processed_blocks:
#                         if block_name in ["WHILE", "FOR"]:
#                             print("in if")
#                             pass
#                         else:
#                             print("else")
#                             raise ValueError(f"Block {block_name} has already been processed.")
#                     else:
#                         print("PROCESSED:", processed_blocks)
#                         process_block_recursive(block_id, processed_blocks, processed_blocks_after_if, depth + 1)
#                 else:
#                     print("Unexpected format for block:", block)
#     return processed_blocks_after_if


# def process_blocks(style):
#     # Define the styles to process
#     styles_to_process = ["STARTBLK", "STOPBLK"]

#     # Count occurrences of each block style
#     style_counts = {style: 0 for style in styles_to_process}

#     for style_to_process in styles_to_process:
#         blocks = get_block_elements(style_to_process)

#         for block in blocks:
#             block_id = block.get('id')
#             block_style = block.get('style')
#             if block_style in style_counts:
#                 style_counts[block_style] += 1

#     # Check for multiple occurrences of STARTBLK or STOPBLK styles
#     for style, count in style_counts.items():
#         if count > 1:
#             raise ValueError(f"Multiple occurrences of {style} style found.")

#     # Process the blocks
#     for style_to_process in styles_to_process:
#         blocks = get_block_elements(style_to_process)
        
#         for block in blocks:
#             block_id = block.get('id')
#             print(f"{style_to_process} having explicitOutputPorts: {block.get('explicitOutputPorts')} and block ID: {block_id}")
#             process_block_recursive(block_id, processed_blocks=set(), processed_blocks_after_if=set())

# try:
#     process_blocks("STARTBLK")
# except ValueError as e:
#     print(e)