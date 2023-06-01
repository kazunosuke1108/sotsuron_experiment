mat_general=readmatrix("C:\Users\hayashide\kazu_ws\sotsuron_experiment\sotsuron_experiment\results\0117\csv\20230117_d_060_1_Hayashide.csv");
mat=readmatrix("C:\Users\hayashide\kazu_ws\sotsuron_experiment\sotsuron_experiment\matlab_ws\result.csv")

rajc.no=15;
lajc.no=14;

t=mat(:,56);
rajc.mat=[mat(:,rajc.no),mat(:,rajc.no+17),mat(:,rajc.no+17*2)];
lajc.mat=[mat(:,lajc.no),mat(:,lajc.no+17),mat(:,lajc.no+17*2)];

subplot(2,2,1)
plot(t,rajc.mat(:,1),'.')
title("x")

subplot(2,2,2)
plot(t,rajc.mat(:,2),'.')
title("y")

subplot(2,2,3)
plot(t,rajc.mat(:,3),'.')
title("z")

subplot(2,2,4)
plot3(rajc.mat(:,1),rajc.mat(:,2),rajc.mat(:,3))
grid on
daspect([1 1 1])

