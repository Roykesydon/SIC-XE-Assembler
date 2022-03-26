import re

class OpcodeParser:
    def __init__(self, inputFileName):
        self.inputFileName = inputFileName

        with open(self.inputFileName, 'r') as file:
            lines = file.readlines()
            self._lines = [re.sub('[\t]', ' ', line).strip() for line in lines if len(line) > 0 and line[0] != '.']
            self._lines = [ line.split() for line in self._lines]
            self.OPTAB = dict([
                (   
                    line[0], 
                    {
                        'oprandCount': len(line[1].split(',')) if len(line) > 3 else 0,
                        'format': line[-2],
                        'opcode': line[-1]
                    }
                )
                for line in self._lines ])
    
    def get_OPTAB(self):
        return self.OPTAB


if __name__ == '__main__':
    opcodeParser = OpcodeParser('./OPTAB')
    print(opcodeParser.OPTAB)