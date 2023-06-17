clc;clear;close all
mat_general=readmatrix("C:\Users\hayashide\kazu_ws\sotsuron_experiment\sotsuron_experiment\results\20230605\csv\20230107_rotation_16_03_yoshinari.csv");
mat=readmatrix("C:\Users\hayashide\kazu_ws\sotsuron_experiment\sotsuron_experiment\matlab_ws\result_yoshinari.csv")
labelList=getLabel();
r.no=15;
l.no=14;

% [~,ind] = sort(mat(:,end));
% mat= mat(ind,:);
% t=mat(:,56)-mat(1,56)
t=fixTimeBug(mat);
r.mat=[mat(:,r.no),mat(:,r.no+17),mat(:,r.no+17*2)]
l.mat=[mat(:,l.no),mat(:,l.no+17),mat(:,l.no+17*2)];


fig=figure(1);
fig.Position = [100 100 1200 800];
% plot(1:length(t),t)

subplot(2,2,1)
plot(t,r.mat(:,1),"r")
hold on
grid
plot(t,l.mat(:,1),"b")
title(labelList(r.no))
xlabel("time \it{t}\rm [s]",'FontName','Times New Roman')
ylabel("x position \it{x}\rm [m]",'FontName','Times New Roman')
legend(labelList(r.no),labelList(l.no))

subplot(2,2,2)
plot(t,r.mat(:,2),"r")
hold on
grid
plot(t,l.mat(:,2),"b")
title(labelList(r.no+17))
xlabel("time \it{t}\rm [s]",'FontName','Times New Roman')
ylabel("y position \it{y}\rm [m]",'FontName','Times New Roman')
legend(labelList(r.no+17),labelList(l.no+17))

subplot(2,2,3)
plot(t,r.mat(:,3),"r")
hold on
grid
plot(t,l.mat(:,3),"b")
title(labelList(r.no+17*2))
xlabel("time \it{t}\rm [s]",'FontName','Times New Roman')
ylabel("z position \it{z}\rm [m]",'FontName','Times New Roman')
legend(labelList(r.no+17*2),labelList(l.no+17*2))

subplot(2,2,4)
plot(r.mat(:,1),r.mat(:,2),"r")
hold on
plot(l.mat(:,1),l.mat(:,2),"b")
% plot3(r.mat(:,1),r.mat(:,2),r.mat(:,3))
grid on
obsv_idx=find(mat(:,53)==max(mat(:,53)))
rbt_position=plot(mat(obsv_idx,52),mat(obsv_idx,53),"ob");
xlim([-6,6])
ylim([0,5])
daspect([1 1 1])
xlabel("position \it{x}\rm [m]",'FontName','Times New Roman')
ylabel("position \it{y}\rm [m]",'FontName','Times New Roman')
% zlabel("position \it{z}\rm [m]",'FontName','Times New Roman')

% saveas(fig,"C:\Users\hayashide\kazu_ws\sotsuron_experiment\sotsuron_experiment\matlab_ws\"+"time_noise.png")
saveas(fig,"C:\Users\hayashide\kazu_ws\sotsuron_experiment\sotsuron_experiment\matlab_ws\"+"yoshinari_"+labelList(r.no)+"_timeFixed.png")