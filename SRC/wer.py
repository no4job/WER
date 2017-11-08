# import numpy
import time
import Levenshtein
import re
import os
# import csv
import csv_tools
# import editdistance
import collections
def wer(r, h):
    """
    Calculation of WER with Levenshtein distance.

    Works only for iterables up to 254 elements (uint8).
    O(nm) time ans space complexity.

    Parameters
    ----------
    r : list
    h : list

    Returns
    -------
    int

    Examples
    --------
    >>> wer("who is there".split(), "is there".split())
    1
    >>> wer("who is there".split(), "".split())
    3
    >>> wer("".split(), "who is there".split())
    3
    """
    # initialisation
    # d = numpy.zeros((len(r)+1)*(len(h)+1), dtype=numpy.uint8)
    d = numpy.zeros((len(r)+1)*(len(h)+1), dtype=numpy.uint16)
    # d = numpy.zeros((len(r)+1)*(len(h)+1), dtype=numpy.uint32)
    d = d.reshape((len(r)+1, len(h)+1))
    for i in range(len(r)+1):
        for j in range(len(h)+1):
            if i == 0:
                d[0][j] = j
            elif j == 0:
                d[i][0] = i

    # computation
    for i in range(1, len(r)+1):
        for j in range(1, len(h)+1):
            if r[i-1] == h[j-1]:
                d[i][j] = d[i-1][j-1]
            else:
                substitution = d[i-1][j-1] + 1
                insertion    = d[i][j-1] + 1
                deletion     = d[i-1][j] + 1
                d[i][j] = min(substitution, insertion, deletion)

    return d[len(r)][len(h)]

def Convert_to_UTF_string(compared,ref):
    ref_count = 0
    # ref_dict = collections.OrderedDict()
    # compared_dict = collections.OrderedDict()
    wrd_dict = {}
    # compared_dict = {}
    # ref_dict = {}
    # compared_dict = {}
    for wrd in ref:
        wrd_dict[wrd]=chr(ref_count).encode('utf-8')
        ref_count += 1
    for wrd in compared:
        wrd_dict[wrd]=chr(ref_count).encode('utf-8')
        ref_count += 1
        # utf_code = ref_dict.get(compared_wrd,None)
        # if not utf_code:
        #     utf_code = chr(ref_count).encode('utf-8')
        #     ref_count += 1
        # compared_dict[compared_wrd]= utf_code
    ref_str = ''.join(str(wrd_dict[wrd], encoding='utf-8') for wrd in ref)
    compared_str = ''.join(str(wrd_dict[wrd], encoding='utf-8') for wrd in compared)
    return [compared_str,ref_str]

'''
def save_csv(compared,ref,edit_ops,csv_file,append = 0):
    out_csv = csv_tools.csvLog(csv_file,append)
    # header_list = sort_headers(list(get_field_type_list(patent_list)))
    # if append == 0:
    #     out_csv.add_row(header_list)
    for patent in patent_list:
        csv_row = []
        for header in header_list:
            value = filter_blank(patent.get(header) or "")
            value = trim_leading_signes(value)
            trim_leading_signes
            csv_row.append(value)
        out_csv.add_row(csv_row)
        # if value !=None:
        #     csv_row.append(value)
        # else:
        #     csv_row.append(value)
    return out_csv

def syncronize_list__(lst_1,lst_2,edit_ops):
    deletion = []
    insertion = []
    replacement = []
    lst_1_sync = list(lst_1)
    lst_2_sync = list(lst_2)
    for op in edit_ops:
        if op[0] == 'delete':
            deletion.append(op[1])
        if op[0] == 'insert':
            insertion.append(op[1])
        if op[0] == 'replace':
            replacement.append(op[1])
    insertion.sort(reverse=True)
    for delete_position in deletion:
        lst_1_sync[delete_position]=">"+lst_1_sync[delete_position]+"<"
    for replace_position in replacement:
        lst_1_sync[replace_position]="|"+lst_1_sync[replace_position]+"|"
    for insert_position in insertion:
        lst_1_sync.insert(insert_position,'<>')
    for delete_position in range(len(lst_1_sync)):
        if re.match('^>[^<>]*<$',lst_1_sync[delete_position]):
            lst_2_sync.insert(delete_position,'')
    return lst_1_sync,lst_2_sync
'''
def syncronize_list(lst_1,lst_2,edit_ops):
    deletion = []
    insertion = []
    replacement = []
    lst_1_sync = list( [e,''] for e in lst_1)
    lst_2_sync = list( [e,''] for e in lst_2)
    for op in edit_ops:
        if op[0] == 'delete':
            deletion.append(op[1])
        if op[0] == 'insert':
            insertion.append(op[1])
        if op[0] == 'replace':
            replacement.append(op[1])
    insertion.sort(reverse=True)
    for delete_position in deletion:
        # lst_1_sync[delete_position]=">"+lst_1_sync[delete_position]+"<"
        lst_1_sync[delete_position][1]='delete'
    for replace_position in replacement:
        # lst_1_sync[replace_position]="|"+lst_1_sync[replace_position]+"|"
        lst_1_sync[replace_position][1]='replace'
    for insert_position in insertion:
        # lst_1_sync.insert(insert_position,'<>')
        lst_1_sync.insert(insert_position,['','insert'])
    for delete_position in range(len(lst_1_sync)):
        # if re.match('^>[^<>]*<$',lst_1_sync[delete_position]):
        if lst_1_sync[delete_position][1] == 'delete':
            lst_2_sync.insert(delete_position,['','skip'])
    return lst_1_sync,lst_2_sync

