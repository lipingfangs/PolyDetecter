import os
import sys

refindex = sys.argv[1]
refindexfa = sys.argv[2]
inputwholefa = sys.argv[3]

def split_fasta_file(input_file, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_basename = os.path.splitext(os.path.basename(input_file))[0]

    sequences = []
    with open(input_file, "r") as input_file:
        lines = input_file.readlines()
        header, sequence = None, []
        for line in lines:
            line = line.strip()
            if line.startswith(">"):
                if header is not None:
                    sequences.append((header, ''.join(sequence)))
                header = line
                sequence = []
            else:
                sequence.append(line)
        if header is not None:
            sequences.append((header, ''.join(sequence)))

    for idx, (header, sequence) in enumerate(sequences, start=1):
        output_filename = f"{output_basename}_{idx}.fasta"
        output_path = os.path.join(output_dir, output_filename)

        with open(output_path, "w") as output_file:
            output_file.write(header + "\n")
            output_file.write(sequence + "\n")
            
split_fasta_file(inputwholefa, inputwholefa+"_tempdir")

inputfadir = inputwholefa+"_tempdir"
listfile = os.listdir(inputfadir)

for filefasta in listfile:
    inputfa = filefasta
    os.system(f"bwa mem -o {inputfa}.sam {refindex} {inputfadir}/{inputfa}  > /dev/null 2>&1" )
    
    inputfafile = open(f"{inputfa}.sam","r")
    inputfafileline = inputfafile.readlines()
    inputfafile.close()

    refindexfaonlyfile = open(refindexfa,"r")
    refindexfafileonlyline = refindexfaonlyfile.readlines()
    refindexfaonlyfile.close()

    #print(f"bwa mem -o {inputfa}.sam {refindex} {inputfadir}/{inputfa}  > /dev/null 2>&1")
   # os.system(f"bwa mem -o {inputfa}.sam {refindex} {inputfadir}/{inputfa}  > /dev/null 2>&1" )

    fafile = open(f"{inputfadir}/{inputfa}","r")
    fafileline = fafile.readlines()
    fafile.close()
   
    print(fafileline[0].strip(),end = "\t" )
    print(fafileline[1].strip(),end = "\t" )
    vari = ["S","D","M","I","H"]
    numacc = 0
    varilist = []

    for i in refindexfafileonlyline:
        i = i.strip()
        if i.startswith(">"):
            continue
        else:
            refseq = i
    #print(refseq)       
    numacc = ""        
    for i in inputfafileline:
        if i.startswith("@"):
            continue
        else:
            i = i.split()
            stp = int(i[3])
            cig = i[5]
            poiacc = stp
            readacc = 0
           # print("i[9]",i[9])
            for j in cig:
                if j in vari:

                    numaccv = int(numacc)

                    if j == "S" or j == "H":
                        readacc += numaccv
                       # continue
                    if j == "M":
                        count = 0
                        #print(numacc,str(readacc),str(readacc+numaccv),i[9][readacc:readacc+numaccv])
                        for k,r in zip(list(refseq[poiacc-1:poiacc+numaccv-1]),list(i[9][readacc:readacc+numaccv])):
                            count+=1
                            if k !=r:
                                print(str(poiacc+count-1),"Snp",f"{k}/{r}",end = "\t")
                        poiacc += numaccv    
                        readacc += numaccv
                    if j == "D":
                        print(str(poiacc),"Del",str(numacc),end = "\t")
                        poiacc += numaccv

                    if j == "I":
                        print(str(poiacc),"Ins",str(numacc),end = "\t")
                        readacc += numaccv

                    numacc = ""    
                else:
                    #print(j)
                    numacc +=j
    print()
    os.system(f"rm {inputfa}.sam")
