from typing import Tuple,Literal

def filterText(text: str) -> Tuple[bool, Literal["red","blue","white"]]:
    isThrow = False
    color  = ""

    list = text.split(' ')

    for word in list:
        word = word.lower()
        if word == "throw":
            isThrow = True
        elif word == "red":
            color = "red"
            break
        elif word == "blue":
            color = "blue"
            break
        elif word == "white":
            color = "white"
            break
    
    return (isThrow, color)