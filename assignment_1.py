import re
import sys
import time

#decide it match or not
def satisfy_or_not(s,id):
    if s==len(path)-1:
        stack.pop()
        stack.append(-1)
        print(id)
#startelement
def func(element,id):
    if element==path[stack[-1]+1]:
        stack.append(stack[-1]+1)
        satisfy_or_not(stack[-1],id)
    else:
        if element == path[table[stack[-1]]]:
            stack.append(table[stack[-1]])
            satisfy_or_not(stack[-1],id)
        else:
            if element==path[0]:
                stack.append(0)
                satisfy_or_not(stack[-1],id)
            else:
                stack.append(-1)
# initialization
starttime = time.time()
xpath = sys.argv[2]
file = sys.argv[1]
path = re.split('/+',xpath)
path.remove(path[0])
table = []
stack = [-1]
id = -1
path_string = re.sub(r'/+','',xpath)
# creat the "partial macth” table
for n in range(1,len(path)+1):
    prefix_s =path_string[0:n]
    postfix_s= prefix_s
    prefix= []
    postfix= []
    while(len(prefix_s)>0):
        prefix_s = prefix_s[:-1]
        prefix.append(prefix_s)

    while(len(postfix_s)>0):
        postfix_s = postfix_s[1:]
        postfix.append(postfix_s)
    intersection = list(set(postfix).intersection(set(prefix)))
    if intersection==[]:
        table.append(0)
    else:
        l =[len(i) for i in intersection ]
        table.append(max(l))


#start document
for line in open(file):
    element = re.split(' ',line.strip())
    if element[0]=='0':
        id=id+1
        func(element[1],id)
    #end element
    else:
        stack.pop()

endtime = time.time()
print ('execution time: ')
print (endtime - starttime)


