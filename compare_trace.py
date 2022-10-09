import os
import sys


def trace_parser(line):
    result = {}
    tokens = line.split()
    if( len(tokens) > 0 ):
        if( tokens[0] == "[F]" ):
            result["pc"] = tokens[1]
            result["instr"] = tokens[2]
            return {}
        elif( tokens[0] == "[D]" ):
            result["opcode"] = bin( int( tokens[2], 16 ) )[2:].rjust( 7, "0" )
            if result["opcode"] == '0000000':
                return {"opcode": "00000"}
            result["rd"] = bin( int( tokens[3], 16 ) ) [2:].rjust( 5, "0" ) 
            result["rs1"] = bin( int( tokens[4], 16 ) ) [2:].rjust( 5, "0" ) 
            result["rs2"] = bin( int( tokens[5], 16 ) ) [2:].rjust( 5, "0" ) 
            result["funct3"] = bin( int( tokens[6], 16 ) )[2:].rjust( 3, "0" ) 
            result["funct7"] = bin( int( tokens[7], 16 ) )[2:].rjust( 7, "0" ) 
            result["imm"] = bin( int( tokens[8], 16 ) ) [2:].rjust( 31, "0" ) 
            result["shamt"] = bin( int( tokens[9], 16 ) ) [2:].rjust( 5, "0" ) 
        #* [R] rs1 rs2 rd data_rs1 data_rs2 we
        elif( tokens[0] == "[R]" ):
            result["rs1"] = bin( int( tokens[1], 16 ) ) 
            result["rs2"] = bin( int( tokens[2], 16 ) ) 
            result["data_rs1"] = bin( int( tokens[3], 16 ) ) 
            result["data_rs2"] = bin( int( tokens[4], 16 ) ) 
            return {}
        # * [E] pc_address alu_result branch_taken
        elif( tokens[0] == "[E]" ):
            result["PC"] = tokens[1] 
            result["alu_result"] = bin( int( tokens[2], 16 ) ) 
            result["branch_taken"] = + bin( int( tokens[3], 16 ) ) 
            return {}
    return result


def read_all_files(folder_path, trace_list):
    # result = {<file_name>:
    #     {<F line>: {
    #         'F': <F line>,
    #         'D': <D line>,
    #         ...
    #     }
    #     ...
    #     }
    # ...
    # }
    
    all_result = dict()
    for trace in trace_list:
        one_file = dict()
        with open(os.path.join(folder_path, trace), encoding="utf-8") as t:
            one_insn = dict()
            for line in t:
                if line[1] == 'F' and len(one_insn):
                    one_file[one_insn['F']] = one_insn
                    one_insn.clear()
                one_insn[line[1]] = line
        all_result[trace] = one_file
    return all_result

def compare_each_line(all_result, trace_list):
    for lines in all_result[trace_list[0]]:
        print(lines)
    

def main():
    if len(sys.argv) == 1:
        print("Missing option [folder]!")
        print("usage: python compare_trace.py [folder]")
    else:
        folder_path = sys.argv[1]
        trace_list = os.listdir(folder_path)
        trace_list = list(filter(lambda x: x[-6:] == '.trace', trace_list))
        if len(trace_list) < 2:
            print("Cannot compare a single file or no trace files.")
            exit(0)
        all_result = read_all_files(folder_path, trace_list)
        compare_each_line(all_result, trace_list)
        


if __name__ == '__main__':
    main()
