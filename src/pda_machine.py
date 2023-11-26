import os
import argparse

state_list = []
input_list = []
stack_symbols = []
stack = []
global state 
final_states = []
accept_condition = None
transition_table = []

def printPda():
    print(state_list)
    print(input_list)
    print(stack_symbols)
    print(stack)
    print(state)
    print(final_states)
    print(accept_condition)
    for i in transition_table:
        print(i)

def inputAccepted(input, state, stack):
    for i in transition_table:
        if (i[0] == state and i[1] == input and stack[-1] == i[2]):
            return True
    return False

def splitSymbols(string):
    temp =  string.split(',')
    temp.reverse()
    return temp

def epsilonTransition(state,stack):
    can_epsilon = True
    while can_epsilon:
        can_epsilon = False
        if stack != []:
            for i in transition_table:
                if i[0] == state and i[1] == 'e' and stack[-1] == i[2]:
                    state = i[3]
                    stack.pop()
                    for j in splitSymbols(i[4]):
                        stack.append(j)
                    can_epsilon = True
                    break
    return (state,stack)

dirname = os.path.dirname(__file__)

parser = argparse.ArgumentParser()
parser.add_argument("a")
parser.add_argument("b")
args = parser.parse_args()

nama_file_pda = args.a
nama_file_pda = os.path.join(dirname,nama_file_pda)
file_pda = open(nama_file_pda,"r")
#print(file_pda)

nama_file_html = args.b
nama_file_html = os.path.join(dirname,nama_file_html)
file_html = open(nama_file_html,"r")

# convert pda from txt to py
for word in file_pda.readline().split():
    state_list.append(word)
for word in file_pda.readline().split():
    input_list.append(word)
for word in file_pda.readline().split():
    stack_symbols.append(word)
state = file_pda.readline().split()[0]
for word in file_pda.readline().split():
    stack.append(word)
for word in file_pda.readline().split():
    final_states.append(word)
accept_condition = file_pda.readline().split()[0]
for line in file_pda:
    if (line.strip()):
        transition_table.append(line.split())
#printPda()

Lines = file_html.readlines()

word_buffer = ""
m=1
last_input = m
last_input_char = 0
for line in Lines:
    n=0
    for char in line:
        n += 1
        input = None
        state, stack = epsilonTransition(state,stack)
        old_state = state[:]
        old_stack = stack[:]

        if char != ' ' and char != '\n': 
            word_buffer += char
            # print(word_buffer)

        if word_buffer in input_list:  
            input = word_buffer

        if input != None:
            can_search = False
            if stack != []:
                for i in transition_table:
                    if i[0] == state and i[1] == input and (stack[-1] == i[2] or i[2] == '%'):
                        state = i[3]
                        temp = stack[-1]
                        stack.pop()
                        if i[4] != 'e':
                            for j in splitSymbols(i[4]):
                                if j == '%':
                                    stack.append(temp)
                                else:
                                    stack.append(j)
                        can_search = True
                        break
            if can_search:
                last_input = m
                last_input_char = n
                word_buffer = ''
                # print(input,old_state,old_stack,state,stack)
                # print(input,m,state,stack)
            # else:
            #     print(input)
        
        if input == None or not can_search:
            # '%' sebagai pengganti simbol 'all'
            for i in transition_table:
                if i[0] == state and i[1] == '%' and (stack[-1] == i[2] or i[2] == '%'):
                    word_buffer = ""
                    state = i[3]
                    temp = stack[-1]
                    stack.pop()
                    if i[4] != 'e':
                        for j in splitSymbols(i[4]):
                            # print(j)
                            if j == '%':
                                stack.append(temp)
                            else:
                                stack.append(j)
                    break
    m += 1

epsilonTransition(state,stack)
# print(state,stack)
if (accept_condition == "F" and state in final_states) or (accept_condition == "E" and stack == []):
    print("Accepted")
else:
    print("Syntax Error")
    temp_line = Lines[last_input-1]
    print(f"Terjadi kesalahan ekspresi pada line {last_input} : '{temp_line[:last_input_char].rstrip()+"\033[4m"+temp_line[last_input_char:].rstrip()+"\033[0m"}' karakter ke-{last_input_char+1} : '{temp_line[last_input_char].rstrip()}'")
    temp = []
    for i in transition_table:
        if i[0] == state and i[2] == stack[-1] and splitSymbols(i[4])[0] != stack[-1]:
            temp.append(i[1])
    if len(temp)>0:
        print("Expected input: ",end="")
        for i in range(len(temp)):
            if (i>0):
                print(", ",end="")
            print(temp[i],end=" ")
    else:
        temp = []
        for i in transition_table:
            if i[0] == state and i[2] == stack[-1]:
                temp.append(i[1])
        if len(temp)>0:
            print("Expected input: ",end="")
            for i in range(len(temp)):
                if (i>0):
                    print("|| ",end="")
                print(temp[i],end=" ")
