#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  6 20:45:07 2018

"""
finalAcceptedString = ""

def parserTable():
  print("[Init] Creating parser table ...")
  parserDict = dict()
  parserDict[("E","(")] = "(F)"
  parserDict[("E", "0")] = "T"
  parserDict[("E", "1")] = "T"
  parserDict[("E", "2")] = "T"
  parserDict[("E", "3")] = "T"
  parserDict[("F", "+")] = "+EE"
  parserDict[("T", "0")] = "0"
  parserDict[("T", "1")] = "1"
  parserDict[("T", "2")] = "2"
  parserDict[("T", "3")] = "3"
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
  headCurrentInput = currentInput[0]
  headOfStack = stack[0]
  try:
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
  parserDict = parserTable()
  currentInput = stringToParse + "$"
  stack = "E$"
  reject = 0
  print(currentInput + "                        "+stack)
  while(currentInput != "$" or stack != "$"):
    currentInput, stack= parseString(currentInput, stack)
    if(currentInput != None and stack != None):
      print(currentInput + "                        "+stack)
      while(currentInput[0] == stack[0]):
        if(currentInput[0] == "$" or stack[0] == "$"):
          break
        if(currentInput[0] == stack[0]):
          finalAcceptedString += currentInput[0]
          currentInput = currentInput[1:]
          stack = stack[1:]
          print(currentInput + "                        "+stack)
    else:
      reject = 1
      break
  if(reject == 0):
    print("[Output] Accepted : " + finalAcceptedString)    


  

  
