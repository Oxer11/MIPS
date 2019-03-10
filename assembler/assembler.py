# -*- coding: UTF-8 -*-

import re
import os
import sys

reg = ['0', 'at', 'v0', 'v1', 'a0', 'a1', 'a2', 'a3', 't0', 't1', 't2', 't3', 't4', 't5', 't6', 't7', 's0', 's1', 's2', 's3', 's4', 's5', 's6', 's7', 't8', 't9', 'k0', 'k1', 'gp', 'sp', 'fp', 'ra']
RType = ['sll', 0, 'srl', 'sra', 'sllv', 0, 'srlv', 'srav', 'jr', 'jalr', 0, 0, 'syscall', 'break', 0, 0, 'mfhi', 'mthi', 'mflo', 'mtlo', 0, 0, 0, 0, 'mult', 'multu', 'div', 'divu', 0, 0, 0, 0, 'add', 'addu', 'sub', 'subu', 'and', 'or', 'xor', 'nor', 0, 0, 'slt', 'sltu']
Shift = ['sll', 'srl']
IType = {'beq':4, 'bne':5, 'blez':6, 'bgtz':7, 'addi':8, 'addiu':9, 'slti':10, 'sltiu':11, 'andi':12, 'ori':13, 'xori':14, 'lui':15, 'mul':28, 'lb':32, 'lh':33, 'lw':35, 'lbu':36, 'lhu':37, 'sb':40, 'sh':41, 'sw':43, 'lwcl':49, 'swcl':56}
JType = {'j':2, 'jal':3}

os.chdir(os.getcwd() + '/' + sys.argv[1])
FileList = os.listdir(os.getcwd())
print(FileList)

def HEX(number, length):
	if number < 0:
		number += 1 << length
	ans = hex(number)
	return ans[2:len(ans)].rjust(length, '0')

def BIN(number, length):
	if number < 0:
		number += 1 << length
	ans = bin(number)
	return ans[2:len(ans)].rjust(length, '0')

def Disassembler(InputFile, OutputFile):
	labels = {}
	PC = 0
	lines = InputFile.readlines(100000)
	for line in lines:
		sep = line.find(':')
		if sep != -1: 
			labels[line[0:sep].strip()] = PC
		sep = line.find(' ')
		cmd = line[0:sep].strip()
		if (cmd in RType) or (cmd in IType) or (cmd in JType):
			PC += 4
		
	print(labels)
	
	PC = 0	
	for line in lines:
		result = ''
		now = line

		sep = line.find(' ')
		cmd = line[0:sep].strip()
		if cmd in RType:
			line = line[sep+1:len(line)].strip()
			sep = line.find(',')
			reg1 = line[1:sep].strip()
			line = line[sep+1:len(line)].strip()
			sep = line.find(',')
			reg2 = line[1:sep].strip()
			line = line[sep+1:len(line)].strip()
			if cmd not in Shift:
				reg3 = line[1:len(line)].strip()
				result = '000000' + BIN(reg.index(reg2), 5) + BIN(reg.index(reg3), 5) + BIN(reg.index(reg1), 5) + '00000' + BIN(RType.index(cmd), 6)
			else:
				result = '000000' + '00000' + BIN(reg.index(reg2), 5) + BIN(reg.index(reg1), 5) + BIN(int(line.strip()), 5) + BIN(RType.index(cmd), 6)			
		
		elif cmd in IType:
			line = line[sep+1:len(line)].strip()
			sep = line.find(',')
			reg1 = line[1:sep].strip()
			line = line[sep+1:len(line)].strip()
			sep = line.find(',')
			reg2 = line[1:sep].strip()
			line = line[sep+1:len(line)].strip()
			if line in labels:
				imm = labels[line]
			else:
				imm = int(line, base = 0)
			if cmd in ['beq', 'bne']:
				imm = (imm - PC - 4) >> 2;
			result = BIN(IType[cmd], 6) + BIN(reg.index(reg2), 5) + BIN(reg.index(reg1), 5) + BIN(imm, 16)
			
		elif cmd in JType:
			result = BIN(JType[cmd], 6)
			line = line[sep+1:len(line)].strip()
			if line in labels:
				result += BIN(labels[line] >> 2, 26)
			else:
				result += BIN(int(line, base = 0), 26)
		
		if result == '' and sys.argv[3] == '0': continue
		if sys.argv[2] == 'hex' and result != '':
			result = HEX(int(result, base = 2), 8)
		if sys.argv[3] == '1':
			result = hex(PC).rjust(4) + ' : ' + now.strip().ljust(20) + ' | ' + result
		print(result)
		OutputFile.write(result+'\n')
		if (cmd in RType) or (cmd in IType) or (cmd in JType):
			PC += 4

for File in filter(lambda s: True if s.find('.in') != -1 else False, FileList):
	print(File)
	InputFile = open(File, 'r')
	OutputFile = open(File[0:len(File)-3] + '.out', 'w')
	Disassembler(InputFile, OutputFile)
	InputFile.close()
	OutputFile.close()

