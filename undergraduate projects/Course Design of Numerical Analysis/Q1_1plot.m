clear ;  % 清除内存变量
a=0; b=2; h=0.01; c=1;  % 输入参数值
[ T1, U1 ] = euler (a, b, h, c) ;  %调用Euler函数
[ T2, U2 ] = eu (a, b, h, c) ;
[ T3, U3 ] = trapezoid (a, b, h, c) ;
[ T4, U4 ] = RK (a, b, h, c) ;
% 绘图
t=0:2;
plot ( t, orig(t), 'b-') 
hold on
plot( T1, U1, 'r*')
plot( T2, U2, 'g*')
plot( T3, U3, 'k--')
plot( T4, U4, 'y+')
hold off
title('四种解法与精确解的比较');
xlabel('T');
ylabel('U');
legend ( '精确解', 'Euler法','改进Euler法','梯形法','四阶R-K法') ;
function  r = f (t, u)
r = -99*u+(100*cos(t)-sin(t))*exp(t);
end
function  r = orig (t)
r =exp(t).*cos(t);
end
function  [ T, U ] = euler (a, b, h, c)   % c= y0
n = round ((b-a)/h) + 1 ;  % 计算点的个数
t = zeros (n, 1) ;   % 设定 t 维数
u = zeros (n, 1) ;   % 设定 u 维数
t(1) = a ;
u(1) = c ;    % 初始条件
for i=1: n-1
      u(i+1)=u(i)+h*f(t(i), u(i)) ;
      t(i+1)=t(i)+h ;
end
T = t ;   
U = u ; % 返回计算结果
end
function  [ T, U ] = eu (a, b, h, c)   % c= y0
n = round ((b-a)/h) + 1 ;  % 计算点的个数
t = zeros (n, 1) ;   % 设定 t 维数
u = zeros (n, 1) ;   % 设定 u 维数
t(1) = a ;
u(1) = c ;    % 初始条件
for i=1: n-1
      K1=f(t(i), u(i)) ;
      t(i+1)=t(i)+h ;
      K2=f(t(i+1),u(i)+h*K1);
      u(i+1)=u(i)+h/2*(K1+K2);
end
T = t ;   
U = u ; % 返回计算结果
end
function [ T, U ] = trapezoid (a, b, h, c)
    n = round ((b-a)/h) + 1 ;  % 计算点的个数
t = zeros (n, 1) ;   % 设定 t 维数
u = zeros (n, 1) ;   % 设定 u 维数
t(1) = a ;
u(1) = c ;    % 初始条件
str = sprintf ('x0=%g, y0=%g \ n', t(1), u(1));
disp (str);    % 显示初始条件

    for i = 1:n
        t(i+1) = t(i) + h;
        u(i+1) = calculate(u(i), t(i), c, h, f(t(i),u(i)));
        str= sprintf ('%d   t= %g   u= %g   e= %g',     i , t(i+1), u(i+1), abs(u(i+1) - orig(t(i+1)))) ;
   disp (str);       % 显示计算结果与误差
    end
    T = t ;   
U = u ; % 返回计算结果
end
function result = calculate(u0, t1, u1, h, f0)
    acc = -6;
    now = 0.0;
    z1 = u1;
    while now >= acc
        z0 = z1;
        f1 = -99*z0+(100*cos(t1+h)-sin(t1+h))*exp(t1+h);
        z1 = u0 + h/2*(f0+f1);
        now = log10(abs(z1-z0));
    end
    result = z1;
end
function  [ T, U ] =RK (a, b, h, c)   % c= y0
n = round ((b-a)/h) + 1 ;  % 计算点的个数
t = zeros (n, 1) ;   % 设定 t 维数
u = zeros (n, 1) ;   % 设定 u 维数
t(1) = a ;
u(1) = c ;    % 初始条件
for i=1: n-1
    K1=f(t(i),u(i));
    K2=f(t(i)+h/2,u(i)+h/2*K1);
    K3=f(t(i)+h/2,u(i)+h/2*K2);
    K4=f(t(i)+h,u(i)+h*K3);
      u(i+1)=u(i)+h/6*(K1+2*K2+2*K3+K4);
      t(i+1)=t(i)+h ;
end
T = t ;   
U = u ; % 返回计算结果
end