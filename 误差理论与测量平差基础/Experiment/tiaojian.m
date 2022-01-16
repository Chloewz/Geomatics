% hg存储高差观测值
hg = input('请输入各高差观测值，以分号间隔: ');

% b为标志数组
b = input('请输入标志数组, 与线路相同的为正, 相反为负');

% h存储高差观测值, 已知点高程
disp('请按编号依次输入各观测值和已知高程，数据未知用0代替。 路线相反需将观测值前代负号。已知高程线路末端也需要带负号: ');
h = input('请输入: ');

% S存储水准路线距离
S = input('请输入各水准路线的距离: ');

% n为总观测数，t为必要观测数，r为多余观测数
n = input('总观测数为：');
t = input('必要观测数为：');
r = n - t;

% A为改正数方程系数阵
A = zeros(r, n);
for i = 1 : r
    for j = 1 : n
        if (h(i,j) ~= 0 && b(1,j) > 0)
            A(i, j) = 1;
        elseif (h(i,j) ~=0 && b(1,j) < 0)
            A(i, j) = -1;
        else 
            A(i, j) = 0;
        end
    end
end
A

% w为改正数方程中的常数项
w = zeros(r, 1);
for i = 1 : r
    w(i, 1) = sum(h(i,:));
end
w

% c为单位权观测高差公里数
c = input('单位权观测高差公里数为: ');

% Q为权因数阵，由于水准测量各观测之间独立，因此Q为对角阵
Q = zeros(n, n);
for i = 1 : n
    Q(i, i) = S(1, i) / c;
end
Q

%　Naa为法方程系数阵
Naa = A * Q * A';
Naa

% K为联系数阵
K = -inv(Naa) * w;

% V为改正数阵
V = Q * A' * K;
V

% hp为平差值方程
hp = zeros(n, 1);
hp = hg + V;
hp
