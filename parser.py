#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  6 20:45:07 2018

"""
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

def parseString(currentInput, stack):
  headCurrentInput = currentInput[0]
  headOfStack = stack[0]
  try:
    replaceString = parserDict[(headOfStack, headCurrentInput)]
    stack = replaceString + stack[1:]
    return currentInput, stack
  except:
    print("[Output] Rejected")
    return None, None

stringToParse = readFile(input("Filename : "))
if(stringToParse):
  parserDict = parserTable()
  currentInput = stringToParse + "$"
  stack = "E$"
  reject = 0
  while(currentInput != "$" and stack != "$"):
    currentInput, stack = parseString(currentInput, stack)
    if(currentInput != None and stack != None):
      print(currentInput + "                        "+stack)
      while(currentInput[0] == stack[0]):
        if(currentInput[0] == "$" or stack[0] == "$"):
          break
        if(currentInput[0] == stack[0]):
          currentInput = currentInput[1:]
          stack = stack[1:]
          print(currentInput + "                        "+stack)
    else:
      reject = 1
      break
  if(reject == 0):
    print("[Output] Accepted")    


  

  
