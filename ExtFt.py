#!/usr/bin/env python
import cv
import numpy as np
from time import clock
#--------------------------------------
#author xuxinchao 
#Email  xxinchao st gmail dot com
#University sdu
#--------------------------------------

class  ExtractFeature:
    ''' this class is mainly supply methods to extract 
    features from the image , the return result is histogram .
    1)Color feature.
    2)Texture feature.
    '''
    def __init__(self,src,ftfile):
        #self.image=path+imgname
        #self.src=cv.LoadImageM(self.image)
        self.src=src
        self.hist=None
        self.cft=[0]*72#color feature vector
        self.tft=[0]*10
        self.ftfile=ftfile

    def qhsv(self,val):
        h=2*val[0]
        s=val[1]/255
        v=val[2]/255
        #transform h
        if h>315 or h<=20:
            h=0
        elif h>20 and h<=40:
            h=1
        elif h>40 and h<75:
            h=2
        elif h>75 and h<155:
            h=3
        elif h>155 and h<190:
            h=4
        elif h>190 and h<270:
            h=5
        elif h>270 and h<295:
            h=6
        else:
            h=7
        #transform s
        if s>=0 and s<0.2:
            s=0
        elif s>=0.2 and s<0.8:
            s=1
        else:
            s=2
        #transform v
        if v>=0 and v<0.2:
            v=0
        elif v>=0.2 and v<0.8:
            v=1
        else:
            v=2
        return (h,s,v)

    def extColorFeature(self,colorsp):
        if colorsp=='hsv':
            hsv=cv.CreateMat(self.src.rows,self.src.cols,cv.CV_8UC3)
            # rgb color transform to hsv , note it is BGR
            cv.CvtColor(self.src,hsv,cv.CV_BGR2HSV)
            # quantization 
            quan=cv.CreateImage(cv.GetSize(hsv),8,1)
            ftisum=0
            for x in range(hsv.rows):
                for y in range(hsv.cols):
                    val=hsv[x,y]
                    qval=self.qhsv(val)
                    quan[x,y]=int(9*qval[0]+3*qval[1]+qval[2])
                    fti=int(quan[x,y])
                    self.cft[fti]+=1
                    ftisum+=1
            # normalize the feature vector 
            for i in range(len(self.cft)):
                self.cft[i]=float(self.cft[i])/ftisum
            bins=8*3*3
            ranges=[0,71]
            self.hist=cv.CreateHist([bins],cv.CV_HIST_ARRAY,[ranges],1)
            cv.CalcHist([quan],self.hist,0,None)
            #"-------------------------------------------------
            #draw the hist
            maxvalue=cv.GetMinMaxHistValue(self.hist)[1]
            hist_img=cv.CreateImage((400,400),cv.IPL_DEPTH_8U,3)
            cv.SetZero(hist_img)
            bin_width=float(hist_img.width)/bins
            bin_unit=float(hist_img.height)/maxvalue
            for b in range(bins):
                binv=cv.QueryHistValue_1D(self.hist,b)
                p1=(int(b*bin_width),hist_img.height)
                p2=(int((b+1)*bin_width),hist_img.height-int(binv*bin_unit))
                cv.Rectangle(hist_img,p1,p2,cv.Scalar(255,0,0),-1,8,0)
            return hist_img
        else:
            print 'ERROR:PLEASE USE HSV!!'
            return None

    def qgray(self,val):
        #linear transform ,may improve
        unit=256/16
        return val/unit

    def calchmat(self,i,j,d,mat):
        count=0
        for k in range(mat.rows):
            for l in range(mat.cols):
                if l>=d and l<(mat.cols-d) and mat[k,l]==i and (mat[k,l-d]==j or mat[k,l+d]==j):
                        count+=1
        return count

    def calcrdmat(self,i,j,d,mat):
        count=0
        for k in range(mat.rows):
            for l in range(mat.cols):
                if k>=d and k<(mat.rows-d) and l>=d and l<(mat.cols-d)\
                    and mat[k,l]==i and (mat[k-d,l+d]==j or mat[k+d,l-d]):
                        count+=1
        return count

    def calcvmat(self,i,j,d,mat):
        count=0
        for k in range(mat.rows):
            for l in range(mat.cols):
                if k>=d and k<(mat.rows-d) and mat[k,l]==i and (mat[k-d,l]==j or mat[k+d,l]==j):
                        count+=1
        return count

    def calcldmat(self,i,j,d,mat):
        count=0
        for k in range(mat.rows):
            for l in range(mat.cols):
                if k>=d and k<(mat.rows-d) and l>=d and l<(mat.cols-d)\
                    and mat[k,l]==i and (mat[k-d,l-d]==j or mat[k+d,l+d]==j):
                        count+=1
        return count
    
    def calSum(self,mat,rows,cols):
        isum=0
        for i in range(rows):
            for j in range(cols):
                isum+=((i-j)**2)*mat[i,j]
        return isum

    def calCl(self,mat,rows,cols):
        #ux
        r=np.zeros(rows)
        for (i,ele) in enumerate(mat):
            r[i]=np.sum(ele)
        mux=np.mean(r)
        deltax=np.std(r)
        #uy
        c=np.zeros(cols)
        for i in range(rows):
            for j in range(cols):
                c[j]+=mat[i,j]
        muy=np.mean(c)
        deltay=np.std(c)
        isum=0
        for i in range(rows):
            for j in range(cols):
                isum+=i*j*mat[i,j]
        delta=deltax*deltay
        #print 'isum %f ,mux %f ,muy %f ,deltax %f ,deltay %f'%(isum,mux,muy,deltax,deltay)
        if delta>0:
            iresult=(isum-mux*muy)/delta
        else:
            iresult=0
        return iresult

    def calL(self,mat,rows,cols):
        isum=0
        for i in range(rows):
            for j in range(cols):
                isum+=mat[i,j]/(1+(i-j)**2)
        return isum

    def extTextureFeature(self):
        #transform from color image to gray image
        grayim=cv.CreateMat(self.src.rows,self.src.cols,cv.CV_8UC1)
        cv.CvtColor(self.src,grayim,cv.CV_BGR2GRAY)
        #quantilize the gray level
        for x in range(grayim.rows):
            for y in range(grayim.cols):
                grayim[x,y]=self.qgray(grayim[x,y])
        #gray-tone dependence matrices
        qlevel=16
        d=1
        hmat=np.zeros((qlevel,qlevel))#0 ,16*16
        rdmat=np.zeros((qlevel,qlevel))#45
        vmat=np.zeros((qlevel,qlevel))#90
        ldmat=np.zeros((qlevel,qlevel))#135
        #compute the gray-tone dependence matrices
        for i in range(qlevel):
            for j in range(qlevel):
                hmat[i,j]=self.calchmat(i,j,d,grayim) #0
                rdmat[i,j]=self.calcrdmat(i,j,d,grayim)#45
                vmat[i,j]=self.calcvmat(i,j,d,grayim)#90
                ldmat[i,j]=self.calcldmat(i,j,d,grayim)#135
        #normalize the matrices
        hmat/=np.sum(hmat)
        rdmat/=np.sum(rdmat)
        vmat/=np.sum(vmat)
        ldmat/=np.sum(ldmat)
        #Get E,H,I,C,l 
        e=np.zeros(4)
        e[0]=np.sum(hmat**2)
        e[1]=np.sum(rdmat**2)
        e[2]=np.sum(vmat**2)
        e[3]=np.sum(ldmat**2)
        h=np.zeros(4)
        epsilon=0.0001
        h[0]=-np.sum(hmat*np.log(hmat+epsilon))
        h[1]=-np.sum(rdmat*np.log(rdmat+epsilon))
        h[2]=-np.sum(vmat*np.log(vmat+epsilon))
        h[3]=-np.sum(ldmat*np.log(ldmat+epsilon))
        i=np.zeros(4)
        i[0]=self.calSum(hmat,16,16)
        i[1]=self.calSum(rdmat,16,16)
        i[2]=self.calSum(vmat,16,16)
        i[3]=self.calSum(ldmat,16,16)
        c=np.zeros(4)
        c[0]=self.calCl(hmat,16,16)
        c[1]=self.calCl(rdmat,16,16)
        c[2]=self.calCl(vmat,16,16)
        c[3]=self.calCl(ldmat,16,16)
        l=np.zeros(4)
        l[0]=self.calL(hmat,16,16)
        c[1]=self.calL(rdmat,16,16)
        c[2]=self.calL(vmat,16,16)
        c[3]=self.calL(ldmat,16,16)
        #get the mean and the standard deviations as texture feature
        self.tft[0]=np.mean(e)
        self.tft[1]=np.std(e)
        self.tft[2]=np.mean(h)
        self.tft[3]=np.std(h)
        self.tft[4]=np.mean(i)
        self.tft[5]=np.std(i)
        self.tft[6]=np.mean(c)
        self.tft[7]=np.std(c)
        self.tft[8]=np.mean(l)
        self.tft[9]=np.std(l)
    
    def writeFeature(self,label):
        self.extColorFeature('hsv')
        self.extTextureFeature()
        line=''
        line+=str(label)
        ft=self.cft+self.tft
        for (i,ele) in enumerate(ft):
            svmele=' '+str(i)+':'+str(ele)
            line+=svmele
        line+='\n'
        self.ftfile.writelines(line)

def main():
    src=cv.LoadImageM('/home/seaslee/1.jpg')
    ftfile=open('ft','a')
    ext=ExtractFeature(src,ftfile)
    start=clock()
    ext.writeFeature(1)
    t=clock()-start
    print 'time is %f'%t


if __name__=='__main__':
    main()
