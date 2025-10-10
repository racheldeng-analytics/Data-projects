clc,clear
x0=[1.952,1.968];
y0=[-2.76856,-2.76856];
x=1.96;
y=lagrange(x0,y0,x);
format long;
disp(y)
function y = lagrange(x0,y0,x)
if length(x0)==length(y0)
    n=length(x0);
else
    disp('原始数据x和y的个数不相等')
    return;
end
y=zeros(size(x));
Num=length(x);
for k=1:Num
    for i=1:n
    for j=1:n
        if i~=j
            t=(x(k)-x0(j))/(x0(i)-x0(j));
        end
    end
    y(k)=y(k)+y0(i)*t;
    end
end
end