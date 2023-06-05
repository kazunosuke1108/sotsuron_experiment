clc;clear;
mat_general=load("C:\Users\hayashide\kazu_ws\sotsuron_experiment\sotsuron_experiment\matlab_ws\result.csv");
fig=figure();clf;
plot(1:length(mat_general),mat_general(:,end)-mat_general(1,end))
xlabel("frame no.")
ylabel("time [s]")
saveas(fig,"C:\Users\hayashide\kazu_ws\sotsuron_experiment\sotsuron_experiment\matlab_ws\time_noise.png")