#!/usr/bin/env python
import sys
'''
    to format the file to adapt to the 
    svmlib .
    label index1:feature1 index1:feature1 ....
    '''

def svmfileformat(source1,target1):
    f=open(source1)
    s=f.read()
    f.close()
    lines=s.split('\n')[:-1]
    nlines=''
    for line in lines:
        ll=line.split()
        nline=ll[0]
        for i in range(1,len(ll)):
            nline+=' '+str(i)+':'+ll[i]
        nline+='\n'
        nlines+=nline
    t=open(target1,'w')
    t.write(nlines)
    t.close()

if __name__=='__main__':
    source1=sys.argv[1]
    target1=sys.argv[2]
    svmfileformat(source1,target1)

