function ft=glcm(imgname)
format long
tic
img=imread(imgname);
gimg=rgb2gray(img);
%quantilize the gray level 
gl=16;
gimg=gimg/(256/gl);
gm=zeros(gl,gl,4);
%computer the glcm 
d=1;
[rows,cols]=size(gimg);
for i=1:gl
	for j=1:gl
		for k=1:rows
            for l=1:cols
                if gimg(k,l)==i &(((l-d)>=1&gimg(k,l-d)==j)|((l+d)<=cols&gimg(k,l+d)==j))
                    gm(i,j,1)=gm(i,j,1)+1;
                end
                if gimg(k,l)==i &(((k-d)>=1&(l+d)<=cols&gimg(k-d,l+d)==j)|((k+d)<=rows&(l-d)>=1&gimg(k+d,l-d)==j))
                    gm(i,j,2)==gm(i,j,2)+1;
                end
                if gimg(k,l)==i &(((k-d)>=1&gimg(k-d,l)==j)|((k+d)<=rows&gimg(k+d,l)==j))
                    gm(i,j,3)=gm(i,j,3)+1;
                end
                if gimg(k,l)==i &(((k-d)>=1&(l-d)>=1&gimg(k-d,l-d)==j)|((k+d)<=rows&(l+d)<=cols&(gimg(k+d,l+d))==j))
                    gm(i,j,4)=gm(i,j,4)+1;
                end
            end
        end
    end
end

%normalize the matrices
for i=1:4
    isum=sum(sum(gm(:,:,i)));
    if isum>0
        gm(:,:,i)=gm(:,:,i)/isum;
    end
end
%computer E H I C L
E=zeros(1,4);
for i=1:4
    E(i)=sum(sum(gm(:,:,i).^2));
end
H=zeros(1,4);
epsilon=0.0001;
for i=1:4
    H(i)=-sum(sum(gm(:,:,i).*log(epsilon+gm(:,:,i))));
end
I=zeros(1,4);
mux=I;
muy=I;
deltax=I;
deltay=I;
for i=1:4
    [r,c]=size(gm(:,:,i))
    for m=1:r
        for n=1:c
          I(i)=I(i)+((m-n)^2)*gm(m,n,i);
          mux(i)=mux(i)+m*gm(m,n,i);
          muy(i)=muy(i)+n*gm(m,n,i);
        end
    end
end
C=zeros(1,4)
for i=1:4
    %tmp=gm(:,:,i)';
    %row=sum(tmp);
    %mux=mean(row);
    %deltax=std(row);
    %col=sum(gm(:,:,i));
    %muy=mean(col);
    %deltay=std(col);
    isum=0;
    [r,c]=size(gm(:,:,i));
    for m=1:r
        for n=1:c
          deltax(i)=deltax(i)+(m-mux(i))^2*gm(m,n,i);
          deltay(i)=deltay(i)+(n-muy(i))^2*gm(m,n,i);
          isum=isum+m*n*gm(m,n,i);
        end
    end
    delta=deltax(i)*deltay(i);
    if delta>0
        C(i)=((isum-mux(i)*muy(i))/delta);
    end
end
L=zeros(1,4);
for i=1:4
    [m,n]=size(gm(:,:,i));
    for m=1:r
        for n=1:c
          L(i)=L(i)+gm(m,n,i)/(1+(m-n)^2);
        end
    end
end
ft=zeros(1,10);
ft(1)=mean(E);
ft(2)=std(E);
ft(3)=mean(H);
ft(4)=std(H);
ft(5)=mean(I);
ft(6)=std(I);
ft(7)=mean(C);
ft(8)=std(C);
ft(9)=mean(L);
ft(10)=mean(L);
toc
