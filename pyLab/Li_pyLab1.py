#Evelyn Li
#08/23/2022

#Warmup 1:


def sleep_in(weekday, vacation):
    return not weekday or vacation

def monkey_trouble(a_smile, b_smile):
  return (a_smile == b_smile)

def sum_double(a, b):
  return 2*a + 2*b if a == b else a + b

def diff21(n):
  return 21 - n if n <= 21 else (n - 21) * 2

def parrot_trouble(talking, hour):
  return (talking and hour < 7) or (talking and hour > 20)

def makes10(a, b):
  return (a == 10 or b == 10 or a+b == 10)

def near_hundred(n):
  return (100 - n <= 10) if n < 100 else (n - 100 <= 10) if n < 190 else (200 - n <= 10) if n < 200 else (n - 200 <= 10)

def pos_neg(a, b, negative):
  return True if (negative == True and a < 0 and b < 0) else False if ((negative == True and a > 0 and b < 0) or negative == True and a < 0 and b > 0) else True if (a < 0 and b > 0) else True if (a > 0 and b < 0) else False

#String 1:
def hello_name(name):
  return "Hello " + name + "!"

def make_abba(a, b):
  return a + b + b + a

def make_tags(tag, word):
  return "<" + tag + ">" + word + "<" + "/" + tag + ">"

def make_out_word(out, word):
  return out[0:len(out)//2] + word + out[len(out)//2:]

def extra_end(str):
  return 3 * str[-2:]

def first_two(str):
  return str if (len(str) < 2) else (str[0] + str[1])

def first_half(str):
  return str[:int(len(str) / 2)]

def without_end(str):
  return str[1:-1]

#List 1
def first_last6(nums):
  return nums[0] == 6 or nums[-1] == 6

def same_first_last(nums):
  return (len(nums) > 0 and nums[0] == nums[-1])

def make_pi(n):
  return [int(i) for i in str(314159265358979323846)[0:n]]

def common_end(a, b):
  return (a[-1] == b[-1] or a[0] == b[0])

def sum3(nums):
  return sum(nums)

def rotate_left3(nums):
  return nums[1:] + nums[:1]

def reverse3(nums):
  return nums[::-1]

def max_end3(nums):
  return [nums[0]]*len(nums) if nums[0] >= nums[-1] else [nums[-1]]*len(nums)

#Logic 1
def cigar_party(cigars, is_weekend):
  return (is_weekend and cigars >= 40) or (is_weekend == False and cigars <= 60 and cigars >= 40)

def date_fashion(you, date):
  return 0 if (you <= 2 or date <=2) else 2 if (you >=8 or date >=8) else 1

def squirrel_play(temp, is_summer):
  return (is_summer and temp in range(60, 101)) or (is_summer == False and temp in range(60, 91))

def caught_speeding(speed, is_birthday):
  return 0 if ((is_birthday and (speed-5) <= 60) or (not is_birthday and speed <= 60)) else 1 if ((is_birthday and 60 < (speed-5) < 81) or (not is_birthday and 60 < speed < 81)) else 2

def sorta_sum(a, b):
  return 20 if ((a+b)>=10 and (a+b)<=19) else (a+b)

def alarm_clock(day, vacation):
  return "10:00" if (vacation and not (day == 0 or day == 6)) else "off" if (vacation and (day == 0 or day == 6)) else "7:00" if (not (day == 0 or day == 6)) else "10:00"

def love6(a, b):
  return a+b == 6 or abs(a-b) == 6 or a == 6 or b == 6

def in1to10(n, outside_mode):
  return True if ((outside_mode and (n <= 1 or n >= 10)) or (not outside_mode and (n >= 1 and n <= 10))) else False