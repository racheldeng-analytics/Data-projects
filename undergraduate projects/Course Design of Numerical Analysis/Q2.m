%第一阶段
[t1,y1]=ode45(@Windfun1,[0 40],[0;0]);
% 第二阶段
init1=y1(end,1);
init2=y1(end,2);
[t2,y2]=ode45(@Windfun2,[40 60],[init1;init2]);

% 路程
figure(1)
plot(t1,y1(:,1),'b-',t2,y2(:,1),'k','LineWidth',1.5)
title('h-t图');
xlabel('t');
ylabel('h(t)');
grid on
hold on
[~, y2_mpos] = max(y2);
plot(t2(y2_mpos),y2(y2_mpos),'o','color','r')
hold off

% 速度
figure(2)
plot(t1,y1(:,2),'c',t2,y2(:,2),'r--','LineWidth',1.5);
title('v-t图');
xlabel('t');
ylabel('v(t)');
grid on

%加速度
g=9.8;
m0=1200;
m1=600;
F=27000;
u=15;
k=0.4;
a1=(F-(k.*y1(:,2).*y1(:,2))-(m0-u.*t1).*g)./(m0-u.*t1);
a2=((-k.*y2(:,2).*y2(:,2))-(m0-m1).*g)./(m0-m1);
figure(3)
plot(t1,a1,'g',t2,a2,'y','LineWidth',2)
title('a-t图');
xlabel('t');
ylabel('a(t)');
hold on
line([40 40],[a1(end) a2(1)]);
grid on

function y=Windfun1(t,x)
g=9.8;
m0=1200;
F=27000;
u=15;
k=0.4;
y=[x(2);
    (F-(k.*x(2).*x(2))-(m0-u.*t).*g)./(m0-u.*t)];
end
function y=Windfun2(t,x)
g=9.8;
m0=1200;
m1=600;
k=0.4;
y=[x(2);
    (-k.*(x(2).*x(2))-(m0-m1).*g)./(m0-m1)];
end
