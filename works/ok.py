# a = [1,2,3]
# b = [4,5,6]
#
# list = []
# for i in range(3):
#     c = a[i]
#     d = b[i]
#     e = (c,d)
#     list.append(e)
# print(list)

# def auth(type):
#     def out_wrapper(func):
#         def wrapper(*args,**kwargs):
#                 return func(*args,**kwargs)
#         return wrapper
#     return out_wrapper
# def index():
#     print("in the index page.")
# @auth(type="local") #"相当于执行了auth("local")和home=wrapper(home)"
# def home(a):
#     print("in the home page.")
#     return a
# @auth(type="ldap")
# def bbs(b):
#     print("in the bbs page.")
#     return b
#
# index()
# print(home("hrg"))
# print(bbs("aass"))



# def index(li):
#     for i in range(len(li)-1):
#         for j in range(len(li)-i-1):
#             if li[j] > li[j+1]:
#                 li[j],li[j+1]=li[j+1],li[j]
# li=[1,3,5,6,7,8,2,9]
# index(li)
# print(li)






s='aaaadssfsdfsggsdhshsdh'

s2=set(s)
print(s2)
s1=list(s2)
print(s1)
s3=sorted(s1)
print(s3)

