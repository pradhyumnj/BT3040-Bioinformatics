class Dna:
    """Contains helper functions for DNA strings"""
    def __init__(self, strand, type = 'coding'):
        import re
        strand = strand.upper()
        self._complement = {'A' : 'T', 'T' : 'A', 'G' : 'C', 'C' : 'G'}
        if type == 'coding':
            self._strand = strand
        elif type == 'template':
            self._strand = ''.join([self._complement[s] for s in strand])

        file = open('codon.txt')
        string = file.read()
        bank = re.findall("[A-z]{3}\s[A-z]{1,4}",string)
        bank = dict([tuple(x.split(' ')) for x in bank])
        self._codon = bank

    def __repr__(self):
        return self._strand
    
    def __len__(self):
        "Get length of Strand"
        return len(self._strand)
    
    def __getitem__(self,k):
        "Get Base at index k"
        return Dna(self._strand[k])

    def complement(self):
        """Return the complement of the DNA strand"""
        return Dna(''.join([self._complement[s] for s in self._strand]))
    
    def revComplement(self):
        """Return the reverse complement of the DNA strand"""
        return self.complement()[::-1]

    def transcribe(self):
        """Transcribe the DNA strand"""
        return Dna(self._strand.replace('T', 'U'))
    
    def translate(self):
        """Translate the DNA strand"""
        mRna = str(self.transcribe())
        protein = ''.join([self._codon[mRna[i:i+3]] for i in range(0,len(mRna),3)])
        return protein
    
    def splice(self, intron):
        """Splice the introns from the DNA strand"""
        self._strand = self._strand.replace(intron,'')
    
    def start(self):
        """Return the index of start codons"""
        import re
        return [x.start() for x in re.finditer('AUG', str(self.transcribe()))]
    
    def stop(self):
        """Return the index of stop codons"""
        import re
        return [x.start() for x in re.finditer('UAA|UAG|UGA', str(self.transcribe()))]
    
    def ORF(self):
        """Return the open reading frame of the DNA strand (use RevComplement for its ORF)"""
        ofs = []
        start = self.start()
        stop = self.stop()
        for i in start:
            for j in stop:
                if j > i and (j-i) % 3 == 0 and [x for x in stop if x > i and x < j and (x-i) % 3 == 0] == []:
                    ofs.append((i,j))
        return ofs
        
    def find(self, seq):
        """Return indices (start,stop) where seq is found in strand"""
        import re
        return [(i.start(), i.end()) for i in re.finditer(seq, self._strand)]
    
    def count(self, base):
        """Returns number of occourences of a base in the strand"""
        return self._strand.count(base)
    
    
    
    
    
    
    

########################### x--x-x-x-x-x-x-x-x-x-x--x-x-x--x-x-x-x-x-x-x-x-x-x-x--x-x-x-x-x-x-x--x-x-x-x-x-x--x-x-x-x-x--x-x-x-x-x-x--x ############
    
    
def readFasta(fileName , type = 'File'):
    """Function to quickly read FASTA files. Returns (ids,sequences)"""
    if type == "File":
        file = open(fileName)
        s = file.read()
    elif type == 'String':
        s = fileName
        
    sequences = []
    ids = []
    sequence = ''
    for line in s.split('\n'):
        if len(line) == 0:
            continue
        if line[0] == '>':
            ids.append(line)
            sequences.append(sequence)
            sequence = ''
            pass
        else:
            sequence += line
    sequences.append(sequence)
    sequences = [x.replace('\n','') for x in sequences if x != '']
    return ids, sequences

########################### x--x-x-x-x-x-x-x-x-x-x--x-x-x--x-x-x-x-x-x-x-x-x-x-x--x-x-x-x-x-x-x--x-x-x-x-x-x--x-x-x-x-x--x-x-x-x-x-x--x ############

#Constants

codon = Dna("A")._codon

revCodon = {}
for (code, protein) in codon.items():
    if protein in revCodon:
        revCodon[protein].append(code)
    else:
        revCodon[protein] = [code]

file = open('protein_mass.txt')
s = file.read()
protein_mass = {protein : float(mass) for protein, mass in [line.split('   ') for line in s.splitlines()]}