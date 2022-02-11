import re

consoleOn = True
currentMode = "execute" # Mode can be token, parse, or execute
stopWords = ["quit", "stop", "exit", "q"]
commands = ["if", "else", "while", "for", "function", "write"]

# ================= PREPROCESSING ===============
def preprocesser(text):
    # Removes capital letters
    text = text.lower()
    
    # Removes punctutation    
    text = re.sub(r'[\?\!\,\:\"]', '', text)

    # Identifies stop words
    for stopWord in stopWords:
      if text == stopWord:
        return None;
    
    return text;

# =================== PARSING ===================
def tokenizer(text):
  # Splits tokens into list at spaces
  tokens = re.split("\s", text)
  
  # Gets rid of empty strings
  tokens = [token for token in tokens if token]

  return tokens

def parser(tokens):
  typeList = [None] * len(tokens)

  for tokenIndex, token in enumerate(tokens):
    #tokenIndex = tokens.index(token)
    tokenHasType = False
    
    # Identifies float values
    try:
      float(token)
      typeList[tokenIndex] = ["FLOAT", token]
      tokenHasType = True
    except:
      pass

    # Identifies integer values
    try:
      int(token)
      typeList[tokenIndex] = ["INT", token]
      tokenHasType = True
    except:
      pass
    
    # Identifies assignment operator
    if token == "is" and not tokenHasType:
      typeList[tokenIndex] = ["ASSIGNMENT OPERATOR", token]
    
    # Identifies assignment operator
    elif token == "equals" and not tokenHasType:
      typeList[tokenIndex] = ["COMPARISON OPERATOR", token]
    
    # Identifies assignment operator
    elif token == "plus" or token == "minus" or token == "times" or token == "over" and not tokenHasType:
      typeList[tokenIndex] = ["MATH OPERATOR", token]
    
    # Identifies command
    elif token in commands and not tokenHasType:
      typeList[tokenIndex] = ["COMMAND", token]
    
    # Identifies end keyword
    elif token == "end" and not tokenHasType:
      typeList[tokenIndex] = ["END", token]

    # Identifies string values
    elif type(token) == str and not tokenHasType:
      typeList[tokenIndex] = ["STRING", token]
    
    # Identifies type errors
    else:
      if not tokenHasType:
        print("ERROR: token is of type unknown")
        return None
  
  for typeListItem in typeList:
    if typeListItem == None:
      print("INTERPRETER ERROR: type list was not fully ")
      return None
  
  return typeList

# ================== EXECUTER =================

# All variables are stored in this dictionary
variables = {"examplevariable": "examplevalue"}

def preExecute(tokens):
  for tokenIndex, token in enumerate(tokens):

    # ====================== MATH ======================
    if token[0] == "MATH OPERATOR":
      finalValue = 0

      num1 = tokens[tokenIndex - 1][1]
      num2 = tokens[tokenIndex + 1][1]

      if tokens[tokenIndex - 1][0] == 'FLOAT':
        num1 = float(num1)
      elif tokens[tokenIndex - 1][0] == 'INT':
        num1 = int(num1)

      if tokens[tokenIndex + 1][0] == 'FLOAT':
        num2 = float(num2)
      elif tokens[tokenIndex + 1][0] == 'INT':
        num2 = int(num2)
      
      # Identifies string math other than addition
      if token[1] != "plus" and (tokens[tokenIndex - 1][0] == 'STRING' or tokens[tokenIndex + 1][0] == 'STRING'):
        print("ERROR: Strings can only be added")
        break

      if token[1] == "plus":
        finalValue = num1 + num2
      elif token[1] == "minus":
        finalValue = num1 - num2
      elif token[1] == "times":
        finalValue = num1 * num2
      elif token[1] == "over":
        finalValue = num1 / num2
      else:
        print("ERROR: Invalid math operator")

      tokens[tokenIndex - 1:tokenIndex + 2] = [["STRING", str(finalValue)]]

