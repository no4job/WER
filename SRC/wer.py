import numpy
import time
import Levenshtein
import editdistance
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


if __name__ == "__main__":
    # import doctest
    # doctest.testmod()
    # print (wer("who is there".split(), "who is there 123".split()))
    REF_FILE_PATH = '../IN/'
    REF_FILE_NAME = 'ref.txt'
    COMPARED_FILE_PATH = '../IN/'
    COMPARED_FILE_NAME = 'compared.txt'
    start_time = time.clock()
    with open(REF_FILE_PATH+REF_FILE_NAME, 'r', encoding='utf-8') as ref_file, open(COMPARED_FILE_PATH+COMPARED_FILE_NAME, 'r', encoding='utf-8') as compared_file:
        ref_str = ref_file.read().replace('\n', ' ').replace('\r', ' ')
        compared_str = compared_file.read().replace('\n', ' ').replace('\r', ' ')
        converted_str = Convert_to_UTF_string(compared_str.split(),ref_str.split())
        compared_str = converted_str[0]
        ref_str = converted_str[1]
        print (compared_str)
        print (ref_str)
        print (Levenshtein.distance(compared_str, ref_str))
        print (Levenshtein.editops(compared_str, ref_str))
        # ******  tested OK 616s
        # print(wer(compared_str.split()[:10000:],ref_str.split()[:10000:]))
        # ******  tested OK 1.26s
        # ****** print(editdistance.eval(compared_str.split(),ref_str.split()))
    finish_time = time.clock()
    print("{:.2f}s".format((finish_time-start_time)))
    exit(0)