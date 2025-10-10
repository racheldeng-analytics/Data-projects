clear ;  % 清除内存变量
a=0; b=2; h=0.016; c=1;  % 输入参数值
[ T, U ] = RK (a, b, h, c) ;  %调用RK函数
% 绘图
t=0:2;
plot ( t, orig(t), 'b-') 
hold on
plot( T, U, 'r--')
hold off
title('R-K法');
xlabel('T');
ylabel('U');
legend ( '精确解', '数值解') ;
Rate=log(1.08255e-06/6.02422e-08)/log(0.005/0.0025);
disp(Rate);
m=sum(U);
disp(m)
function  r = f (t, u)
r = -99*u+(100*cos(t)-sin(t))*exp(t);
end
function  r = orig (t)
r =exp(t).*cos(t);
end
function  [ T, U ] =RK (a, b, h, c)   % c= y0
n = round ((b-a)/h) + 1 ;  % 计算点的个数
t = zeros (n, 1) ;   % 设定 t 维数
u = zeros (n, 1) ;   % 设定 u 维数
t(1) = a ;
u(1) = c ;    % 初始条件
str = sprintf ('x0=%g, y0=%g \ n', t(1), u(1));
disp (str);    % 显示初始条件
for i=1: n-1
    K1=f(t(i),u(i));
    K2=f(t(i)+h/2,u(i)+h/2*K1);
    K3=f(t(i)+h/2,u(i)+h/2*K2);
    K4=f(t(i)+h,u(i)+h*K3);
      u(i+1)=u(i)+h/6*(K1+2*K2+2*K3+K4);
      t(i+1)=t(i)+h ;
      str= sprintf ('%d   t= %g   u= %g   e= %g',     i , t(i+1), u(i+1), abs(u(i+1) - orig(t(i+1)))) ;
   disp (str);       % 显示计算结果与误差
end
T = t ;   
U = u ; % 返回计算结果
end
