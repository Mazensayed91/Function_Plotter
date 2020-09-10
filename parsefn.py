# useful modules 
import matplotlib.pyplot as plt
import numpy as np
import string
import operator
import re


class DrawEquation():
    def __init__(self,function,x_min,x_max):
        self.function = function
        self.equation_parsed = {}
        self.operators = ['+','-','/','*']
        self.external_operators = []
        self.ops = {
            '+' : operator.add,
            '-' : operator.sub,
            '*' : operator.mul,
            '/' : operator.truediv,  
            '^' : operator.pow
        }
        self.formatted_function = []
        self.y = []
        self.xs = [t * 0.01 for t in range(x_min*100,x_max*100)]
           
    
    def formatFunction(self):
        self.function = self.function.translate({ord(c): None for c in string.whitespace})
        fn_splitted = re.findall('\w+|\W+',self.function)
        number_xs = sum(np.array(fn_splitted) == 'x')
        number_power = sum(np.array(fn_splitted) == '^')
        x = len(re.findall('[+-]\d[+-]',self.function))+2
        for j in range(x):
            for i in range(len(fn_splitted)):
                if fn_splitted[i].isnumeric() and (i==0 or fn_splitted[i-1] in ['+','-']) and (i==len(fn_splitted)-1 or fn_splitted[i+1] in ['+','-']):
                        fn_splitted.insert(i+1,'0')
                        fn_splitted.insert(i+1,'^')
                        fn_splitted.insert(i+1,'x')
                        fn_splitted.insert(i+1,'*')

        for j in range(number_xs - number_power+1):
            for i in range(len(fn_splitted)):
                if fn_splitted[i] == 'x' and (fn_splitted[i-1] in ['+','-'] or i == 0):
                    fn_splitted.insert(i,'*')        
                    fn_splitted.insert(i,'1')


                if fn_splitted[i] == 'x' and ((i == len(fn_splitted)-1) or fn_splitted[i+1] in ['+','-']):
                    fn_splitted.insert(i+1,'1')        
                    fn_splitted.insert(i+1,'^')
        self.formatted_function = fn_splitted
        return self.formatted_function
    
    def parseEquation(self):
        i = 0
        for element in self.formatted_function:
            factor = self.formatted_function[i]
            i+=1
            op = self.formatted_function[i]
            i+=3
            power = self.formatted_function[i]
            i+=2
            self.equation_parsed[factor+'_'+str(i)] = [op]
            self.equation_parsed[factor+'_'+str(i)].append(power)


            #print(factor,op,power)
            if i >= len(self.formatted_function)-1:
                break
        self.external_operators = re.findall('[+-]',self.function)

    
    def evaluateFunction(self):
        for x in self.xs:
            if x == 0:
                x+=0.00000000001
            terms = []
            for key in (self.equation_parsed.keys()):
                op = self.equation_parsed[key][0]
                power = self.equation_parsed[key][1]
                factor = key.split('_')[0]
                term_without_factor = self.ops['^'](x,int(power))
                term_with_factor = self.ops[op](int(factor),term_without_factor)
                terms.append(term_with_factor)

            final = terms[0]    
            for i in range(len(self.external_operators)):
                final = self.ops[self.external_operators[i]](final,terms[i+1])
            self.y.append(final)
            
        return self.xs,self.y
        