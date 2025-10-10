clear ;  % 清除内存变量
a=0; b=2; h=0.0025; c=1;  % 输入参数值
[ T, U ] = eu (a, b, h, c) ;  
% 绘图
t=0:2;
plot ( t, orig(t), 'b-') 
hold on
plot( T, U, 'r--')
hold off
title('advanced Euler法');
xlabel('T');
ylabel('U');
legend ( '精确解', '数值解') ;
Rate=log(0.000111092/2.38649e-05)/log(0.005/0.0025);
disp(Rate);
function  r = f (t, u)
r = -99*u+(100*cos(t)-sin(t))*exp(t);
end
function  r = orig (t)
r =exp(t).*cos(t);
end
function  [ T, U ] = eu (a, b, h, c)   % c= y0
n = round ((b-a)/h) + 1 ;  % 计算点的个数
t = zeros (n, 1) ;   % 设定 t 维数
u = zeros (n, 1) ;   % 设定 u 维数
t(1) = a ;
u(1) = c ;    % 初始条件

str = sprintf ('x0=%g, y0=%g \ n', t(1), u(1));
disp (str);    % 显示初始条件
for i=1: n-1
      K1=f(t(i), u(i));
      t(i+1)=t(i)+h;
      K2=f(t(i+1),u(i)+h*K1);
      u(i+1)=u(i)+h/2*(K1+K2);
      
      str= sprintf ('%d   t= %g   u= %g   e= %g',     i , t(i+1), u(i+1), abs(u(i+1) - orig(t(i+1)))) ;
   disp (str);       % 显示计算结果与误差
end
T = t ;   
U = u ; % 返回计算结果
end
