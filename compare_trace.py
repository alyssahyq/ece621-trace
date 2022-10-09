import copy
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
                    one_file[one_insn['F']] = copy.copy(one_insn)
                    one_insn.clear()
                one_insn[line[1]] = line
        all_result[trace] = one_file
    return all_result

def compare_each_line(all_result, my_trace, folder_path):
    other_traces = list(all_result.keys())
    other_traces.remove(my_trace)
    flag_no_stage = True
    insn_with_disagreement = set()
    with open(os.path.join(folder_path, "result_"+my_trace[:-6]+'.txt'), 'w') as r:
        for my_insn, my_results in all_result[my_trace].items():
            flag_print_my_result = True
            for other_trace in other_traces:
                if my_insn not in all_result[other_trace]:
                    r.write(my_insn+" is an instruction in "+other_trace)
                    continue
                else:
                    stage_tokens = list(my_results.keys())
                    for stage_token in stage_tokens:
                        if stage_token not in all_result[other_trace][my_insn]:
                            if flag_no_stage:
                                r.write(other_trace + " doesn't have " + stage_token+ " stage!")
                                flag_no_stage = False # I don't wanna see endless "no such stage" messages.
                            continue
                        else:
                            if(my_results[stage_token]!= all_result[other_trace][my_insn][stage_token]):
                                if(flag_print_my_result):
                                    r.write("\n\nDisagreement on: " + my_insn)
                                    insn_with_disagreement.add(my_insn.split()[2])
                                    flag_print_my_result = False
                                r.write(my_trace + ": " + my_results[stage_token])
                                r.write(other_trace + ": " + all_result[other_trace][my_insn][stage_token])
    with open(os.path.join(folder_path, "sum_"+my_trace[:-6]+'.txt'), 'w') as s:
        for item in insn_with_disagreement:
            s.write(item+'\n')
                                
    

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
        print("Find following trace files in the directory:")
        for i in range(len(trace_list)):
            print(i, trace_list[i])
        
        my_trace = trace_list[int(input(f"Which one is your trace? (index)  "))]
        if my_trace not in trace_list:
            print("Cannot find'", my_trace, "'in the directory.")
            exit(0)
        all_result = read_all_files(folder_path, trace_list)
        compare_each_line(all_result, my_trace, folder_path)
        


if __name__ == '__main__':
    main()
