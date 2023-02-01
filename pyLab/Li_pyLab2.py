#Evelyn Li
#08/26/2022

#Warmup 2:
def string_times(s, n):
  return s*n
def front_times(str, n):
  return str[:3]*n
def string_bits(str):
  return str[::2]
def string_splosion(str):
  return ''.join(str[:i+1] for i in range(len(str)))
def last2(str):
  return sum([str[i:i+2] == str[-2:] for i in range(len(str)-2)])
def array_count9(nums):
  return nums.count(9)
def array_front9(nums):
  return 9 in nums[:4]
def array123(nums):
  return sum([nums[i:i+3] == [1,2,3] for i in range(len(nums)-2)])>0
def string_match(a, b):
  return sum([a[i:i+2]==b[i:i+2] for i in range(min(len(a), len(b))-1)])

#Logic 2:
def make_bricks(small, big, goal): 
  return goal-5*big <= small and goal%5 <= small
def lone_sum(a, b, c):
  return sum(i*((a,b,c).count(i) == 1) for i in (a,b,c))
def lucky_sum(a, b, c):
  return sum((w:=[a,b,c])[:(w+[13]).index(13)])
def no_teen_sum(a, b, c):
  return sum(i for i in (0,a,b,c) if not i in [13,14,17,18,19])
def round_sum(a, b, c):
  return int(sum([round(i+.2,-1) for i in (a,b,c)]))
def close_far(a, b, c):
  return 1 == sum(-1<=i<=1 for i in [a-b,b-c,a-c])
def make_chocolate(small, big, goal):
  return [-1, goal - min(goal // 5, big) * 5][goal % 5 <= small and goal <= big * 5 + small]
  
#String 2
def double_char(str):
  return ''.join([c*2 for c in str])
def count_hi(str):
  return str.count('hi')
def cat_dog(str):
  return str.count('cat') == str.count('dog')
def count_code(str):
  return sum([str[i:i+2] == 'co' and str[i+3] == 'e' for i in range(len(str)-3)])
def end_other(a, b):
  return (r:=a.lower()).endswith(m := b.lower()) or m.endswith(r)
def xyz_there(str):
  return str.count('.xyz') < str.count('xyz')

#List 2 
def count_evens(nums):
  return sum([i%2==0 for i in nums])
def big_diff(n):
  return max(n) - min(n)
def centered_average(n):
  return sum(a:=sorted(n)[1:-1])//len(a)
def sum13(n):
  return sum([n[i] for i in range(len(n)) if n[i] != 13 and (n + [0])[i-1] != 13])
def sum67(nums):
  return nums and (nums[0]==6 and sum67(nums[nums.index(7)+1:]) or (nums[0] != 6 and nums[0]+sum67(nums[1:]))) or 0
def has22(nums):
  return (2, 2) in zip(nums, nums[1:])

#Evelyn Li 7 2024