import re

class FileReadWriter:
    def __init__(self, inputFileName, outputFileName=None):
        self.inputFileName = inputFileName
        self.outputFileName = outputFileName if outputFileName is not None else inputFileName[:-3] + 'obj'
        
        with open(self.inputFileName, 'r') as file:
            # return lines by a list
            # ignore comment
            lines = file.readlines()
            self.lines = [re.sub('[\t]', ' ', line).rstrip() for line in lines if len(line) > 0 and line[0] != '.']

    def get_lines(self):
        return self.lines

    def write_line(self, sentence, append=True):
        file = open(self.outputFileName, 'a' if append else 'w')
        file.write(f'{sentence}\n')
        file.close()