#!/usr/bin/env python
import cv
import sys
#--------------------------------------
#author xuxinchao 
#Email  xxinchao st gmail dot com
#University sdu
#--------------------------------------

class  ExtractFeature:
    ''' this class is mainly supply methods to extract 
    features from the image , the return result is histogram .
    1)Color feature.
    2)
    '''
    def __init__(self,path,imgname):
        self.image=path+imgname
        self.src=cv.LoadImageM(self.image)
        self.hist=None
        self.ft=[0]*72

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
            for x in range(hsv.rows):
                for y in range(hsv.cols):
                    val=hsv[x,y]
                    qval=self.qhsv(val)
                    quan[x,y]=int(9*qval[0]+3*qval[1]+qval[2])
                    fti=int(quan[x,y])
                    self.ft[fti]+=1
            #cv.ShowImage('cv',quan)
            #cv.WaitKey()
            bins=8*3*3
            ranges=[0,71]
            self.hist=cv.CreateHist([bins],cv.CV_HIST_ARRAY,[ranges],1)
            cv.CalcHist([quan],self.hist,0,None)
            maxvalue=cv.GetMinMaxHistValue(self.hist)[1]
            #"-------------------------------------------------
            #draw the hist
            hist_img=cv.CreateImage((400,400),cv.IPL_DEPTH_8U,3)
            cv.SetZero(hist_img)
            bin_width=float(hist_img.width)/bins
            bin_unit=float(hist_img.height)/maxvalue
            for b in range(bins):
                binv=cv.QueryHistValue_1D(self.hist,b)
                p1=(int(b*bin_width),hist_img.height)
                p2=(int((b+1)*bin_width),hist_img.height-int(binv*bin_unit))
                cv.Rectangle(hist_img,p1,p2,cv.Scalar(255,0,0),-1,8,0)
                print b,binv
            return hist_img
        else:
            print 'ERROR:PLEASE USE HSV!!'
            return None
def main():
    ext=ExtractFeature('/home/seaslee/','lenna.jpg')
    h=ext.extColorFeature('hsv')
    for e in ext.ft:
        print e,
    cv.ShowImage('hsv hist',h)
    cv.WaitKey()

if __name__=='__main__':
    main()
