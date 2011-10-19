function ftfile=processImage(ft)
%0-999images , 10 classes 。
%0-99,100-199,200-299,.......,900-999
m=1;
n=9;
ftfile=fopen(ft,'a+');
for i=1:m
    %90 images as data set
    for j=1:n
        numofimg=(i-1)*100+(j-1);
        imgname=strcat('~/research/img/',num2str(numofimg),'.jpg');
        ft=glcm(imgname);
        [row,cols]=size(ft);
        fprintf(ftfile,'%d ',i);
        for k=1:cols-1
            fprintf(ftfile,'%f ',ft(k));
        end
        fprintf(ftfile,'%f\n',ft(cols));
    end
end
        
            
            
