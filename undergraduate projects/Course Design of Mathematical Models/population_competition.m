function [t, N1, N2] = populationcompetition(app,r1, r2, K1, K2, s1, s2, N10, N20, t0, tf, dt)
    
    %   r1: 甲种群的增长率
    %   r2: 乙种群的增长率
    %   K1: 甲种群的容量
    %   K2: 乙种群的容量
    %   s1: 甲种群个体的生存能力
    %   s2: 乙种群个体的生存能力
    %   N10: 甲种群初始数量
    %   N20: 乙种群初始数量
    %   t0: 初始时间
    %   tf: 终止时间
    %   dt: 时间步长
    %   t: 时间
    %   N1: 甲种群数量
    %   N2: 乙种群数量


    t = t0:dt:tf;
    N1 = zeros(1, length(t));
    N2 = zeros(1, length(t));
    N1(1) = N10;
    N2(1) = N20;

    
    for i = 1:length(t)-1
        N1(i+1) = N1(i) + dt * r1 * N1(i) * (1 - N1(i)/K1 - s1 * N2(i)/K2);
        N2(i+1) = N2(i) + dt * r2 * N2(i) * (1 - N2(i)/K2 - s2 * N1(i)/K1);
    end
    plot(app.UIAxes2,t, N1, t, N2, 'LineWidth', 2)

    legend(app.UIAxes2,'x种群数量', 'y种群数量');
end

