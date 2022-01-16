clc;
clear;
% �������ݴ�������-KalmanFilter

% ��ʼֵ��ѡȡ
n=7;                            % �۲�ֵ����
t=[1 8 15 30 60 120 360];       % �Ա���
x=[111 108 105 100 101 91 80];  % �۲�ֵx
y=[213 207 208 200 194 190 185];% �۲�ֵy
originin=[x; y];                % �ɹ۲�ֵ���ɵľ���[2,n]

% ���״̬����ϵ����
l1=zeros(3,1);l2=zeros(3,1);
b1=zeros(3,3);b2=zeros(3,3);
a=ceil(n/3);b=ceil(2*n/3);  % ȡx=1,x=n/3,x=2n/3,x=n��ֵ���ڽ�ģ

l1(1,1)=x(a-1); l1(2,1)=x(b-1); l1(3,1)=x(n-1);
l2(1,1)=y(a); l2(2,1)=y(b); l2(3,1)=y(n);
b1(1,1)=x(1); b1(2,1)=x(a-1); b1(3,1)=x(b-1);
b2(1,1)=x(1); b2(2,1)=y(a); b2(3,1)=y(b);
b1(1,2)=t(a-1)-t(1); b1(2,2)=t(b-1)-(a-1); b1(3,2)=t(n-1)-t(b-1);
b2(1,2)=t(a)-t(1); b2(2,2)=t(b)-t(a); b2(3,2)=t(n)-t(b);

for i=1:3
    b1(i,3)=b1(i,2)^2;
    b2(i,3)=b1(i,3);
end

disp('״̬����ϵ����Ϊ:');
x1=pinv(b1'*b1)*b1'*l1
x2=pinv(b2'*b2)*b2'*l2

disp('�۲ⷽ��ΪL=BX+V:')
B=[1 0;0 1]

% ��ʼֵ�ļ���
phi=[x1(1) 0;0 x2(1)];  % phi��ת�ƾ���
tau=[x1(2) x1(3);x2(2) x2(3)]*[(t(2)-t(1))/2;((t(2)-t(1))/2)^2];% tau���Ŷ���
x0=(x(1)+x(2))/2;       % ���ߵĳ�ʼֵȡǰ��λ����ƽ��ֵ
y0=(y(1)+y(2))/2;
% x0=mean(x); y0=mean(y);   % ���ߵĳ�ʼֵȡȫ����ƽ��ֵ
X=zeros(2,1);
X(1,1)=x0; X(2,1)=y0;
D_omega=0.1; D_delta=0.04;    % �Լ��涨
Dx=zeros(2,2);
Dx(1,1)=0.025; Dx(2,1)=0.025;

% Kalman�˲�����
% ��ʽ��Դ��P54
L=[x(1);y(1)];
E=zeros(2,2);
S=X+Dx*B'*pinv(B*Dx*B'+D_delta)*(L-B*X);
s=S;    % sΪ��С�����˲����
X=phi*X;
Dx=phi*Dx*phi'+tau*D_omega*tau';    % ���ߵķ�������omegaֵ�ڰ������������(��һ��)
l=L-B*X;    % lΪ����ֵ��ƽ��ֵ֮��,����Ϣ
J=Dx*B'*pinv(B*Dx*B'+D_delta);   % JΪ������󣬼�Ϊ����ֵ�����ֵ+ƽ��ֵ�ķ���֮��
XL=X+J*l; XY=XL;  % XYΪKalman�˲����
DL=(E-J*B)*Dx; d=DL; % ��Э�������

for i=2:n
    % ��С�����˲�ֵ��ȡ
    X=phi*[x(i);y(i)];  % ��״̬���̼���X�Ĺ�ֵ������
    tau=[x1(2:3,1)';x2(2:3,1)']*[(t(i)-t(i-1));(t(i)-t(i-1))^2];
    Dx=phi*Dx*phi'+tau*D_omega*tau';
    S=X+Dx*B'*pinv(B*Dx*B'+D_delta)*(L-B*X);
    s=[s,S];
    
    % Kalman�˲�ֵ��ȡ
    X=phi*XL;
    Dx=phi*Dx*phi'+tau*D_omega*tau';
    L=B*[x(i);y(i)];
    l=L-B*X;
    J=DL*B'*pinv(B*DL*B'+D_delta);
    XL=X+J*l;
    XY=[XY,XL];
    DL=(E-J*B)*Dx;
    d=[d,DL];
    
    if i>n
        break;
    end
end

disp('��С�����˲���ֵSΪ:');
s
disp('Kalman�˲���ѹ�ֵ������Ӧ�ķ���ֵΪ:');
XY
d

% ��ͼֱ����ʾ��С�����˲���Kalman�˲��ıȽ�
plot(t,originin,'^g',t,s,'b--o',t,XY,'r-*');
legend('�۲�ֵx' ,'�۲�ֵy','��С�����˲�ֵx','��С�����˲�ֵy','Kalman�˲�x','Kalman�˲�ֵy');
box on;     % ��ʾ����������
title('�۲�ֵ����С�����˲�ֵ���������˲��������ѹ�ֵ�ķֲ�');
xlabel('ʱ��t');
ylabel('����ֵx��y');

% �����������excel�����
filename='KalmanResult.xlsx';
%xlswrite(filename,["ʱ��","��С�����˲�ֵ","Kalman�˲�ֵ"],'Result');
xlswrite(filename,t,'Result','B2');
xlswrite(filename,s,'Result','B3');
xlswrite(filename,XY,'Result','B5');
%xlswrite(filename,d,'Result','B7');