import os


def vasp(n):
    os.system('mpirun -np '+str(n)+' vasp')
    return True

def readEnergy():
    fin=open('OSZICAR','r')
    energy=float(fin.read().split('F=')[-1].split('E0')[0])  # 'F=' e 'E0' are used as separators. See OSZICAR.
    fin.close()
    return energy

def readTime():
    fin=open('OUTCAR','r')
    time=float(fin.read().split('Total CPU time used (sec):')[-1].split('\n')[0])  
    fin.close()
    return time

def readMemory():
    fin=open('OUTCAR','r')
    memory=float(fin.read().split('Maximum memory used (kb):')[-1].split('\n')[0])  
    fin.close()
    return memory


def makePOSCAR(interlayer1,interlayer2,interlayer3):
    fposcar=open('POSCAR','w')
    
    fposcar.write('Mo2 S4 - homobilayer AA stacking\n0.99\n3.1903157234 0.0000000000 0.0000000000\n-1.5951578617 2.7628944626  0.0000000000\n0.0000000000 0.0000000000 25.56927055\n')
    fposcar.write('Mo S\n2 4\nSelective dynamics\nCartesian\n0.000000000 1.841929697 3.719750881 F F F\n0.000000000 1.841929697 '+str(interlayer2)+' F F F\n1.595157909 0.920964848 5.284635273 F F F\n1.595157909  0.920964848 '+str(interlayer1)+' F F F\n1.595157909 0.920964848 2.154866490 F F F\n1.595157909 0.920964848 '+str(interlayer3)+' F F F')
    fposcar.close()
    return True

#Mo2 S4 - homobilayer AA stacking
#0.99
#3.1903157234 0.0000000000 0.0000000000
#-1.5951578617 2.7628944626  0.0000000000
#0.0000000000 0.0000000000 25.56927055
#Mo S
#2 4
#Selective dynamics
#Cartesian
#0.000000000 1.841929697 3.719750881 F F F
#0.000000000 1.841929697 11.159252644 F F F
#1.595157909 0.920964848 5.284635273 F F F
#1.595157909  0.920964848 12.724137035 F F F
#1.595157909 0.920964848 2.154866490 F F F
#1.595157909 0.920964848 9.594368252 F F F


#Parameter 1
interlayer1_ini=10.71440406
interlayer1_end=12.51440406
interlayer1_step=0.1
fout=open('results-interlayer-convergence','w')

#Parameter 2
interlayer2_ini=9.149419665
interlayer2_end=10.94941967
interlayer2_step=0.1

#Parameter 3
interlayer3_ini=7.584635273
interlayer3_end=9.384635273
interlayer3_step=0.1

#Initializing main loop
interlayer1=interlayer1_ini
interlayer2=interlayer2_ini
interlayer3=interlayer3_ini
while interlayer1<interlayer1_end and interlayer2<interlayer2_end and interlayer3<interlayer3_end:
    makePOSCAR(interlayer1,interlayer2,interlayer3)
    vasp(8)
    energy=readEnergy()
    time=readTime()
    memory=readMemory()
    fout.write(str(interlayer1)+' '+str(interlayer2)+' '+str(interlayer3)+' '+str(energy)+' '+ str(time)+' '+ str(memory)+'\n')
    
    interlayer1+=interlayer1_step
    interlayer2+=interlayer2_step
    interlayer3+=interlayer3_step

fout.close()
