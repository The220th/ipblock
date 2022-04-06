# -*- coding: utf-8 -*-

# https://github.com/The220th/ansck

from typing import List
import sys

def sn2dec(suf : int, a : List[int]) -> int:
	'''
	Переводит число `a` из системы счисления `suf` в число в десятичной системе счисления.

	Например:
	>>> sn2dec(2, [1, 0, 0, 1, 1]) # вернёт 25
	>>> sn2dec(3, [1, 0, 1, 1]) # вернёт 37
	>>> sn2dec(123, [1, 16, 0, 15]) # вернёт 27914974
	>>> sn2dec(10, [7, 5, 3]) # вернёт 357

	В аргументе `a` на позиции a[0] стоит самый младший разряд.
	'''
	res = 0
	for i in range(len(a)):
		res += int(a[i]*(suf**i))
	return res

def dec2sn(suf : int, a : int) -> List[int]:
	'''
	Переводит число `a` из десятичной системы счисления в число в системе счисления `suf`.

	Например:
	>>> dec2sn(2, 25) # вернёт [1, 0, 0, 1, 1]
	>>> dec2sn(3, 37) # вернёт [1, 0, 1, 1]
	>>> dec2sn(123, 27914974) # вернёт [1, 16, 0, 15]
	>>> dec2sn(10, 357) # вернёт [7, 5, 3]

	В возвращаемом числе (листе) на позиции 0 находится самый младший разряд.
	'''
	res = []
	while(a // suf != 0):
		res.append(a % suf)
		a = a // suf
	res.append(a % suf)
	return res

def float2dec(suf : int, a : List[int], digNum : int = -1) -> float:
	'''
	Переводит дробную часть `a` из системы счисления `suf` в дробную часть в десятичной системе счисления.
	У дробной части десятичного числа будет `digNum` знаков после запятой.
	По умолчанию параметр функции `digNum` меньше нуля. Это значит, что будет высчитываться максимальное кол-во знаков после запятой.
	
	Чем дальше от запятой, тем точность хуже.

	Например:
	>>> float2dec(5, [1, 2, 3, 4]) # вернёт ~0.3104, так как 0.1234_5 = 0.3104_10
	>>> float2dec(14, [1, 0, 10, 1, 2, 12]) # вернёт ~0.07510422953021276, так как 0.10A12C_14 = 0.07510422953021276_10
	>>> float2dec(14, [1, 0, 10, 1, 2, 12], 8) # вернёт ~0.0.07510423

	В аргументе `a` на позиции a[0] стоит самый младший разряд дробной части.
	'''
	res = 0
	for i in range(1, len(a) + 1):
		res += a[i-1]*(suf**(-(i)))
	if(digNum >= 0):
		s = (f"%.{digNum}f") % res
		res = float(s)
	return res

def dec2float(suf : int, a : float, digNum : int = 10) -> List[int]:
	'''
	Переводит дробную часть `a` из десятичной системы счисления в дробную часть числа в системе счисления `suf`.
	По умолчанию считает примерно 10 знаков после запятой.
	Если нужно больше/меньше знаков после запятой, то задайте соответствующее значение параметра `digNum`.

	Если `a` не меньше единицы, то от `a` отсечётся целая часть.

	Чем дальше от запятой, тем точность хуже.

	Например:
	>>> dec2float(5, 0.9378) # вернёт [4, 3, 2, 1, 0, 3, 0, 3, 0, 3], так как 0.9378_10 = 0.4321030303_5
	>>> dec2float(5, 0.9378, 5) # вернёт [4, 3, 2, 1, 0]
	>>> dec2float(27, 0.43569875698756987) # вернёт [11, 20, 16, 23, 4, 25, 13, 5, 9, 10], так как 0.43569875698756987_10 = 0.BKGN4PD59A_27

	В возвращаемой дробной часте (листе) на позиции 0 находится самый младший разряд.
	'''
	if(a >= 1):
		#raise ValueError(f"{a} must be less, than zero. ")
		a = a - int(a)
	res = []
	for i in range(digNum):
		buff = a*suf
		res.append(int(buff))
		buff -= int(buff)
		a = buff
	return res

def letter2num(a : List[int]) -> str:
	'''
	Переводит число `a` в представлении листа (см. dec2sn) в число в этой системе счисления.

	Например:
	>>> letter2num([15, 12, 8, 2]) # вернёт "29CF"

	Если "букв" больше не "осталось", то вернёт None.
	'''
	res = ""
	for i in range(len(a)):
		if(a[i] < 10):
			res += str(a[i])
		elif(a[i] < 36):
			res += chr(a[i] + 55)
		else:
			return None
	return res[::-1]

def num2letter(a : str) -> List[int]:
	'''
	Переводит число `a`, записанное в определённой системе счисления в число в виде листа (см. sn2dec).
	Такое число съест функция `sn2dec`.

	Например:
	>>> num2letter("29CF") # вернёт [15, 12, 8, 2]
	'''
	res = []
	for c in a:
		if(48 <= ord(c) <= 57):
			res.append(int(c))
		elif(65 <= ord(c) <= 90):
			res.append(ord(c)-55)
		else:
			return None
	return res[::-1]

def syntaxErrorMsg() -> str:
	res = "Syntax error. Check README.md: "
	res += "https://github.com/The220th/ansck/blob/main/README.md"
	return res

def process(suf1 : int, sn : List[int], suf2 : int) -> None:
	global NORMALFORM # https://i.imgur.com/ZQBexZC.png
	if(NORMALFORM == 1):
		origNum = letter2num(sn)
	else:
		origNum = sn[::-1]
	print(f"Entered original number \"{origNum}\" in this numeral system \"{suf1}\"")
	
	decOrigNum = sn2dec(suf1, sn)
	print(f"{origNum}_{suf1} = {decOrigNum}_{10}")

	secondNum_sn = dec2sn(suf2, decOrigNum)

	print("")

	marked1, marked2 = "", ""
	if(NORMALFORM == 1):
		marked1 = "    <------"
	else:
		marked2 = "    <------"

	print(f"{letter2num(sn)}_{suf1} = {letter2num(secondNum_sn)}_{suf2} {marked1}")
	#print("")
	print(f"{sn[::-1]}_{suf1} = {secondNum_sn[::-1]}_{suf2} {marked2}")

def process_dot(suf1 : int, sn_ : List[int], _sn : List[int], suf2 : int) -> None:
	global NORMALFORM
	global DIGNUM
	global DOT
	# https://i.imgur.com/qpLAqvj.png

	if(NORMALFORM == 1):
		origNum_ = letter2num(sn_)
		_origNum = letter2num(_sn)[::-1]
	else:
		origNum_ = sn_[::-1]
		_origNum = _sn
	print(f"Entered original number \"{origNum_}{DOT}{_origNum}\" in this numeral system \"{suf1}\"")
	
	decOrigNum_ = sn2dec(suf1, sn_)
	_decOrigNum = float2dec(suf1, _sn)
	_decOrigNumPrint = str(float2dec(suf1, _sn, DIGNUM))[2:]
	print(f"{origNum_}{DOT}{_origNum}_{suf1} = {decOrigNum_}{DOT}{_decOrigNumPrint}_{10}")

	secondNum_sn_ = dec2sn(suf2, decOrigNum_)
	_secondNum_sn = dec2float(suf2, _decOrigNum, DIGNUM)

	print("")

	marked1, marked2 = "", ""
	if(NORMALFORM == 1):
		marked1 = "    <------"
	else:
		marked2 = "    <------"

	Nonbl9 = letter2num(_sn)
	if(Nonbl9 != None):
		Nonbl9 = Nonbl9[::-1]

	print(f"{letter2num(sn_)}{DOT}{Nonbl9}_{suf1} = {letter2num(secondNum_sn_)}{DOT}{letter2num(_secondNum_sn)[::-1]}_{suf2} {marked1}")
	#print("")
	print(f"{sn_[::-1]}{DOT}{_sn}_{suf1} = {secondNum_sn_[::-1]}{DOT}{_secondNum_sn}_{suf2} {marked2}")

#python snk.py num_suf 2suf [digNum]

if __name__ == '__main__':
	if(len(sys.argv) < 3 or 4 < len(sys.argv)):
		print(syntaxErrorMsg())
		exit()
	if(sys.argv[1].find("_") == -1):
		print(syntaxErrorMsg())
		exit()
	if(len(sys.argv) == 4):
		DIGNUM = int(sys.argv[3])
		if(DIGNUM < 1):
			print(f"{DIGNUM} less than 1")
			exit()
	else:
		DIGNUM = 10

	suf1 = int(  sys.argv[1][sys.argv[1].find("_")+1:]  )
	withoutSuf = sys.argv[1][:sys.argv[1].find("_")]
	suf2 = int(sys.argv[2])

	if(suf1 < 2 or suf2 < 2):
		print(f"({suf1} or {suf2}) less than 2")
		exit()

	NORMALFORM = 0


	if(withoutSuf.count(".") > 1):
		print(syntaxErrorMsg())
		exit()

	if(withoutSuf.count(",") > 1):
		print(syntaxErrorMsg())
		exit()

	# https://i.imgur.com/UpdFhzc.png
	if(withoutSuf.count(",") == 1 or withoutSuf.count(".") == 1):
		if(withoutSuf.count(",") == 1):
			DOT = ","
		elif(withoutSuf.count(".") == 1):
			DOT = "."
		initNum = None
		if(withoutSuf.find("[") == -1):
			dot_pos = withoutSuf.find(".")
			if(dot_pos == -1):
				dot_pos = withoutSuf.find(",")
			initNum_ = withoutSuf[:dot_pos]
			_initNum = withoutSuf[dot_pos+1:]
			initNum_ = num2letter(initNum_)
			_initNum = num2letter(_initNum)[::-1]
			if(initNum_ == None or _initNum == None):
				print("Use only uppercase latin letters")
				exit()
			NORMALFORM = 1
		else:
			if(withoutSuf.find("]") == -1):
				print("Cannot find \"]\"")
				print(syntaxErrorMsg())
				exit()
			# https://i.imgur.com/UzuKq3B.png
			initNum = withoutSuf[withoutSuf.find("[")+1:withoutSuf.find("]")]
			dot_pos = initNum.find(".")
			if(dot_pos == -1):
				dot_pos = initNum.find(",")
			#initNum = initNum.replace(",", " , ")
			initNum_ = list(map(int, initNum[:dot_pos].split()))
			initNum_ = initNum_[::-1]
			_initNum = list(map(int, initNum[dot_pos+1:].split()))

		if(max(_initNum) >= suf1 or max(initNum_) >= suf1):
			print(f"{withoutSuf} cannot be in this numeral system: {suf1}. Because {max(_initNum)} >= {suf1} or {max(initNum_)} >= {suf1}")
			exit()
		process_dot(suf1, initNum_, _initNum, suf2)
	else: # https://i.imgur.com/qqYQcEq.png
		initNum = None
		if(withoutSuf.find("[") == -1):
			initNum = num2letter(withoutSuf)
			if(initNum == None):
				print("Use only uppercase latin letters")
				exit()
			NORMALFORM = 1
		else:
			if(withoutSuf.find("]") == -1):
				print("Cannot find \"]\"")
				print(syntaxErrorMsg())
				exit()
			initNum = withoutSuf[withoutSuf.find("[")+1:withoutSuf.find("]")]
			initNum = list(map(int, initNum.split()))
			initNum = initNum[::-1]

		if(max(initNum) >= suf1):
			print(f"{withoutSuf} cannot be in this numeral system: {suf1}. Because {max(initNum)} >= {suf1}")
			exit()

		process(suf1, initNum, suf2)