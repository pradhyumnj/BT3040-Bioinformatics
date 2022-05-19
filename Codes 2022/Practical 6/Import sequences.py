import requests as r
from DnaUtils import getFasta, readFasta
set1_ids = ['P69905', 'P01946', 'P01942', 'P01966', 'P01958', 'P01959', 'P01965', 'P06635', 'P60529', 'P80043', 'P01980']
set1 = [getFasta(Id) for Id in set1_ids ]
set2_ids = ['TPIS_HUMAN', 'TPIS_YEAST', 'TPIS_GRAVE', 'TPIS_TRYCR', 'TPIS_MAIZE', 'TPIS_MOUSE', 'TPIS_DROME', 'TPIS_RABIT', 'TPIS_CAEEL']
set2 = [getFasta(Id) for Id in set2_ids ]
open('set1.fasta','w').write('\n'.join(set1))
open('set2.fasta','w').write('\n'.join(set2))
set1_MSA = r.get("https://www.ebi.ac.uk/Tools/services/rest/clustalo/result/clustalo-I20220228-121158-0732-53765895-p1m/aln-clustal")
open("set1_MSA.clustal", 'w').write(set1_MSA.text)
set2_MSA = r.get("https://www.ebi.ac.uk/Tools/services/rest/clustalo/result/clustalo-I20220228-121626-0464-24089352-p1m/aln-clustal_num")
open("set2_MSA.clustal", 'w').write(set2_MSA.text)