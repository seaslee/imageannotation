#!/usr/bin/env python
'''
  put the color feature file and the texture feature file together,
  the target file is the feature with color and texture
  '''

def link(s1,s2):
    return s1+s2[1:]+'\n'

def linkfile(file1,file2,target):
    f1=open(file1,'r')
    f2=open(file2,'r')
    s1=f1.read()
    s2=f2.read()
    f1.close()
    f2.close()
    l1=s1.split('\n')
    l2=s2.split('\n')
    l3=map(link,l1[:-1],l2[:-1])
    s3=''.join(l3)
    s3.strip()
    f3=open(target,'w')
    f3.write(s3)
    f3.close()

def main():
    linkfile('cft','tft','ft')

if __name__=='__main__':
    main()

