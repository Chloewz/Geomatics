clc;
clear;

% 测量数据处理理论与方法-最小二乘滤波与推估
% P44 例3.1

B=[-1,-1;-1,0];
Dyy=[2,0;0,2];
Ddd=[2,0;0,2];
Dyd=[0,-1;0,0];
Muy=[0;0];
L=[1;1];

Y=Muy+(Dyy*B'+Dyd)*inv(Ddd+B*Dyd+Dyd'*B'+B*Dyy*B')*(L-B*Muy)