#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  6 20:45:07 2018

"""
import sys

finalAcceptedString = ""
isError = False
errorRequired = ""
nonTerminalList = ["(",")","if","+","-","*","1","2","3","0","a","b","c","d","print","$"]

# This function here creates the parsing table
def parserTable():
  print("[Init] Creating parser table ...")
  parserDict = dict()
  print("[Read] Reading production rules ...")
  print("[Output] Generating ...")
  print()
  with open("parse_table.txt") as f_in:
    lines = list(line for line in (l.strip() for l in f_in) if line)
    for l in lines:
      l = l.split()
      nonterminal = l[0]
      stringer = ""
      setContinue = False
      printCounter = 0
      for i in [i for i in l[1]]:
        if(setContinue or printCounter>0):            # checks if the key is "if" or "print"
          setContinue = False
          printCounter -=1
          continue
        if(i != "["):
          if(i != "]"):
            if(i != ","):
              if(i == "i"):           # checks if the key is "if"
                stringer+="if"+","
                setContinue = True
              elif(i == "p"):         # checks if key is "print"
                stringer += "print"+","
                printCounter = 4
              else:
                stringer+=str(i)+","
      stringer = stringer[:len(stringer)-1].split(",")
      for i in stringer:
        parserDict[(nonterminal, i)] = l[2]  # parser is a two key dict ex: parserDict('L','0') = 'EM'
                                             # that is, 'L on seeing '0' must replace 'L' with 'EM'.. likewise
  return parserDict

# function to read the input  string file
def readFile(filename):
  print("[Read] Reading input string file ...")
  inputString = ""
  try:
    with open(filename+".txt") as f_in:
      lines = list(line for line in (l.strip() for l in f_in) if line)
      for i in lines:
        inputString+=i.strip()
    inputString = inputString.replace(" ", "")
    if(inputString):
      return inputString
  except:
    print("[Error] Input file not found ...")
    return None

# This function gives the list of expected inputs for the head of the stack.
# That is if head of the stack is 'L' this returns [(,0,1,2,3,a,b,c,d] as expected inputs   
def getValuesForNonTerminal(parserDict, headOfStack):
  expectedList = []
  keys = list(parserDict.keys())
  for i in keys:
    if(i[0]==headOfStack):
      expectedList.append(i[1])
  return expectedList

# This function creates the head of stack
def parseString(currentInput, stack):
  if(currentInput[0]=="i"):
    headCurrentInput = currentInput[:2]  # To tackle 'if' we need to shift two places
    if(headCurrentInput != "if"):
      print("[Error] ERROR_INVALID_SYMBOL")
      print("[Output] Rejected")
      return None, None
  elif(currentInput[0]=="p"):
    headCurrentInput = currentInput[:5]  # To tackle 'print' we need to shift five places
    if(headCurrentInput != "print"):
      print("[Error] ERROR_INVALID_SYMBOL")
      print("[Output] Rejected")
      return None, None
  else:
    headCurrentInput = currentInput[0]  # if not 'print' or 'if' only shift 1 place
    if(headCurrentInput not in nonTerminalList):
      print("[Error] ERROR_INVALID_SYMBOL")
      print("[Output] Rejected")
      return None, None
  if(stack[0]=="i"):
    headOfStack = stack[:2]   # similar logic for the stack
  elif(stack[0]=="p"):
    headOfStack = stack[:5]
  else:  
    headOfStack = stack[0]
  try:
    if(headOfStack == "^"):     # Checks if head of stack is EPSILON
      return currentInput, stack[1:]    # if EPSILON, ignore current head of stack
    replaceString = parserDict[(headOfStack, headCurrentInput)]
    stack = replaceString + stack[1:]   # Replace head of stack with relevant symbol from parser table
    return currentInput, stack
  except: # if there's no value for the head of currentInput in parser table execute the below
    if(isError):
      if(headOfStack == "$" and len(currentInput)==2): # head of the stack is at the bottom of the stack while input is not bottom of the stack
        if(currentInput[1]=="$"): # extra character in current input that needs to be deleted
          print("[Error] Got " + headCurrentInput+", but expected {$}")
          userInput = input("Delete input? Y or N : ")
          if(userInput == "Y"):
            currentInput = currentInput[1:]
            return currentInput, stack
          else:
            print("[Info] Invalid user input..")
            print("[Output] Rejected")
            return None, None
      elif(headCurrentInput == "$" and len(stack)==2):  # current input is bottom of the input but stack has values, reverse of above case
        if(stack[1]=="$"):
          print("[Error] Got " + headCurrentInput+", but expected {"+headOfStack+"}")
          userInput = input("Add input? ")
          if(userInput == headOfStack):
            currentInput = userInput+headCurrentInput
            return currentInput, stack
          else:
            print("[Info] Invalid user input..")
            print("[Output] Rejected")
            return None, None
      else:
          expectedList = getValuesForNonTerminal(parserDict, headOfStack) 
          if(expectedList):     # there is a list of values that can replace current head of stack
            expectedListString = ""
            for item in expectedList:   # creates the list of expected characters as a string seperated by ','
              expectedListString+=item + ", "
            expectedListString = expectedListString.strip()
            if(expectedListString[len(expectedListString)-1]==","):
              expectedListString = expectedListString[:len(expectedListString)-1]
            print("[Error] Got " + headCurrentInput+", but expected {" + expectedListString+" }")
            userInput = input("Add input? ")
            if(userInput in expectedList):
              if(currentInput == "$"):
                currentInput = userInput+currentInput
              else:
                currentInput = userInput+currentInput[1:]
              return currentInput, stack
            else:
              print("[Info] Invalid user input..")
              print("[Output] Rejected")
              return None, None
          else: # No items in expected list
            print("[Error] Got " + headCurrentInput+", but expected {" + headOfStack+"}")
            if(currentInput == "$"):
              userInput = input("Add input? ")
              if(userInput == headOfStack):
                currentInput = userInput+currentInput
                return currentInput, stack
              else:
                print("[Info] Invalid user input..")
                print("[Output] Rejected")
                return None, None
            else:
              userInput = input("Delete input? Y or N : ")
              if(userInput == "Y"):
                currentInput = currentInput[1:]
                return currentInput, stack
              else:
                print("[Info] Invalid user input..")
                print("[Output] Rejected")
                return None, None
    else:
      print("[Output] Rejected")
      return None, None


userInput = sys.argv[1]
if(len(sys.argv)==3):
  if(sys.argv[2]=="ERROR"):
    errorRequired = "ERROR"
  else:
    print("[INFO]  Unidentifed second argument")
if(errorRequired == "ERROR"):
  print("Parser running on : ERROR-RECOVERY MODE")
  isError = True
  stringToParse = readFile(userInput)
else:
  print("Parser running on : NON-ERROR-RECOVERY MODE")
  stringToParse = readFile(userInput)

if(stringToParse):
  print("[Info] EPSILON will be denoted by '^' symbol....")
  parserDict = parserTable()
  currentInput = stringToParse + "$"
  stack = "L$"
  reject = 0
  non_terminals = ["(",")","i","+","-","*","1","2","3","0","a","b","c","d","p"]
  print(currentInput + "                        "+stack)
  while(currentInput != "$" or stack != "$"):    # continue until input or stack is empty
    currentInput, stack= parseString(currentInput, stack)
    if(currentInput != None and stack != None):
      print(currentInput + "                        "+stack)
      while(currentInput[0] == stack[0]):  # if two symbols are equal
        if(currentInput[0] == "$" or stack[0] == "$"):
          break
        if(currentInput[0:2]=="if" and currentInput[0:2] == stack[0:2]): # handle 'if' case
          finalAcceptedString += currentInput[0:2]
          currentInput = currentInput[2:]
          stack = stack[2:]
          print(currentInput + "                        "+stack)          
        elif(currentInput[0:5]=="print" and currentInput[0:5] == stack[0:5]): # handle 'print' case
          finalAcceptedString += currentInput[0:5]
          currentInput = currentInput[5:]
          stack = stack[5:]
          print(currentInput + "                        "+stack)          
        elif(currentInput[0] == stack[0]):        # handle other cases
          finalAcceptedString += currentInput[0]
          currentInput = currentInput[1:]
          stack = stack[1:]
          print(currentInput + "                        "+stack)
    else:
      reject = 1
      break
  if(reject == 0):
    print("[Output] Accepted : " + finalAcceptedString)    


  

  
