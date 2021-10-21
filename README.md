# parse email-info.csv to .cmd-file

1 - read input file
2 - clean-up user nput around e-mail address
3 - report and skip lines with wrong e-mail address format
ex: a31onh+ojrzmb2xwz9sm0bg==_1103431943983_joqjofd+eeovpnsuupqgoq==@in.constantcontact.com
4. write output file with pre-defined command tokens

usage:
python csv2cmd.py data/example.csv data/out.cmd
