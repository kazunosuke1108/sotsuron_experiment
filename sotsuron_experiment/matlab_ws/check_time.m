clc;clear;
mat_general=load("C:\Users\hayashide\kazu_ws\sotsuron_experiment\sotsuron_experiment\matlab_ws\result.csv");
fig=figure();clf;
time_series=mat_general(:,end)-mat_general(1,end)
time_compensated=zeros(size(time_series))
frame_idx=1:length(time_series)
% straight=polyfit(frame_idx,time_series,1)

% histogram(time_series-straight(1).*frame_idx+straight(2),10)
time_compensated(1)=time_series(1);
time_compensated(2)=time_series(2);
for i = 2:length(time_series)-1
    if time_series(i+1)-time_series(i)>2*(time_compensated(i)-time_compensated(i-1))
        time_compensated(i+1)=(time_series(i)-time_series(i-1))*(time_series(i+1)-time_series(i));
    else
        time_compensated(i)=time_series(i)
    end
end

% time_compensated=smoothdata(time_series)
plot(frame_idx,mat_general(:,end)-mat_general(1,end))
hold on
plot(frame_idx,straight(1)*frame_idx)
% plot(1:length(time_compensated),time_compensated-time_compensated(1))
xlabel("frame no.")
ylabel("time [s]")
legend("raw time [s]","compensated time [s]")
saveas(fig,"C:\Users\hayashide\kazu_ws\sotsuron_experiment\sotsuron_experiment\matlab_ws\time_noise.png")