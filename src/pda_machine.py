import os

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

# def splitSymbols2(string): 
#     temp = []
#     char_buffer = ""
#     for i in string:
#         if i in stack_symbols and char_buffer == "":
#             temp.append(i)
#         elif char_buffer in stack_symbols:
#             temp.append(char_buffer)
#             char_buffer = ""
#         else:
#             char_buffer += i
#     if char_buffer in stack_symbols:
#         temp.append(char_buffer)
#     temp.reverse()
#     # print("AAAA",end=" ")
#     # print(temp)
#     return temp

def inputAccepted(input, state, stack):
    for i in transition_table:
        if (i[0] == state and i[1] == input and stack[-1] == i[2]):
            return True
    return False

def splitSymbols(string):
    temp =  string.split(',')
    temp.reverse()
    return temp

dirname = os.path.dirname(__file__)

# nama_file_pda = input("Masukkan nama file definisi PDA: ")
# nama_file_pda = os.path.join(dirname, f"{nama_file_pda}.txt")
nama_file_pda = os.path.join(dirname, "PDA.txt")
file_pda = open(nama_file_pda,"r")
#print(file_pda)

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
# nama_file_html = input("Masukkan nama file HTML: ")
#nama_file_html = os.path.join(dirname, f"{nama_file_html}.txt")
nama_file_html = os.path.join(dirname, "tes_html.html")
file_html = open(nama_file_html,"r")

Lines = file_html.read().replace(' ','').replace('\n','')
print(Lines)

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

# for i in transition_table:
#     print(i)

def isAccepted(Lines,state,stack):
    word_buffer = ""
    while (Lines != ''):
        input = None
        state, stack = epsilonTransition(state,stack)
        old_state = state[:]
        old_stack = stack[:]

        if Lines[0] != ' ' and Lines[0] != '\n': 
            word_buffer += Lines[0]

        if word_buffer in input_list:  
            input = word_buffer
        # else:
        #     print(word_buffer,state,stack)

        if input != None:
            # print(input)
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
                word_buffer = ''
                print(input,old_state,old_stack,state,stack)
        
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
        Lines = Lines[1:]
    epsilonTransition(state,stack)
    return (accept_condition == "F" and state in final_states) or (accept_condition == "E" and stack == [])

print("\n",isAccepted(Lines,state,stack))
