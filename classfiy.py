#/usr/bin/env python
#-*-coding: utf-8 -*-
import os
import string
import struct
import time

from util import *

'''
todo:
    1. 文件类型 平台分类；
    2. windows样本分类;
    3. 根据样本特征，区分样本家族;
'''

EI_MACHINE = {
        0:"No-machine",
        1:"AT&T-WE-32100",
        2:"SPARC",
        3:"Intel-80386",
        4:"Motorola-68000",
        5:"Motorola-88000",
        6:"Intel-MCU",
        7:"Intel-80860",
        8:"MIPS-I-Architecture",
        9:"IBM-System/370-Processor",
        10:"MIPS-RS3000-Little-endian",
        11-14:"Reserved",
        15:"Hewlett-Packard PA-RISC",
        16:"Reserved",
        17:"Fujitsu-VPP500",
        18:"Enhanced-instruction-set-SPARC",
        19:"Intel-80960",
        20:"PowerPC",
        21:"64-bit-PowerPC",
        22:"IBM",
        23:"IBM",
        24-35:"Reserved",
        36:"NEC-V800",
        37:"Fujitsu",
        38:"TRW-RH-32",
        39:"Motorola",
        40:"ARM32",
        41:"Digital-Alpha",
        42:"Hitachi-SH",
        43:"SPARC-V9",
        44:"Other",
        45-49:"Other",
        50:"Intel-IA-64",
        51:"MIPS",
        52:"Motorola",
        53:"Motorola",
        54:"Fujitsu",
        55:"Siemens",
        56:"Sony",
        57:"Denso",
        58:"Motorola",
        59:"Toyota",
        60:"STMicroelectronics",
        61:"Other",
        62:"AMD-x86-64",
        63:"Sony-DSP",
        64:"Digital-PDP-10",
        65:"Digital-PDP-11",
        66:"Siemens-FX66",
        67:"STMicroelectronics",
        68:"STMicroelectronics",
        69:"Motorola-MC68HC16",
        70:"Motorola-MC68HC11",
        71:"Motorola-MC68HC08",
        72:"Motorola-MC68HC05",
        73:"Silicon-Graphics",
        74:"STMicroelectronics",
        75:"Digital-VAX",
        76:"Axis",
        77:"Infineon",
        78:"Element-14",
        79:"LSI-Logic",
        80:"Donald-Knuth's-educational",
        81:"Harvard-University",
        82:"SiTera-Prism",
        83:"Atmel",
        84:"Fujitsu",
        85:"Mitsubishi",
        86:"Mitsubishi",
        87:"NEC-v850",
        88:"Mitsubishi",
        89:"Matsushita",
        90:"Matsushita",
        91:"picoJava",
        92:"OpenRISC-32",
        93:"ARC-International-ARCompact",
        94:"Tensilica-Xtensa",
        95:"Alphamosaic-VideoCore",
        96:"Thompson-Multimedia",
        97:"National-Semiconductor",
        98:"Tenor",
        99:"Trebia",
        100:"STMicroelectronics",
        101:"Ubicom",
        102:"MAX",
        103:"National-Semiconductor",
        104:"Fujitsu",
        105:"Texas",
        106:"Analog",
        107:"S1C33",
        108:"Sharp",
        109:"Arca",
        110:"PKU-Unity",
        111:"eXcess",
        112:"Icera",
        113:"Altera",
        114:"National",
        115:"Motorola",
        116:"Infineon",
        117:"Renesas",
        118:"Microchip",
        119:"Freescale",
        120:"Renesas",
        121-130:"Reserved for future use",
        131:"Altium",
        132:"Freescale",
        133:"Analog",
        134:"Cyan",
        135:"Sunplus",
        136:"NJR",
        137:"Broadcom",
        138:"RISC",
        139:"Seiko-Epson",
        140:"Texas",
        141:"Texas",
        142:"Texas",
        143:"Texas",
        144:"Texas",
        145-159:"Reserved",
        160:"STMicroelectronics",
        161:"Cypress",
        162:"Renesas",
        163:"NXP-Semiconductors",
        164:"QUALCOMM-DSP6",
        165:"Intel-8051",
        166:"STMicroelectronics",
        167:"Andes",
        168:"Cyan",
        168:"Cyan",
        169:"Dallas",
        170:"NJR",
        171:"M2000",
        172:"Cray",
        173:"Renesas",
        174:"Imagination",
        175:"MCST",
        176:"Cyan",
        177:"National-Semiconductor",
        178:"Freescale",
        179:"Infineon",
        180:"Intel-L10M",
        181:"Intel-K10M",
        182:"Reserved",
        183:"ARM-64-bit",
        184:"Reserved",
        185:"Atmel",
        186:"STMicroeletronics",
        187:"Tilera",
        188:"Tilera",
        189:"Xilinx",
        190:"NVIDIA-CUDA",
        191:"Tilera",
        192:"CloudShield",
        193:"KIPO",
        194:"KIPO",
        195:"Synopsys",
        196:"Open8",
        197:"Renesas",
        198:"Broadcom",
        199:"Renesas",
        200-243:"Other",
}

