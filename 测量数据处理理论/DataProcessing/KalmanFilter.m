clc;
clear;
% 测量数据处理理论-KalmanFilter

% 初始值的选取
n=7;                            % 观测值个数
t=[1 8 15 30 60 120 360];       % 自变量
x=[111 108 105 100 101 91 80];  % 观测值x
y=[213 207 208 200 194 190 185];% 观测值y
originin=[x; y];                % 由观测值构成的矩阵[2,n]

% 求解状态方程系数阵
l1=zeros(3,1);l2=zeros(3,1);
b1=zeros(3,3);b2=zeros(3,3);
a=ceil(n/3);b=ceil(2*n/3);  % 取x=1,x=n/3,x=2n/3,x=n处值用于建模

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

disp('状态方程系数阵为:');
x1=pinv(b1'*b1)*b1'*l1
x2=pinv(b2'*b2)*b2'*l2

disp('观测方程为L=BX+V:')
B=[1 0;0 1]

% 初始值的计算
phi=[x1(1) 0;0 x2(1)];  % phi是转移矩阵
tau=[x1(2) x1(3);x2(2) x2(3)]*[(t(2)-t(1))/2;((t(2)-t(1))/2)^2];% tau是扰动项
x0=(x(1)+x(2))/2;       % 二者的初始值取前两位数的平均值
y0=(y(1)+y(2))/2;
% x0=mean(x); y0=mean(y);   % 二者的初始值取全部的平均值
X=zeros(2,1);
X(1,1)=x0; X(2,1)=y0;
D_omega=0.1; D_delta=0.04;    % 自己规定
Dx=zeros(2,2);
Dx(1,1)=0.025; Dx(2,1)=0.025;

% Kalman滤波计算
% 公式来源书P54
L=[x(1);y(1)];
E=zeros(2,2);
S=X+Dx*B'*pinv(B*Dx*B'+D_delta)*(L-B*X);
s=S;    % s为最小二乘滤波结果
X=phi*X;
Dx=phi*Dx*phi'+tau*D_omega*tau';    % 二者的方差与其omega值于白噪声方差相关(后一项)
l=L-B*X;    % l为估计值与平差值之差,即新息
J=Dx*B'*pinv(B*Dx*B'+D_delta);   % J为增益矩阵，即为估计值与估计值+平差值的方差之比
XL=X+J*l; XY=XL;  % XY为Kalman滤波结果
DL=(E-J*B)*Dx; d=DL; % 其协方差矩阵

for i=2:n
    % 最小二乘滤波值求取
    X=phi*[x(i);y(i)];  % 由状态方程计算X的估值及方差
    tau=[x1(2:3,1)';x2(2:3,1)']*[(t(i)-t(i-1));(t(i)-t(i-1))^2];
    Dx=phi*Dx*phi'+tau*D_omega*tau';
    S=X+Dx*B'*pinv(B*Dx*B'+D_delta)*(L-B*X);
    s=[s,S];
    
    % Kalman滤波值求取
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

disp('最小二乘滤波的值S为:');
s
disp('Kalman滤波最佳估值及其相应的方差值为:');
XY
d

% 绘图直观显示最小二乘滤波与Kalman滤波的比较
plot(t,originin,'^g',t,s,'b--o',t,XY,'r-*');
legend('观测值x' ,'观测值y','最小二乘滤波值x','最小二乘滤波值y','Kalman滤波x','Kalman滤波值y');
box on;     % 显示坐标区轮廓
title('观测值、最小二乘滤波值、卡尔曼滤波求出的最佳估值的分布');
xlabel('时间t');
ylabel('距离值x、y');

% 将结果输入至excel表格中
filename='KalmanResult.xlsx';
%xlswrite(filename,["时间","最小二乘滤波值","Kalman滤波值"],'Result');
xlswrite(filename,t,'Result','B2');
xlswrite(filename,s,'Result','B3');
xlswrite(filename,XY,'Result','B5');
%xlswrite(filename,d,'Result','B7');