def execute(tokens):
  preExecute(tokens)

  for tokenIndex, token in enumerate(tokens):
    
    # ==================== VARIABLES ===================
    # Sets variables if the assignment operator is found
    if token[0] == "ASSIGNMENT OPERATOR":
      variableValue = ""

      # Executes if there is only one word in the print statement
      if not (tokenIndex + 2) < len(tokens) or tokens[tokenIndex + 2][0] == "COMMAND" or tokens[tokenIndex + 2][0] == "END":
        variables[tokens[tokenIndex - 1][1]] = tokens[tokenIndex + 1][1]

      else:
        currentlyVariable = False

        # Iterates through tokens to store all words that need to be printed to the printText variable
        for token in tokens:
          if currentlyVariable:
            if token[0] == "END":
              currentlyVariable = False
            else:
              try:
                variableValue += str(token[1]) + " "
              except:
                print("ERROR: Objects of this type cannot be assigned as a variable")
          
          else:
            if token[1] == "is":
              currentlyVariable = True
        
        variables[tokens[tokenIndex - 1][1]] = variableValue

    # ===================== WRITING ====================
    if token[1] == "write":
      printText = ""

      # Checks if there are multiple words in the print statement
      if not (tokenIndex + 2) < len(tokens) or tokens[tokenIndex + 2][0] == "COMMAND" or tokens[tokenIndex + 2][0] == "END":
        printText = tokens[tokenIndex + 1][1]
      
      else:
        currentlyPrinting = False

        # Iterates through tokens to store all words that need to be printed to the printText variable
        for token in tokens:
          if currentlyPrinting:
            if token[0] == "END":
              currentlyPrinting = False
            else:
              try:
                printText += str(token[1]) + " "
              except:
                print("ERROR: Objects of this type cannot be printed")
          
          else:
            if token[1] == "write":
              currentlyPrinting = True

      finalPrintText = []

      for word in re.split("\s", printText):
        printWord = word

        # Checks if word in print text is a variable
        for item in variables.items():
          if item[0] == word:
            printWord = item[1]
        
        finalPrintText.append(printWord)
        
      
      print(' '.join(finalPrintText))

# MAIN CONSOLE LOOP
while consoleOn:
  consoleInput = input("ease >> ");
  preprocessedInput = preprocesser(consoleInput);
  consoleCommand = False

  # Checks if stop word was identified
  if not preprocessedInput:
    consoleOn = False;
    break
  
  # Handles changing modes
  if "change mode" in preprocessedInput:
  
    if "token" in preprocessedInput:
      currentMode = "token"
    elif "parse" in preprocessedInput:
      currentMode = "parse"
    elif "execute" in preprocessedInput:
      currentMode = "execute"
    else:
      print("ERROR: Current mode not recognized")
    
    consoleCommand = True
    print("Mode changed to " + currentMode)
  
  elif "what is current mode" in preprocessedInput:
    print("The current mode is " + currentMode)
  
  # Splits text into tokens
  tokenList = tokenizer(preprocessedInput)

  # Parses through tokens
  parsedText = parser(tokenList)

  # Prints output based on the mode 
  if not consoleCommand:
    if currentMode == "token":
      print(tokenList)

    elif currentMode == "parse":
      print(parsedText)
    
    elif currentMode == "execute":
        # Executes code
        execute(parsedText)
    
    else:
      print("INTERPRETER ERROR: Current mode variable not recognized")

"""
LANGUAGE COMMANDS:
end - ends any command to allow multiple commands per line
write - writes objects to the console ("print" in python)
is - assigns a variable a value ("=" in python)
plus, minus, times, over - math operators ("+", "-", "*", "/" in python)

BUGS:
- When writing, variables only print their latest value, even if it was changed after the write statement

TO-DO:
- Add variable identification in parse mode
- Add if statements
- Add for, while loops

"""