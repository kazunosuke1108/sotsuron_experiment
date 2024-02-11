% theory_check master.m
clear; close all; clc;
omg=5;
xi=0.1;
robot_system=tf(100,[1,2*xi*omg,omg^2]);

%% 極と零点の図示
figure(1)
pzmap(robot_system), grid, legend();

%% bode線図
figure(2)
bode(robot_system),grid,legend();
[gpeak,fpeak] = getPeakGain(robot_system);
%% step応答
figure(3)
step(robot_system),grid,legend();
xlabel("time [s]")
ylabel("y(t)")

%% sin波応答
for i =0.1:0.1:10
    figure(4)
    t=0:0.001:10;
    freq_h=i;
    freq_l=0.1;
    input=sin(2*pi*freq_h*t);%+sin(2*pi*freq_l*t);
    lsim(robot_system,input,t),title(i),grid,legend();
end