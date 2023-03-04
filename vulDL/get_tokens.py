# -*- coding:utf-8 -*-

import re
import os
import string
import xlrd


def isphor(s, liter):
    m = re.search(liter,s)
    if m is not None:
        return True
    else: 
        return False

    
def doubisphor(forward, back):
    double = ('->','--','-=','+=','++','>=','<=','==','!=','*=','/=','%=','/=','&=','^=','||','&&','>>','<<')
    string=forward+back
    
    if string in double:
        return True
    else:  
        return False

    
def trisphor(s,t):
    if (s=='>>')|(s=='<<')and(t=='='):
        return True
    else:
        return False
    

def create_tokens(sentence):
    formal='^[_a-zA-Z][_a-zA-Z0-9]*$'
    phla='[^_a-zA-Z0-9]'
    space='\s'
    spa=''
    string=[]
    j=0
    str = sentence
    i=0
    
    while(i<len(str)):
        if isphor(str[i],space):  # ==> 检查此字符是否是空格
            if i>j:  # ==> 用来提取单词、关键字等，如果j<i，那么j到i之间的字符就是单词、关键字等
                string.append(str[j:i])  # ==> 找出单词，标记为token，加入string中
                j=i+1
            else:
                j=i+1
                
        elif isphor(str[i],phla):   # ==> 检查此字符是否是非字母数字，即是否是标记符号如括号、符号、运算符等字符
            if (i+1<len(str))and isphor(str[i+1],phla):  # ==> 检查是否是两个连续的非字母数字符号，如逗号加空格、单引号加括号等字符连接处
                m=doubisphor(str[i],str[i+1])  # ==> 检查是否是双符号操作符，如引号、双等号、*=、+=、>>、-> 等
                
                if m:  # ==> 如果是双符号操作符、标记等，如
                    string1=str[i]+str[i+1]  # ==> 将本字符与下一字符拼接成双符号操作符
                    
                    if (i+2<len(str))and (isphor(str[i+2],phla)):  # ==> 检查第三个字符是否是符号(非字母数字符号)
                        if trisphor(string1,str[i+2]):  # ==> 检查是否是三符号操作符，如>>=、<<=
                            string.append(str[j:i])  # ==> 将本符号前的单词、关键字放入string中
                            string.append(str[i]+str[i+1]+str[i+2])  # ==> 将此字符与后续两个字符拼成一个三字符操作符后，放入string中
                            j=i+3
                            i=i+2
                            
                        else:  # ==> 第三个符号不能与前两个符号构成三符号操作符，说明前两个符号是双符号操作符，第三个符号是独立符号
                            string.append(str[j:i])  # ==> 将此字符前的单词、关键字放入stirng中
                            string.append(str[i]+str[i+1])  # ==> 将此字符与后面一个符号(即第二个符号)拼成一个双符号操作符后，放入string中
                            string.append(str[i+2])  # ==> 将此字符后的第二个符号(即第三个字符)，单独放入string中
                            j=i+3
                            i=i+2
                            
                    else:  # ==> 第三个字符不是符号，是字母或数字，故还需看第三个字符后面的字符来断定第三个字符的单词、关键字
                        string.append(str[j:i])  # ==> 将此符号前的单词、关键字放入string中
                        string.append(str[i]+str[i+1])  # ==> 将此符号与后面一个符号(即第二个符号)拼成一个双符号操作符后，放入string中
                        j=i+2
                        i=i+1
                        
                else:  # ==> 若不是双符号操作符，则是两个独立符号，可能是连接处等独立分隔符号，如逗号加空格、引号加括号
                    string.append(str[j:i])  # ==> 将第一个符号的前面单词、关键字放进string中
                    string.append(str[i])  # ==> 将第一个符号单独放进string中
                    string.append(str[i+1])  # ==> 将第二个符号单独放进string中
                    j=i+2
                    i=i+1
                    
            else:
                string.append(str[j:i])  # ==> 将此符号(非字母数字的字符)前的单词放进string，然后单独放此运算符、操作符等, 若此时j=i则会将空字符放进string中
                string.append(str[i])  # ==> 将此符号单独放入string中
                j=i+1
                
        i=i+1
        
    count=0  # ==> 记录空字符数
    count1=0  # ==> 记录空格数
    sub0='\r'
    
    if sub0 in string:
        string.remove('\r')
        
    for sub1 in string:
        if sub1==' ':  # ==> 记录空格出现的次数
            count1=count1+1
            
    for j in range(count1):  # ==> 移除空格
        string.remove(' ')
        
    for sub in string:
        if sub==spa:  # ==> spa='' 记录空字符的次数，因为在之前的处理中可能会出现将空字符放入string的情况，如j=i时，str[j:i]就会是空字符''
            count=count+1
            
    for i in range(count):  # ==> 删除空字符
        string.remove('')
        
    return string
