import sys; args = sys.argv[1:]
idx = int(args[0])-30

myRegexLst = [
  r"/^0$|^10[10]$/", # 30
  r"/^[01]*$/", # 31
  r"/0$/", # 32
  r"/\w*[aeiou]\w*[aeiou]\w*/i", # 33
  r"/^1[10]*0$|^0$/", # 34
  r"/^[10]*110[10]*$/", # 35
  r"/^.{2,4}$/s", # 36
  r"/^\d{3} *-? *\d\d *-? *\d{4}$/", # 37
  r"/^.*?d\w*/mi", # 38
  r"/^1[01]*1$|^0[01]*0$|^[10]$|^$/", # 39
  r"/^[x.o]{64}$/i",  # 40
  r"/^[xo]*\.[xo]*$/i",  # 41
  r"/^x+o*\.|\.o*x+$|\.$|^\./i",  # 42
  r"/^(..)*.$/s",  # 43
  r"/^(0|1[01])([01]{2})*$/",  # 44
  r"/\w*(a[eiou]|e[aiou]|i[aeou]|o[aeiu]|u[aeio])\w*/i",  # 45
  r"/^(1?0)*1*$/",  # 46
  r"/^\b[bc]*a?[bc]*$/",  # 47
  r"/^\b([bc]|(a[bc]*){2})*$/",  # 48
  r"/^\b(20*)*((1[02]*){2})*$/",  # 49
  r"/(\w)*\w*\1\w*/i",  # 50
  r"/(\w)*\w*(\1\w*){3}/i",  # 51
  r"/^(1|0)([01]*\1)*$/",  # 52
  r"/\b(?=\w*cat)\w{6}\b/i",  # 53
  r"/\b(?=\w*bri)(?=\w*ing)\w{5,9}\b/i",  # 54
  r"/\b(?!\w*cat)\w{6}\b/i",  # 55
  r"/\b(?!(\w)*\w*\1)\w+/i",  # 56
  r"/(?!.*10011)^[01]*$/",  # 57
  r"/\w*([aeiou])(?!\1)[aeiou]\w*/i",  # 58 -2
  r"/^((?!1[01]1)[10])*$/",  # 59 ----
  r"/(?!.*010)^[01]*$/",  # 60 16 14
  r"/(?!.*(101|010))^[01]*$/",  # 61 22 20
  r"/^(1|0)([01]*\1)*$/",  # 62 17 14
  r"/\b(?!\w*(\w)\w*\1\b)\w+/i",  # 63 23 21
  r"/\b(?=(\w)*((\w*\1){3}|\w*\1(\w)*\4)|(\w)*(\w)*\w*(\6\w*\5|\5\w*\6))\w*/i",  # 64 70 43
  r"/\b(?=(\w)*(\w*\1){2,})(?!\w*(?!\1)(\w)\w*\3)\w*/i",  # 65 47 44
  r"/\b(?!\w*([aeiou])\w*\1)(?=\w*a)(?=\w*e)(?=\w*o)(?=\w*i)(?=\w*u)\w*/i",  # 66 66 39
  r"/^(?=(0*(10*1)?0*)*$)([10]{2})*[10]$/",  # 67 36 22
  r"/^(0|(1(01*0)*10*)+)$/",  # 68 20 19
  r"/^1((10*1)*(01*0)?)*(01*)?$/",  # 69 26 19
]

'''
30: Determine whether a string is either 0, 100, or 101.
31: Determine whether a given string is a binary string (ie. composed only of  0 and 1 characters).
32: Given a binary integer string, what regular expression determines whether it is even?
33: What is a regular expression to determine (ie. match) those words in a text that have at least two vowels?
34: Given a string, determine whether it is a non-negative, even binary integer string.
35: Determine whether a given string is a binary string containing 110 as a substring.
36: Match on all strings of length at least two, but at most four.
37: Validate a social security number entered into a field 
    (ie. recognize ddd-dd-dddd where the d represents digits and where the dash indicates an arbitrary number of spaces with at most one dash). 
    For example, 542786363, 542  786363, and 542 - 78-6263 are all considered valid.
38: Determine a regular expression to help you find the first word of each line of text with a  d  in it: 
    Match through the end of the first word with a d on each line that has a d.
39: Determine whether a string is a binary string that has the same number of 01 substrings as 10 substrings.

Q40: Write a regular expression that will match on an Othello board represented as a string.
Q41: Given a string of length 8, determine whether it could represent an Othello edge with exactly one hole.
Q42: Given an Othello edge as a string, determine whether there is a hole such that if X plays to the hole (assuming it could), 
     it will be connected to one of the corners through X tokens.  Specifically, this means that one of the ends must be a hole, or 
     starting from an end there is a sequence of at least one x followed immediately by a sequence (possibly empty) of o, immediately followed by a hole.
Q43: Match on all strings of odd length.
Q44: Match on all odd length binary strings starting with 0, and on even length binary strings starting with 1.
Q45: Match all words having two adjacent vowels that differ.
Q46: Match on all binary strings which DON'T contain the substring 110.
Q47: Match on all non-empty strings over the alphabet {a, b, c} that contain at most one a.
Q48: Match on all non-empty strings over the alphabet {a, b, c} that contain an even number of a's.
Q49: Match on all positive, even, base 3 integer strings.

Q50: Match all words where some letter appears twice in the same word.
Q51: Match all words where some letter appears four times in the same word.
Q52: Match all non-empty binary strings with the same number of 01 substrings as 10 substrings.
Q53: Match all six letter words containing the substring cat.
Q54: Match all 5 to 9 letter words containing both the substrings bri and ing.
Q55: Match all six letter words not containing the substring cat.
Q56: Match all words with no repeated characters.
Q57: Match all binary strings not containing the forbidden substring 10011.
Q58: Match all words having two different adjacent vowels.
Q59: Match all binary strings containing neither 101 nor 111 as substrings.

Q60: Match all binary strings that do not contain the forbidden substring 010.  (14)
Q61: Match all binary strings containing neither 101 nor 010 as substrings.  (20)
Q62: Match on all non-empty binary strings with the same number of 01 substrings as 10 substrings.  (14)
Q63: Match all words whose final letter is not to be found elsewhere in the word.  (21)  
Q64: Match all words that have at least two pairs of doubled letters (two pairs of distinct letters or four of the same letter are both OK).  (43)
Q65: Match all words that have no duplicate letter, except for one, which occurs at least 3 times.  (42)
Q66: Match all words where each of the five vowels occurs exactly once.  (39)
Q67: Match all binary strings that have an odd number of 0s and an even number of 1s.  (22)
Q68: Match all binary integer strings that are divisible by 3.  (19)
Q69: Match all binary integer strings that are not divisible by 3.  (19)
'''

if idx < len(myRegexLst):
  print(myRegexLst[idx])

#Evelyn Li, pd 7, 2023