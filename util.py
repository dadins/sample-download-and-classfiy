#/usr/bin/env python
#-*-coding: utf-8 -*-
import os
import sys
import string
import shutil
import struct
import hashlib
import re

md5_file = "md5.txt"

'''
1. 将源文件(包含路径)移到目标文件(包含路径);
2. 如果有同名文件,则在字符串后面+1,直到无同名文件为止
'''
def move_file(src, org_dst):
    '''
    1. 获取源文件的MD5值;
    2. 判断是否存在同名文件,如果存在则对比MD5,否则跳过此步骤；
    3. 如果MD5值相同，则退出，否则迭代对比;
    '''
    num = 1
    hash_md5 = md5(src)
    dst = org_dst
    
    while os.path.exists(dst):
        if hash_md5 == md5(dst):
            os.remove(src)
            return 
        else:
            dst = org_dst + str(num)
            num += 1
    '''
    1. 存储样本文件的MD5值(后续可以考虑存储倒redis的数据库中)
    2. 将样本文件move到指定的位置
    '''
    md5_path = os.path.join(os.path.dirname(dst), md5_file)
    store_md5(dst, hash_md5, md5_path)
    shutil.move(src, dst)

def md5(filename):
    return str(hashlib.md5(open(filename, "rb").read()).hexdigest())

def store_md5(md5_file, md5_key, md5_value):
    md5_info = md5_key + "\t" + md5_value + "\n"
    open(md5_file, "a+").write(md5_info)


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



'''
impletent of linux strings cmd
'''
def strings(file) :
    chars = r"A-Za-z0-9/\-:|.,_$%'()[\]<> "
    shortestReturnChar = 4
    regExp = '[%s]{%d,}' % (chars, shortestReturnChar)
    pattern = re.compile(regExp)
    with open(file, 'rb') as f:
        return pattern.findall(f.read())
