clc;
clear;

% 测量数据处理理论与方法--整体最小二乘回归（TLS）
% P114 例5.10
x=[1 2 6];
y=[2 6 1];
x_mean = mean(x);
y_mean = mean(y);
X=x-x_mean;
Y=y-y_mean;
B=[X' Y'];
N=B'*B;
lambda=diag(eig(N));    % B'B特征值
lambda(lambda==0)=[];
lambda_min=min(lambda);

% 求解TLS拟合直线系数
%beta_1=inv((N(1,1)-lambda_min))*N(1,2)
beta_1=N(1,2)/(N(1,1)-lambda_min);
beta_0=y_mean-beta_1*x_mean;

% 将TLS拟合直线直观表示出
t = 1:0.1:30;
k = beta_1*t+beta_0;
plot(x,y,'*');
hold on;
plot(t,k,'DisplayName','TLS拟合直线');
legend;
fprintf('TLS拟合直线为：Y=%3.3f*X+%3.3f',beta_1,beta_0);
