clc;
clear;

% �������ݴ��������뷽��-��С�����˲����ƹ�
% P44 ��3.1

B=[-1,-1;-1,0];
Dyy=[2,0;0,2];
Ddd=[2,0;0,2];
Dyd=[0,-1;0,0];
Muy=[0;0];
L=[1;1];

Y=Muy+(Dyy*B'+Dyd)*inv(Ddd+B*Dyd+Dyd'*B'+B*Dyy*B')*(L-B*Muy)