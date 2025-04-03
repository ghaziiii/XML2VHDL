import xml.etree.ElementTree as ET
from datetime import datetime

def generate_vhdl_header(module_name):
    return f"""\
-- Auto-generated VHDL from XML
-- Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity {module_name} is
"""

def generate_generics(generics):
    if not generics:
        return ""
    
    generic_lines = []
    # get max length of genric names, to used for indentation
    generic_names = []
    for i, generic in enumerate(generics):
        generic_names.append(generic['name']);
    print(generic_names);
    max_length = max(len(s) for s in generic_names);
    print("max len" , max_length);
    for i, generic in enumerate(generics):
        comment = f"  -- {generic['comment']}" if generic['comment'] else ""
        line = f"        {generic['name']} {" " *(max_length - len(generic['name']) + 4)}: {generic['type']} := {generic['default']}"
        if i < len(generics) - 1:
            line = f"{line};{comment}"
        else:
            line = f"{line};{comment}"
        generic_lines.append(line)
    
    return "    generic (\n" + "\n".join(generic_lines) + "\n);\n"

def generate_ports(ports):
    if not ports:
        return ""
    
    port_lines = []
    # get max length of port names, to used for indentation
    port_names = []
    for i, port in enumerate(ports):
        port_names.append(port['name']);
    print(port_names);
    max_length = max(len(s) for s in port_names);
    print("max len" , max_length);
    for i, port in enumerate(ports):
        if port['width'] > 1:
            type_str = f"std_logic_vector({port['width']-1} downto 0)"
        else:
            type_str = "std_logic"
        comment = f"  -- {port['comment']}" if port['comment'] else ""
        line = f"        {port['name']}{" " *(max_length - len(port['name']) + 4)}: {port['direction']} {type_str}"
        if i < len(ports) - 1:
            line = f"{line};{comment}"
        else:
            line = f"{line};{comment}"
        port_lines.append(line)
    
    return "    port (\n" + "\n".join(port_lines) + "\n);\n"

def generate_signals(signals):
    if not signals:
        return ""
    
    signal_lines = ["    -- Internal signals"]
    for signal in signals:
        if signal['width'] > 1:
            type_str = f"std_logic_vector({signal['width']-1} downto 0)"
        else:
            type_str = "std_logic"
        
        default_str = ""
        if signal['default'] is not None:
            default_str = f" \t:= {signal['default']}"
        comment = f"  -- {signal['comment']}" if signal['comment'] else ""
        signal_lines.append(f"    signal {signal['name']} \t: {type_str}{default_str};{comment}")
    
    return "\n".join(signal_lines) + "\n"

def generate_registers(registers):
    if not registers:
        return ""
    
    register_lines = ["    -- Registers"]
    for reg in registers:
        register_lines.append(f"    signal {reg['name']} \t: std_logic_vector({reg['width']-1} downto 0);")
        for field in reg['fields']:
            register_lines.append(f"    -- {field['name']}\t: bits {field['bits']} (default: {field['default']})")
    
    return "\n".join(register_lines) + "\n"

def generate_components(components):
    if not components:
        return ""
    
    component_lines = ["    -- Components"]
    for comp in components:
        component_lines.append(f"    component {comp['type']}")
        component_lines.append("        port (")
        component_lines.append("        -- Port declarations")
        component_lines.append("        );")
        component_lines.append("     end component;")
    
    return "\n".join(component_lines) + "\n"

def generate_assignments(assignments):
    if not assignments:
        return ""
    
    assignment_lines = ["    -- Concurrent assignments"]
    for assign in assignments:
        comment = f"  -- {assign['comment']}" if assign['comment'] else ""
        assignment_lines.append(f"    {assign['target']} <= {assign['expression']};{comment}")
    
    return "\n".join(assignment_lines) + "\n"

def generate_processes(processes):
    if not processes:
        return ""
    
    process_lines = ["    -- Processes"]
    for proc in processes:
        process_lines.append(f"    {proc['name']}_process : process({proc['sensitivity']})")
        process_lines.append("    begin")
        for line in proc['content'].split('\n'):
            process_lines.append(f"        {line.strip()}")
        process_lines.append("    end process;")
    
    return "\n".join(process_lines) + "\n"

def xml_to_vhdl(xml_file, vhdl_file):
    """Convert XML hardware description to VHDL."""
    
    # Parse XML
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    # Extract module information
    module = {
        'name': root.attrib.get('name', 'module'),
        'generics': [],
        'ports': [],
        'signals': [],
        'registers': [],
        'components': [],
        'processes': [],
        'assignments': []
    }
    
    # Process XML elements
    for child in root:
        if child.tag == 'generic':
            module['generics'].append({
                'name': child.attrib['name'],
                'type': child.attrib.get('type', 'integer'),
                'default': child.attrib.get('default', '0'),
                'comment': child.attrib.get('comment', '')
            })
        elif child.tag == 'port':
            module['ports'].append({
                'name': child.attrib['name'],
                'direction': child.attrib['direction'],
                'type': child.attrib.get('type', 'std_logic'),
                'width': int(child.attrib.get('width', 1)),
                'comment': child.attrib.get('comment', '')
            })
        elif child.tag == 'signal':
            module['signals'].append({
                'name': child.attrib['name'],
                'type': child.attrib.get('type', 'std_logic'),
                'width': int(child.attrib.get('width', 1)),
                'default': child.attrib.get('default', None),
                'comment': child.attrib.get('comment', '')
            })
        elif child.tag == 'register':
            fields = []
            for field in child:
                fields.append({
                    'name': field.attrib['name'],
                    'bits': field.attrib['bits'],
                    'default': field.attrib.get('default', '0')
                })
            module['registers'].append({
                'name': child.attrib['name'],
                'width': int(child.attrib['width']),
                'fields': fields
            })
        elif child.tag == 'component':
            module['components'].append({
                'name': child.attrib['name'],
                'type': child.attrib['type']
            })
        elif child.tag == 'process':
            module['processes'].append({
                'name': child.attrib.get('name', 'proc'),
                'sensitivity': child.attrib.get('sensitivity', 'clk'),
                'content': child.text.strip() if child.text else ""
            })
        elif child.tag == 'assignment':
            module['assignments'].append({
                'target': child.attrib['target'],
                'expression': child.attrib['expression'],
                'comment': child.attrib.get('comment', '')
            })
    
    # Generate VHDL code
    vhdl_code = generate_vhdl_header(module['name'])
    vhdl_code += generate_generics(module['generics'])
    vhdl_code += generate_ports(module['ports'])
    vhdl_code += f"end {module['name']};\n\n"
    vhdl_code += f"architecture Behavioral of {module['name']} is\n\n"
    vhdl_code += generate_signals(module['signals']) + "\n"
    vhdl_code += generate_registers(module['registers']) + "\n"
    vhdl_code += generate_components(module['components']) + "\n"
    vhdl_code += "begin\n\n"
    vhdl_code += generate_assignments(module['assignments']) + "\n"
    vhdl_code += generate_processes(module['processes']) + "\n"
    vhdl_code += "end Behavioral;"
    
    # Write to file
    with open(vhdl_file, 'w') as f:
        f.write(vhdl_code)
    
    print(f"Successfully generated {vhdl_file}")

# Example usage
if __name__ == "__main__":
    input_xml = "hardware_config.xml"
    output_vhdl = "generated_module.vhdl"


    # Create sample XML if it doesn't exist
    try:
        with open(input_xml, 'r') as f:
            pass
    except FileNotFoundError:
        print(f"could not open file: {input_xml}")
    
    # Generate VHDL
    xml_to_vhdl(input_xml, output_vhdl)