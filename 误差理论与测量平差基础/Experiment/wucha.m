n=input('总观测数=');
t=input('必要观测数=');
b=input('已知高程点数=');
H0=input('已知点的高程=');
a=input('输入始点、终点、观测值');
disp('间接平差模型为v=Bx-l，解得:');

% 求解误差方程中的系数
B=zeros(n,t);

% 测量起始点在误差方程中的系数为-1
for i=1:n
    if(a(i,1)<=n)
        B(i,a(i,1))=-1;
    end
end

% 测量终点在误差方程中的系数为1
for i=1:n
    if(a(i,2)<=n)
        B(i,a(i,2))=1;
    end
end

% 已知点没有设参数，在误差方程中的系数为0
for i=1:n
    if(a(i,1)>t && a(i,1)<=(b+t))
        B(i,a(i,1))=0;
    elseif(a(i,2)>t && a(i,2)<=(b+t))
        B(i,a(i,2))=0;
    end
end

% 输出B
B=B(1:n,1:t)

% 求解误差方程中的l
% 首先求解水准网中各点近似高程
H=zeros((b+t),1);

for i=1:b
    H((t+i),1)=H0(i,1);
end

% 与已知点有联系的高程直接求解
for i=1:n
    if(a(i,1)>=(t+1)&&a(i,1)<=(b+t))
        H(a(i,2),1)=H(a(i,1),1)+a(i,3);
    elseif(a(i,2)>=(t+1)&&a(i,2)<=(b+t))
        H(a(i,1),1)=H(a(i,2),1)-a(i,3);
    end
end

% 求解和已知点没有直接联系的点的高程
for i=1:n
    if(H(a(i,1),1)~=0&&H(a(i,2),1)==0)
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

% 输出l
l



