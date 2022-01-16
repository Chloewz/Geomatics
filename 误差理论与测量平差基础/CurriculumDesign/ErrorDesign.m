% �˳���Ϊˮ׼���ļ��ƽ�����;������������Լ����ˮ׼������·��ƽ��ֵ�͸���ĸ߳�ƽ��ֵ
% ���ҿ��Զ����ǽ��о�������
% �ڼ��ƽ������У�ʹ�õ�λ�߳�ֵ��Ϊƽ��ֵ���м���

% Ϊʹ������澡���ܵؼ�����ˣ��Ҿ�����ע�����ע�ڳ�������У�������������ʾ����ʾ
% �����������Ϊ��Excel����и�����ʾ��ѡ����matlab�����ȷ��
% ע����Excelд��ʱ����֪��ű�Ϊ��λ��ǰ��������������֪��֮������δ֪��
% ����ʱһ��ע��鿴�����д��ڵ���ʾ

% ˮ׼���洢���м����������д����У�����ƽ������Excel�����
% �Ƿ��޼�����Ҫ��Excel�����������Ƽ���

filename = 'Data.xlsx';

% nΪ�ܹ۲�����tΪ��Ҫ�۲�����bΪ��֪������cΪ��λȨ�߲����
disp('������һ����ѡ���ܹ۲�������Ҫ�۲�������֪�����͵�λȨ�߲����');
numbers=xlsread(filename,-1); 
n=numbers(1);
t=numbers(2);
b=numbers(3); 
c=numbers(4);

% H0��˳��洢��֪��߳�
disp('��ѡ����֪��߳�');
H0=xlsread(filename,-1);

% a��˳��ֱ�洢ˮ׼����·����㡢�յ�͸߲�
disp('��ѡ��ˮ׼����·����㡢�յ�͸߲�');
a = xlsread(filename,-1);

% s��·�߱�Ŵ洢��·�߾���
disp('��ѡ���·�߾���');
s=xlsread(filename,-1);

disp('���ƽ��ģ��Ϊv=Bx-l�����:');

% ��������е�ϵ��
B=zeros(n,t);

% ������ʼ���������е�ϵ��Ϊ-1
for i=1:n
    if(a(i,1)>b && a(i,1)<=(b+t))
        B(i,a(i,1)-b)=-1;
    end
end

% �����յ��������е�ϵ��Ϊ1
for i=1:n
    if(a(i,2)<=(b+t)&&a(i,2)>b)
        B(i,a(i,2)-b)=1;
    end
end

% ��֪��û����������������е�ϵ��Ϊ0
for i=1:n
    if(a(i,1)<=b)
        B(i,a(i,1)+b)=0;
    elseif(a(i,2)<=b)
        B(i,a(i,2)+b)=0;
    end
end

% ���B
B=B(1:n,1:t)

% ��������е�l
% �������ˮ׼���и�����Ƹ߳�
H=zeros((b+t),1);

for i=1:b
    H(i,1)=H0(i,1);
end

% ����֪������ϵ�ĸ߳�ֱ�����
for i=1:n
    if(a(i,1)<=b)
        H(a(i,2),1)=H(a(i,1),1)+a(i,3);
    elseif(a(i,2)<=b)
        H(a(i,1),1)=H(a(i,2),1)-a(i,3);
    end
end

% ������֪��û��ֱ����ϵ�ĵ�ĸ߳�
for i=1:n
    if(H(a(i,1),1)~=0&&H(a(i,2),1)~=0)
        break;
    elseif(H(a(i,1),1)~=0&&H(a(i,2),1)==0)
        H(a(i,2),1)=H(a(i,1),1)+a(i,3);
    elseif(H(a(i,1),1)==0&&H(a(i,2),1)~=0)
        H(a(i,2),1)=H(a(i,1),1)-a(i,3);
    end
end

% ��ⳣ����l
l=zeros(n,1);

for i=1:n
    l(i,1)=H(a(i,2),1)-H(a(i,1),1)-a(i,3);
end
l =-l;

% ���l
l

% ���Ȩ��
disp('��ˮ׼����Ȩ��Ϊ:')
P=zeros(n,n);
for i = 1 : n
    P(i,i) = c/s(i,1);
end
P

% ��ⷨ���̣�������ϵ����ΪNbb�������̳�������ΪW
disp('���ƽ��ķ�����ϵ����ͳ�������ֱ�Ϊ:');
Nbb = B' * P * B
W = B' * P * l

% xΪ�����̵Ľ�
disp('�����̵Ľ�Ϊ:');
x = inv(Nbb) * W

% vΪ������
v = B * x - l;

% hCΪ���߲�ƽ��ֵ
hC = zeros(n,1);
for i = 1 : n
    hC(i,1) = a(i,3)+v(i,1);
end

% HCΪ����ĸ߳�ƽ��ֵ
HC = zeros((b+t),1);
for i=1:b
    HC(i,1)=H0(i,1);
end

for i=b+1:b+t
    HC(i,1)=H(i,1)+x(i-2,1);
end

% ����Ϊ������������
disp('������о�������:');

% rΪ���ɶ�
r=n-t;

% sigma0Ϊ��λȨ�����
sigma0 = sqrt(v'*P*v/r);

% QxxΪ����ֵƽ��ֵ��Э������
disp('����ֵƽ��ֵ��Э������Ϊ:');
Qxx = inv(Nbb)

% sigmadΪ����λ�߳������
sigmad = zeros(b+t,1);
for i = b+1 : b+t
    sigmad(i,1) = sigma0 * sqrt(Qxx(i-b,i-b));
end

% sigmaΪ�߲������
sigma = zeros(n,1);
for i = 1 : n
    F = B(i,:);
    sigma(i,1) = sqrt(sigma0 * sigma0 * (F * Qxx * F'));
end

% ���������excel���
xlswrite(filename,["��·���","�۲�߲�","�۲�ֵ������","�߲�ƽ��ֵ","�߲������","��λȨ�����","��λ���","�߳�ƽ��ֵ","�߳������"],'Result');
xlswrite(filename,[1:n]','Result','A2');
xlswrite(filename,roundn(a(:,3),-4),'Result','B2');
xlswrite(filename,roundn(v,-4),'Result','C2');
xlswrite(filename,roundn(hC,-4),'Result','D2');
xlswrite(filename,roundn(sigma,-4),'Result','E2');
xlswrite(filename,roundn(sigma0,-4),'Result','F2');
xlswrite(filename,[1:b+t]','Result','G2');
xlswrite(filename,roundn(HC,-4),'Result','H2');
xlswrite(filename,roundn(sigmad,-4),'Result','I2');
disp('ƽ�����;�����������Ѿ���excel�ļ�����ʾ��');