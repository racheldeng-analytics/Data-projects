clear ;  % 清除内存变量
a=0; b=2; h=0.005; c=1;  % 输入参数值
[ T, U ] = trapezoid (a, b, h, c) ;  %调用trapezoid函数
% 绘图
t=0:2;
plot ( t, orig(t), 'b-') 
hold on
plot( T, U, 'r--')
hold off
title('梯形法');
xlabel('T');
ylabel('U');
legend ( '精确解', '数值解') ;
Rate=log(9.848e-08/4.64405e-07)/log(0.005/0.0025);
disp(Rate);
function  r = f (t, u)
r = -99*u+(100*cos(t)-sin(t))*exp(t);
end
function  r = orig (t)
r =exp(t).*cos(t);
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



