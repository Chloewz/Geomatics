% 使用分块求逆的方法解算法方程
N=input('法方程系数阵=');
n=input('法方程系数阵为n*n的方阵,其中n=');

A11=N(1,1);
A12=N(1,2:n);
A21=N(2:n,1);
A22=N(2:n,2:n);

B22=inv(A22-A21*inv(A11)*A12);
B12=-inv(A11)*A12*B22;
B21=-inv(A22-A21*inv(A11)*A12)*A21*inv(A11);
B11=inv(A11)-inv(A11)*A12*B21;

fprintf('法方程系数阵为:')
B=[B11 B12;B21 B22]