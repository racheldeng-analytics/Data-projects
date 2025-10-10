e=0;
j=2;
h=0.016;
n=(j-e)/h;
w=10^(-6);
t1=(h/2)*(-3.07513+1);
a=0; b=2; h=0.016; c=1;  % 输入参数值
[ T, U ] = RK (a, b, h, c) ;  %调用RK函数
h1=sum(U);
while(1)
        h1=81.560855787335356;
   h1=h1*h;
    t2=(1/2)*(t1+h1);
        if (abs(t2-t1))<w
        break;
    else
        t1=t2;
    end
end
disp('Tn的值为:');
disp(t1);
disp('等分数为:');
disp(n/2);
H=0:0.0005:10;
H1=log(H);
R=-1/12*H.^2*(-2)*exp(1)*sin(1);
r=log(R);
disp(r)
x=-5:0.5:5;
y=2*x;
plot(r,H1)
hold on;
plot(y,x,'--');
xlabel('步长对数')
ylabel('绝对误差对数')
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
