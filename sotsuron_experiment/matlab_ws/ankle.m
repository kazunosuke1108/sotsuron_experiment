mat_general=readmatrix("C:\Users\hayashide\kazu_ws\sotsuron_experiment\sotsuron_experiment\results\0117\csv\20230117_d_060_1_Hayashide.csv");
mat=readmatrix("C:\Users\hayashide\kazu_ws\sotsuron_experiment\sotsuron_experiment\matlab_ws\result.csv")
labelList=getLabel();
rajc.no=15;
lajc.no=14;

% [~,ind] = sort(mat(:,end));
% mat= mat(ind,:);
t=mat(:,56)-mat(1,56)
rajc.mat=[mat(:,rajc.no),mat(:,rajc.no+17),mat(:,rajc.no+17*2)]
lajc.mat=[mat(:,lajc.no),mat(:,lajc.no+17),mat(:,lajc.no+17*2)];


fig=figure();clf;
% plot(1:length(t),t)

subplot(2,2,1)
plot(t,rajc.mat(:,1))
hold on
plot(t,lajc.mat(:,1))
title(labelList(rajc.no))
xlabel("time \it{t}\rm [s]",'FontName','Times New Roman')
ylabel("x position \it{x}\rm [m]",'FontName','Times New Roman')

subplot(2,2,2)
plot(t,rajc.mat(:,2))
hold on
plot(t,lajc.mat(:,2))
title(labelList(rajc.no+17))
xlabel("time \it{t}\rm [s]",'FontName','Times New Roman')
ylabel("y position \it{y}\rm [m]",'FontName','Times New Roman')

subplot(2,2,3)
plot(t,rajc.mat(:,3))
hold on
plot(t,lajc.mat(:,3))
title(labelList(rajc.no+17*2))
xlabel("time \it{t}\rm [s]",'FontName','Times New Roman')
ylabel("z position \it{z}\rm [m]",'FontName','Times New Roman')

subplot(2,2,4)
plot3(rajc.mat(:,1),rajc.mat(:,2),rajc.mat(:,3))
grid on
daspect([1 1 1])
xlabel("position \it{x}\rm [m]",'FontName','Times New Roman')
ylabel("position \it{y}\rm [m]",'FontName','Times New Roman')
zlabel("position \it{z}\rm [m]",'FontName','Times New Roman')

% saveas(fig,"C:\Users\hayashide\kazu_ws\sotsuron_experiment\sotsuron_experiment\matlab_ws\"+"time_noise.png")
saveas(fig,"C:\Users\hayashide\kazu_ws\sotsuron_experiment\sotsuron_experiment\matlab_ws\"+labelList(rajc.no)+".png")