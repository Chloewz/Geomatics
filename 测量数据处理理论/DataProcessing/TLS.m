clc;
clear;

% �������ݴ��������뷽��--������С���˻ع飨TLS��
% P114 ��5.10
x=[1 2 6];
y=[2 6 1];
x_mean = mean(x);
y_mean = mean(y);
X=x-x_mean;
Y=y-y_mean;
B=[X' Y'];
N=B'*B;
lambda=diag(eig(N));    % B'B����ֵ
lambda(lambda==0)=[];
lambda_min=min(lambda);

% ���TLS���ֱ��ϵ��
%beta_1=inv((N(1,1)-lambda_min))*N(1,2)
beta_1=N(1,2)/(N(1,1)-lambda_min);
beta_0=y_mean-beta_1*x_mean;

% ��TLS���ֱ��ֱ�۱�ʾ��
t = 1:0.1:30;
k = beta_1*t+beta_0;
plot(x,y,'*');
hold on;
plot(t,k,'DisplayName','TLS���ֱ��');
legend;
fprintf('TLS���ֱ��Ϊ��Y=%3.3f*X+%3.3f',beta_1,beta_0);
