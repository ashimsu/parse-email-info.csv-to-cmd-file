# parse--email-info.csv--to-cmd-file

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
4. writes output file withpredefined command tokens

usage:
python csv2cmd.py data/example.csv data/out.cmd

"""
