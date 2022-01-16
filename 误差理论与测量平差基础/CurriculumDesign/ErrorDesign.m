% 此程序为水准网的间接平差计算和精度评定，可以计算出水准网各线路的平差值和各点的高程平差值
% 并且可以对他们进行精度评定
% 在间接平差过程中，使用点位高程值作为平差值进行计算

% 为使代码界面尽可能地间洁明了，我尽量将注意事项备注在程序代码中，而不在输入提示中显示
% 本程序的输入为从Excel表格中根据提示框选，在matlab界面出确定
% 注意在Excel写入时将已知点号编为点位号前几个，并编完已知的之后再整未知的
% 运行时一定注意查看命令行窗口的提示

% 水准网存储的中间结果在命令行窗口中，最终平差结果在Excel表格中
% 是否超限计算需要在Excel表格中自行设计计算

filename = 'Data.xlsx';

% n为总观测数、t为必要观测数、b为已知点数、c为单位权高差公里数
disp('请依次一次性选择总观测数、必要观测数、已知点数和单位权高差公里数');
numbers=xlsread(filename,-1); 
n=numbers(1);
t=numbers(2);
b=numbers(3); 
c=numbers(4);

% H0按顺序存储已知点高程
disp('请选择已知点高程');
H0=xlsread(filename,-1);

% a按顺序分别存储水准网各路线起点、终点和高差
disp('请选择水准网各路线起点、终点和高差');
a = xlsread(filename,-1);

% s按路线编号存储各路线距离
disp('请选择各路线距离');
s=xlsread(filename,-1);

disp('间接平差模型为v=Bx-l，解得:');

% 求解误差方程中的系数
B=zeros(n,t);

% 测量起始点在误差方程中的系数为-1
for i=1:n
    if(a(i,1)>b && a(i,1)<=(b+t))
        B(i,a(i,1)-b)=-1;
    end
end

% 测量终点在误差方程中的系数为1
for i=1:n
    if(a(i,2)<=(b+t)&&a(i,2)>b)
        B(i,a(i,2)-b)=1;
    end
end

% 已知点没有设参数，在误差方程中的系数为0
for i=1:n
    if(a(i,1)<=b)
        B(i,a(i,1)+b)=0;
    elseif(a(i,2)<=b)
        B(i,a(i,2)+b)=0;
    end
end

% 输出B
B=B(1:n,1:t)

% 求解误差方程中的l
% 首先求解水准网中各点近似高程
H=zeros((b+t),1);

for i=1:b
    H(i,1)=H0(i,1);
end

% 与已知点有联系的高程直接求解
for i=1:n
    if(a(i,1)<=b)
        H(a(i,2),1)=H(a(i,1),1)+a(i,3);
    elseif(a(i,2)<=b)
        H(a(i,1),1)=H(a(i,2),1)-a(i,3);
    end
end

% 求解和已知点没有直接联系的点的高程
for i=1:n
    if(H(a(i,1),1)~=0&&H(a(i,2),1)~=0)
        break;
    elseif(H(a(i,1),1)~=0&&H(a(i,2),1)==0)
        H(a(i,2),1)=H(a(i,1),1)+a(i,3);
    elseif(H(a(i,1),1)==0&&H(a(i,2),1)~=0)
        H(a(i,2),1)=H(a(i,1),1)-a(i,3);
    end
end

% 求解常数阵l
l=zeros(n,1);

for i=1:n
    l(i,1)=H(a(i,2),1)-H(a(i,1),1)-a(i,3);
end
l =-l;

% 输出l
l

% 求解权阵
disp('该水准网的权阵为:')
P=zeros(n,n);
for i = 1 : n
    P(i,i) = c/s(i,1);
end
P

% 求解法方程，法方程系数阵为Nbb，法方程常数项阵为W
disp('间接平差的法方程系数阵和常数项阵分别为:');
Nbb = B' * P * B
W = B' * P * l

% x为法方程的解
disp('法方程的解为:');
x = inv(Nbb) * W

% v为改正数
v = B * x - l;

% hC为各高差平差值
hC = zeros(n,1);
for i = 1 : n
    hC(i,1) = a(i,3)+v(i,1);
end

% HC为各点的高程平差值
HC = zeros((b+t),1);
for i=1:b
    HC(i,1)=H0(i,1);
end

for i=b+1:b+t
    HC(i,1)=H(i,1)+x(i-2,1);
end

% 以下为精度评定过程
disp('下面进行精度评定:');

% r为自由度
r=n-t;

% sigma0为单位权中误差
sigma0 = sqrt(v'*P*v/r);

% Qxx为参数值平差值互协因数阵
disp('参数值平差值互协因数阵为:');
Qxx = inv(Nbb)

% sigmad为各点位高程中误差
sigmad = zeros(b+t,1);
for i = b+1 : b+t
    sigmad(i,1) = sigma0 * sqrt(Qxx(i-b,i-b));
end

% sigma为高差中误差
sigma = zeros(n,1);
for i = 1 : n
    F = B(i,:);
    sigma(i,1) = sqrt(sigma0 * sigma0 * (F * Qxx * F'));
end

% 将结果读入excel表格
xlswrite(filename,["线路序号","观测高差","观测值改正数","高差平差值","高差中误差","单位权中误差","点位序号","高程平差值","高程中误差"],'Result');
xlswrite(filename,[1:n]','Result','A2');
xlswrite(filename,roundn(a(:,3),-4),'Result','B2');
xlswrite(filename,roundn(v,-4),'Result','C2');
xlswrite(filename,roundn(hC,-4),'Result','D2');
xlswrite(filename,roundn(sigma,-4),'Result','E2');
xlswrite(filename,roundn(sigma0,-4),'Result','F2');
xlswrite(filename,[1:b+t]','Result','G2');
xlswrite(filename,roundn(HC,-4),'Result','H2');
xlswrite(filename,roundn(sigmad,-4),'Result','I2');
disp('平差结果和精度评定结果已经在excel文件中显示！');