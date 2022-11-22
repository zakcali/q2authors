# q2authors
splits (distributes) output (publications) from wos2q to authors

There are two types of outputs from https://github.com/zakcali/wos2q

1- Doesn't include author-address fields. This is the default output

2- If user ticks "Include addresses" checkbox from the menu, software Reads C1 and RP fields from Web of Science output and writes Addresses and Correspondence fields to the end of output. Another utility, q2authors reads that file, and tries to split authors of a specific institution.

q2authors, reads type-2 of output of wos2q, and tries to split (distribute) journals to a specific institute, specified in addresslist.txt
If it finds variant names of authors, tries to use only one name by usinf namedict.txt
