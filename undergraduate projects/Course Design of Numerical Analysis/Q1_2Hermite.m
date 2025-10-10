x=[0.96,0.976];
y=[1.4978,1.48698];
y1=[-0.6357,-0.7049];
y=Hermitezi(x,y,y1,0.97)
function y=Hermitezi(X,Y,Y1,x)
% 2n+1次Hermite插值函数
%   X为已知数据点的x坐标
%   Y为已知数据点的y坐标
%   Y1为数据点y值导数
%   x0为插值点的x坐标
if(length(X) == length(Y))
    if(length(X) == length(Y1))
        n=length(X);
    else
        disp('y和y的导数维数不相等');
        renturn;
    end
  else
    disp('x和y的维数不相等');
    return;
end
%以上为输入判断和确定“n”的值
m=length(x);
for t=1:m
    z=x(t);s=0.0;
  for i=1:n
    h=1.0;
    a=0.0;
    for j=1:n
        if(j~= i)
            h=h*(z-X(j))^2/((X(i)-X(j))^2);%求得值为(li(x))^2
            a=a+1/(X(i)-X(j));   %求得ai（x）表达式之中的累加部分
        end
    end
   s=s+h*((X(i)-z)*(2*a*Y(i)-Y1(i))+Y(i));
  end
y(t)=s;
end
end
