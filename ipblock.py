# -*- coding: utf-8 -*-

import ansck

import sys

def dec2bin(dec : str) -> str:
    if(isinstance(dec, int)):
        dec = str(dec)
    buff = ansck.dec2sn(2, int(dec))
    buff = ansck.letter2num(buff)
    while(len(buff) < 8):
        buff = "0" + buff
    return buff

def bin2dec(bini : str) -> str:
    buff = ansck.num2letter(bini)
    buff = ansck.sn2dec(2, buff)
    buff = str(buff)
    while(len(buff) < 3):
        buff = " " + buff
    return buff

def errorMsg(s : str, typer : int):
    '''
    typer == 1 is Syntax error
    typer == 0 is just msg
    '''
    if(typer == 0):
        res = s + "\n"
    #elif(typer == 1):
    else:
        res = "Syntax error. " + s + ". \n"
    res += "Check README: https://github.com/The220th/ipblock"
    print(res)
    exit()

def getOcts(s : str) -> tuple:
    '''
    255 . 255 . 255 . 255
    oct1 oct2  oct3   oct4

    return (oct1, oct2, oct3, oct4)
    '''
    oct1, oct2, oct3, oct4 = s.split(".")
    if(len(oct1) == 8):
        oct1 = bin2dec(oct1)
    if(len(oct2) == 8):
        oct2 = bin2dec(oct2)
    if(len(oct3) == 8):
        oct3 = bin2dec(oct3)
    if(len(oct4) == 8):
        oct4 = bin2dec(oct4)
    return (int(oct1), int(oct2), int(oct3), int(oct4))

def prefix2mask(prefix : int) -> str:
    '''
    24 -> 255.255.255.0
    '''
    res = ("1"*prefix) + ("0"*(32-prefix))
    return f"{res[0:8]}.{res[8:16]}.{res[16:24]}.{res[24:32]}"

def mask2prefix(mask : str) -> int:
    '''
    255.255.255.0 -> 24
    '''
    masks = mask.split(".")
    res = ""
    for i in masks:
        res += dec2bin(i)
    c = 0
    while(c < 32 and res[c] == '1'):
        c+=1
    return c

def countHosts(prefix : int) -> int:
    if(prefix == 32):
        return 0
    elif(prefix == 31):
        return 2
    else:
        return 2**(32-prefix)-2

def printIP(ips : tuple) -> str:
    t = list(ips)
    for i in range(len(t)):
        t[i] = str(t[i])
        while(len(t[i]) < 3):
            t[i] = " " + t[i]
    return f"{t[0]}.{t[1]}.{t[2]}.{t[3]}"

def printIP_2(t : tuple) -> str:
    return f"{dec2bin(t[0])}.{dec2bin(t[1])}.{dec2bin(t[2])}.{dec2bin(t[3])}"

def ipblockProcess(IP : str, MASK : str):
    octs = getOcts(IP)
    masks = getOcts(MASK)
    for num in (octs+masks):
        if(num > 255 or num < 0):
            errorMsg(f"{num} more than 255", 1)

    for i in masks:
        if(i not in (255, 254, 252, 248, 240, 224, 192, 128, 0)):
            errorMsg(f"The number {i} cannot be in the mask", 1)
    for i in range(1, len(masks)):
        if(masks[i-1] < masks[i]):
            errorMsg("The mask was entered with an mistake", 1)
        if(masks[i] != 255 and masks[i] != 0):
            if(masks[i-1] != 255):
                errorMsg("The mask was entered with an mistake", 1)

    oct1, oct2, oct3, oct4 = octs
    mask1, mask2, mask3, mask4 = masks
    res1, res2, res3, res4 = (oct1 & mask1), (oct2 & mask2), (oct3 & mask3), (oct4 & mask4)
    prefix = mask2prefix(printIP((mask1, mask2, mask3, mask4)))

    print(f"Entered ip: {printIP((oct1, oct2, oct3, oct4))}")
    print(f"        or: {printIP_2((oct1, oct2, oct3, oct4))}")
    print("")
    print(f"Entered mask: {printIP((mask1, mask2, mask3, mask4))}")
    print(f"          or: {printIP_2((mask1, mask2, mask3, mask4))}")
    print(f"          or: /{prefix}")
    print("="*36)
    print("")
    print(printIP((oct1, oct2, oct3, oct4)))
    print(printIP((mask1, mask2, mask3, mask4)))
    print("-"*36)
    print(printIP((res1, res2, res3, res4)))
    print("")
    print(printIP_2((oct1, oct2, oct3, oct4)))
    print(printIP_2((mask1, mask2, mask3, mask4)))
    print("-"*36)
    print(printIP_2((res1, res2, res3, res4)))
    print(f"or {printIP((res1, res2, res3, res4)).replace(' ', '')}/{prefix}")
    print("")
    print(f"Hosts available: {countHosts(prefix)}")

if __name__ == '__main__':
    '''
    > ipblock ip mask
    > ipblock num_ns
    '''
    argc = len(sys.argv)

    if(argc == 2):
        resS = ""
        buff = sys.argv[1]
        if(buff.find("_") == -1):
            errorMsg("Cannot find \"_\"", 1)
        num = buff[:buff.find("_")]
        sn = buff[buff.find("_")+1:]
        sn = int(sn)

        resS += f"{buff} = "

        if(sn == 2):
            resS += bin2dec(num) + "_10"
        elif(sn == 10):
            resS += dec2bin(num) + "_2"
        else:
            errorMsg("Not so the number system. Expected 2 or 10", 1)
        print(resS)
    elif(argc == 3):
        argv1 = sys.argv[1]
        argv2 = sys.argv[2]
        if(argv2[0] == "/"):
            prefix = int(argv2[1:])
            if(prefix < 0 or prefix > 32):
                errorMsg(f"There cannot be such a prefix: {prefix}", 1)
            argv2 = prefix2mask(prefix)
            #print(argv2)
        if(argv1.count(".") != 3):
            errorMsg("IP address is entered incorrectly", 1)
        if(argv2.count(".") != 3):
            errorMsg("Mask is entered incorrectly", 1)
        ipblockProcess(argv1, argv2)
    else:
        errorMsg("Expected: \"ipblock ip mask\" or \"ipblock num_ns\"", 1)