# v6.  check bad patterns
#Convert CSV file to the list of commands

"""
input .csv file
Michele.Martin@exelon.com, SAFE,email1@contosco.com, .fabricam1.com,*@invalid_pattern_discard.com
Michele.Martin@exelon.com,BLOCKED , jane@fourthcoffee.com , invalid_pattern_2_discard
edward_r_diedrich@bge.com, SAFE, noreply@patch.com, baltimoresun@e.baltimoresun.com, aquamail@aqua.org,,,,,,,,,,,,,,,,,,,
-->
output file:
Set-MailboxJunkEmailConfiguration "Michele.Martin@exelon.com" -TrustedSendersAndDomains @{Add="email1@contosco.com","fabricam1.com"}
Set-MailboxJunkEmailConfiguration "Michele.Martin@exelon.com" -BlockedSendersAndDomains @{Add="jane@fourthcoffee.com","invalid_pattern_2_discard"}
Set-MailboxJunkEmailConfiguration "edward_r_diedrich@bge.com" -TrustedSendersAndDomains @{Add="noreply@patch.com","baltimoresun@e.baltimoresun.com","aquamail@aqua.org"}

what it does:
1 - reads input file
2 - clean-up user nput around e-mail address
3 - report and skip lines with wrong e-mail address format
ex: a31onh+ojrzmb2xwz9sm0bg==_1103431943983_joqjofd+eeovpnsuupqgoq==@in.constantcontact.com
4. writes output file withp re-defined command tokens

usage:
python csv2cmd.py data/example.csv data/out.cmd

"""


import sys
import csv
from io import StringIO
import re

# string buider in memory (import StringIO)
class StringBuilder:
    _file_str = None
    def __init__(self):
        self._file_str = StringIO()
    def Add(self, str):
        self._file_str.write(str)
    def __str__(self):
        return self._file_str.getvalue()

# check patterns: email/domain
def is_email_or_domain(el, bad_patts):
    for patt in bad_patts:
        if re.search(patt, el):
            return False
    return True

# construct output row
def build_out_row(n, in_row):
    is_safe = False
    dbl_qt = '"'
    bad_patterns = [r"\W\@\w", r"\*\.", r"\.\*"]
    strip_chars = " .,:;()/*"    #strip these chars before and after an address
    sb  = StringBuilder()

    if isinstance(in_row, list) and len(in_row)  >= 2:  # check input format, row has not less ten 2 tokens
        if (n > 1):
            sb.Add('\n') 

        sb.Add('Set-MailboxJunkEmailConfiguration')
        sb.Add(' ' + dbl_qt + in_row[0].strip() + dbl_qt)
        if 'SAFE' in in_row[1]:
            is_safe = True
            sb.Add(' -TrustedSendersAndDomains')
        elif 'BLOCKED' in in_row[1]:
            sb.Add(' -BlockedSendersAndDomains')
        else:
            print(f"Warning: missing SAFE/BLOCKED in input row #{n}") 
            sb.Add(' ?')
        
        first_el = True
       
        for el in in_row[2:]:
            if not el:
                continue

            if not is_email_or_domain(el, bad_patterns):
               # - activate if skip row
               # print(f"Row {n} skipped; wrong address: {el}")
               # break
               # - activate if skip address
               print(f"Row {n}, skip wrong address: {el}")
               continue

            if first_el:
                sb.Add(' @{Add=')
                first_el = False     
            else:
                sb.Add(',')
            sb.Add(dbl_qt + el.strip(strip_chars) + dbl_qt)         
        sb.Add('}') 
                         
    else:
        print(f"Warning: wrong format of input row #{n}")

    return  sb.__str__()

# read next input row (generator function)
def read_rows(reader):
    cntr = 0
    for nxt_row in reader:
        cntr = cntr + 1
        yield (nxt_row, cntr)

# validate command args
def validate_args():
    args = sys.argv[1:]
    if len(args) < 2:
        print('Missing file names!')
        exit(1)
    return args

# open files
def open_files(args):
    input_fn = sys.argv[1]
    output_fn = sys.argv[2]
       
    print(f"input: {input_fn} => output: {output_fn}")

    try:   # input file
        csvfile = open(args[0], 'r')
        reader = csv.reader(csvfile, delimiter=',')
    except:
        print("Cannot open input file!")
        exit(1)

    try:  # output file
        outfile = open(args[1], 'w')
    except:
        print("Cannot open output file!")
        csvfile.close()
        exit(1)

    return (csvfile, reader, outfile)

# close files
def close_files(files):
    for file in files:
        file.close()
# main
def main():

    args = validate_args()

    (csvfile, reader, outfile) = open_files(args);
    
    for (row, cntr) in read_rows(reader):
        out_row_str = build_out_row(cntr, row)
        outfile.write(out_row_str)

    #clean-up
    close_files([csvfile, outfile])
    print(f"Done. [{cntr} rows]")

if __name__ == "__main__":
    main()