def readelf(elf):
    '''
    #define EI_NIDENT 16
    typedef struct{
    unsigned char e_ident[EI_NIDENT];
    Elf32_Half e_type;
    Elf32_Half e_machine;
    Elf32_Word e_version;
    Elf32_Addr e_entry;
    Elf32_Off e_phoff;
    Elf32_Off e_shoff;
    Elf32_Word e_flags;
    Elf32_Half e_ehsize;
    Elf32_Half e_phentsize;
    Elf32_Half e_phnum;
    Elf32_Half e_shentsize;
    Elf32_Half e_shnum;
    Elf32_Half e_shstrndx;
    }Elf32_Ehdr;
    '''
    e_type = e_class = 'dummpy'
    ei_ident = struct.unpack('16B', elf.read(16))
    ei_mag0, ei_mag1,ei_mag2, ei_mag3, ei_class, ei_data, ei_version, ei_pad = ei_ident[:8]
    ei_nident = ei_ident[8:]
    
    if ei_mag0 != 0x7F and ei_mag1 != ord('E') and ei_mag2 != ord('L') and ei_mag3 != ord('F'):
        print "not an ELF file"
        return "unknown-machine"

    # 32-bit OR 64-bit
    if ei_class == 1:
        e_class = '32-bit objects'
    elif ei_class == 2:
        e_class = '64-bit objects'
    else:
        print "unknown class"
        return "unknown-machine"

    # big endian OR little endian
    if ei_data == 1:
        e_data = 'ELFDATA2LSB'
    elif ei_data == 2:
        e_data = 'ELFDATA2MSB'
    else:
        return "unknown-machine"
    
    # ELF type
    if ei_data == 2:    #"big endian"
        ei_type = struct.unpack('>H', elf.read(2))[0]
    else:               #"little endian"
        ei_type = struct.unpack('<H', elf.read(2))[0]

    if ei_type == 1:
        e_type = 'Relocatable file'
    elif ei_type == 2:
        e_type = 'Executable file'
    elif ei_type == 3:
        e_type = 'Shared object file'
    elif ei_type == 4:
        e_type = 'Core file'
    elif ei_type == 0xff00:
        e_type = 'Processor-specific'
    elif ei_type == 0xffff:
        e_type = 'Processor-specific'
    else:
        print "unknown type"
        return "unknown-machine"

    #machine type
    if ei_data == 2:
        ei_machine  = struct.unpack('>H', elf.read(2))[0]
    else:
        ei_machine  = struct.unpack('<H', elf.read(2))[0]

    if ei_machine in EI_MACHINE:
        e_machine = EI_MACHINE[ei_machine]
    else:
        return "unknown-machine"

    #version
    if ei_data == 2:
        ei_version = struct.unpack('>I', elf.read(4))[0]
    else:
        ei_version = struct.unpack('<I', elf.read(4))[0]

    if ei_version == 0:
        e_version = 'illegal version'
    else:
        e_version = str(ei_version)

    #there is a bug on struct.unpack(): little endian OR big endian
    if ei_class == 1:
        ei_entry = struct.unpack('I', elf.read(4))[0]
        e_entry = ei_entry
        e_phoff, e_shoff, e_flags, e_ehsize, e_phentsize, e_phnum, e_shentsize, e_shnum, e_shstrndx = struct.unpack('IIIHHHHHH', elf.read(24))
    else:
        ei_entry = struct.unpack('Q', elf.read(8))[0]
        e_entry = ei_entry
        e_phoff, e_shoff, e_flags, e_ehsize, e_phentsize, e_phnum, e_shentsize, e_shnum, e_shstrndx = struct.unpack('QQIHHHHHH', elf.read(32))
    return e_machine
 

classfiy_dict = {}

'''
1. 查找数据库,匹配machine、size信息;
2. 如果匹配中,返回family名称, 匹配不中，返回new;
'''
def get_sample_family(machine, size, sample):
    sample_key = machine + "_" + str(size)
    if not classfiy_dict.has_key(sample_key):
        classfiy_dict[sample_key] = "new_"+str(size)
    return classfiy_dict[sample_key]

'''
1. 提供接口
'''
def add_sample_family(machine, size, family):
    sample_key = machine + "_" + str(size)
    classfiy_dict[sample_key] = family
    return

def sample_store(sample, dst):
    move_file(sample, dst)   

'''
1. 遍历样本目录，针对每个样本进行操作;
2. 判断文件大小是否满足要求；
3. 根据文件平台类型、大小、特征等确定样本所属botnet家族;
4. 存储样本;
'''
def classfiy(dir, dst_dir):
    
    if not os.path.exists(dst_dir):
        
        os.makedirs(dst_dir)

    for root,dirs,files in os.walk(dir):
        
        if 0 != len(files):

            for file in files:
                
                sample = os.path.join(root, file)
                
                size = os.path.getsize(sample)
                
                if size >= 36:

                    with open(sample, 'r') as elf:
                
                        machine = readelf(elf)

                        if not machine == "unknown-machine":
                    
                            #step 1: 通过样本所属平台、大小确定样本所属平台
                            family = get_sample_family(machine, size, sample)
                            '''
                            #step 2: 通过深度分析(样本特征)，确定样本所属family
                            if "new" == family:
                                family = deep_sample_analysis(sample)
                                add_sample_family(family)
                            '''
                            dst = os.path.join(dst_dir, family)
                        
                        else:
                            dst = os.path.join(dst_dir, "NOT_ELF")
                    
                else:
                    dst = os.path.join(dst_dir, "NOT_ELF")

                if not os.path.exists(dst):
                        
                    os.makedirs(dst)

                sample_store(sample, os.path.join(dst, file))
        

classfiy(sys.argv[1], sys.argv[2])