def get_all_syncronized_list(ref_file_path,compared_file_dir_path, compared_file_pattern):
    all_syncronized_list = []
    for filename in os.listdir(compared_file_dir_path):
        if re.match(compared_file_pattern,filename):
            with open(ref_file_path, 'r', encoding='utf-8') as ref_file, \
                    open(compared_file_dir_path+filename, 'r', encoding='utf-8') as compared_file:
                ref_str = ref_file.read().replace('\n', ' ').replace('\r', ' ')
                compared_str = compared_file.read().replace('\n', ' ').replace('\r', ' ')
            ref = ref_str.split()
            compared = compared_str.split()
            converted_str = Convert_to_UTF_string(compared,ref)
            compared_str = converted_str[0]
            ref_str = converted_str[1]
            edit_ops = Levenshtein.editops(compared_str, ref_str)
            # compared_sync,ref_sync = syncronize_list(compared,ref,edit_ops)
            syncronized_list=list(syncronize_list(compared,ref,edit_ops))
            syncronized_list.append(filename)
            all_syncronized_list.append(syncronized_list)
    return all_syncronized_list

def syncronize_all(all_syncronized_list):
    all_skip_num_list =[]
    max_skip_num_list =[]
    ref_syncronized_list = []
    all_compared_syncronized_list = []
    for syncronized_list in all_syncronized_list:
        skip_num=0
        # no_skip_count = 0
        skip_num_list = []
        for element in syncronized_list[1]:
            if element[1]=='skip':
                skip_num+=1
            else:
                skip_num_list.append(skip_num)
                skip_num = 0
        # if  skip_num != 0:
        skip_num_list.append(skip_num)
        all_skip_num_list.append([skip_num_list,syncronized_list[2]])
    for i in range(len(all_skip_num_list[0][0])):
        max_skip_num_list.append(max(skip_num_list[0][i] for skip_num_list in all_skip_num_list))

    # no_skip_number = None
    no_skip_number = 0
    for element in all_syncronized_list[0][1]:
        if element[1]!='skip':
            ref_syncronized_list.extend([['','skip'] for x in range(max_skip_num_list[no_skip_number])])
            # ref_syncronized_list.append(['','skip']*max_skip_num_list[no_skip_number])
            no_skip_number+=1
            ref_syncronized_list.append(element)
    # if  len(max_skip_num_list)== no_skip_number+1:
    ref_syncronized_list.extend([['','skip'] for x in range(max_skip_num_list[no_skip_number])])



    for syncronized_list in all_syncronized_list:
        compared_syncronized_list = []
        no_skip_number = 0
        skip_number = 0
        for element in syncronized_list[0]:
            # if element[1]!='delete' and element[1]!='insert':
            if element[1]!='delete':
                compared_syncronized_list.extend([['','skip']
                                                  for x in range(max_skip_num_list[no_skip_number]-skip_number)])
                # ref_syncronized_list.append(['','skip']*max_skip_num_list[no_skip_number])
                no_skip_number+=1
                skip_number = 0
            else:
                skip_number+=1
            compared_syncronized_list.append(element)
        # if  len(max_skip_num_list)== no_skip_number+1:
        compared_syncronized_list.extend([['','skip']
                                          for x in range(max_skip_num_list[no_skip_number]-skip_number)])
        all_compared_syncronized_list.append([compared_syncronized_list,syncronized_list[2]])
    return ref_syncronized_list,all_compared_syncronized_list

if __name__ == "__main__":
    CALC_DIR = 1
    # import doctest
    # doctest.testmod()
    # print (wer("who is there".split(), "who is there 123".split()))
    REF_FILE_DIR_PATH = '../IN/'
    REF_FILE_NAME = 'ref.txt'
    COMPARED_FILE_DIR_PATH = '../IN/'
    COMPARED_FILE_NAME = 'compared.txt'
    start_time = time.clock()
    if CALC_DIR:
        all_syncronized_list = get_all_syncronized_list(REF_FILE_DIR_PATH+REF_FILE_NAME,COMPARED_FILE_DIR_PATH, r'^compared_\d+')
        syncronize_all(all_syncronized_list)
    else:
        with open(REF_FILE_DIR_PATH+REF_FILE_NAME, 'r', encoding='utf-8') as ref_file, \
                open(COMPARED_FILE_DIR_PATH+COMPARED_FILE_NAME, 'r', encoding='utf-8') as compared_file:
            ref_str = ref_file.read().replace('\n', ' ').replace('\r', ' ')
            compared_str = compared_file.read().replace('\n', ' ').replace('\r', ' ')
        ref = ref_str.split()
        compared = compared_str.split()
        converted_str = Convert_to_UTF_string(compared,ref)
        compared_str = converted_str[0]
        ref_str = converted_str[1]
        # print (compared_str)
        # print (ref_str)
        # print (Levenshtein.distance(compared_str, ref_str))
        edit_ops = Levenshtein.editops(compared_str, ref_str)
        print (len(edit_ops))
        print (edit_ops)
        # ******  tested OK 616s
        # print(wer(compared_str.split()[:10000:],ref_str.split()[:10000:]))
        # ******  tested OK 1.26s
        # ****** print(editdistance.eval(compared_str.split(),ref_str.split()))
        compared_sync,ref_sync = syncronize_list(compared,ref,edit_ops)
        print(ref_sync)
        print(compared_sync)
    finish_time = time.clock()
    print("{:.2f}s".format((finish_time-start_time)))
    exit(0)