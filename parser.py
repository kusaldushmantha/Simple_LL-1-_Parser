#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  6 20:45:07 2018

"""
finalAcceptedString = ""

def parserTable():
  print("[Init] Creating parser table ...")
  parserDict = dict()
  print("[Read] Reading production rules ...")
  with open("parse_table.txt") as f_in:
    lines = list(line for line in (l.strip() for l in f_in) if line)
    for l in lines:
      l = l.split()
      nonterminal = l[0]
      stringer = ""
      setContinue = False
      printCounter = 0
      for i in [i for i in l[1]]:
        if(setContinue or printCounter>0):
          setContinue = False
          printCounter -=1
          continue
        if(i != "["):
          if(i != "]"):
            if(i != ","):
              if(i == "i"):
                stringer+="if"+","
                setContinue = True
              elif(i == "p"):
                stringer += "print"+","
                printCounter = 4
              else:
                stringer+=str(i)+","
      stringer = stringer[:len(stringer)-1].split(",")
      for i in stringer:
        parserDict[(nonterminal, i)] = l[2]
  return parserDict

def readFile(filename):
  print("[Read] Reading input string file ...")
  inputString = ""
  with open("input.txt") as f_in:
    lines = list(line for line in (l.strip() for l in f_in) if line)
    for i in lines:
      inputString+=i.strip()
  inputString = inputString.replace(" ", "")
  if(inputString):
    return inputString
  else:
    print("[Error] Error while reading input string file ...")
    return None

def getValuesForNonTerminal(parserDict, headOfStack):
  expectedList = []
  keys = list(parserDict.keys())
  for i in keys:
    if(i[0]==headOfStack):
      expectedList.append(i[1])
  return expectedList

def parseString(currentInput, stack):
  if(currentInput[0]=="i"):
    headCurrentInput = currentInput[:2]
  elif(currentInput[0]=="p"):
    headCurrentInput = currentInput[:5]
  else:
    headCurrentInput = currentInput[0]
  if(stack[0]=="i"):
    headOfStack = stack[:2]
  elif(stack[0]=="p"):
    headOfStack = stack[:5]
  else:  
    headOfStack = stack[0]
  try:
    if(headOfStack == "^"):
      return currentInput, stack[1:]
    replaceString = parserDict[(headOfStack, headCurrentInput)]
    stack = replaceString + stack[1:]
    return currentInput, stack
  except:
    if(headOfStack == "$" and len(currentInput)==2):
      if(currentInput[1]=="$"):
        print("[Error] Got " + headCurrentInput+", but expected {$}")
        userInput = input("Delete input? Y or N : ")
        if(userInput == "Y"):
          currentInput = currentInput[1:]
          return currentInput, stack
        else:
          print("[Info] Invalid user input..")
          print("[Output] Rejected")
          return None, None
    elif(headCurrentInput == "$" and len(stack)==2):
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
        if(expectedList):
          expectedListString = ""
          for item in expectedList:
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
        else:
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

stringToParse = readFile(input("Filename : "))
if(stringToParse):
  print("[Info] EPSILON will be denoted by '^' symbol....")
  parserDict = parserTable()
  currentInput = stringToParse + "$"
  stack = "L$"
  reject = 0
  non_terminals = ["(",")","i","+","-","*","1","2","3","0","a","b","c","d","p"]
  print(currentInput + "                        "+stack)
  while(currentInput != "$" or stack != "$"):
    currentInput, stack= parseString(currentInput, stack)
    if(currentInput != None and stack != None):
      print(currentInput + "                        "+stack)
      while(currentInput[0] == stack[0]):
        if(currentInput[0] == "$" or stack[0] == "$"):
          break
        if(currentInput[0:2]=="if" and currentInput[0:2] == stack[0:2]):
          finalAcceptedString += currentInput[0:2]
          currentInput = currentInput[2:]
          stack = stack[2:]
          print(currentInput + "                        "+stack)          
        elif(currentInput[0:5]=="print" and currentInput[0:5] == stack[0:5]):
          finalAcceptedString += currentInput[0:5]
          currentInput = currentInput[5:]
          stack = stack[5:]
          print(currentInput + "                        "+stack)          
        elif(currentInput[0] == stack[0]):
          finalAcceptedString += currentInput[0]
          currentInput = currentInput[1:]
          stack = stack[1:]
          print(currentInput + "                        "+stack)
    else:
      reject = 1
      break
  if(reject == 0):
    print("[Output] Accepted : " + finalAcceptedString)    


  

  
