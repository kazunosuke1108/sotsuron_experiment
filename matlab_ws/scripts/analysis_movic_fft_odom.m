%% initialize
clc;clear;
format long;
set(groot,'DefaultAxesFontName',  'Times New Roman');

%% load data
odom_data=readmatrix("C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/_2023-12-21-10-22-39/_2023-12-21-10-22-39_od_raw.csv",'Delimiter',',');
[unique_timestamps, idx] = unique(odom_data(:, 1));
unique_odo_data = odom_data(idx, :);

%% extract data
timestamp_start=1703121800;
timestamp_end=timestamp_start+4;
data=unique_odo_data(unique_odo_data(:,1)>=timestamp_start-1,:);
data=data(data(:,1)<=timestamp_end+1,:);

%% resample_data
resample_hz=100;
resample_dt=1/resample_hz;
resmaple_time_array=timestamp_start-1:resample_dt:timestamp_end+1;

resampled_data=zeros(length(resmaple_time_array),size(data,2));
for idx = 1:size(resampled_data,2)
    resampled_data(:,idx)=interp1(data(:,1),data(:,idx),resmaple_time_array);
end
resampled_data=resampled_data(resampled_data(:,1)>=timestamp_start,:);
resampled_data=resampled_data(resampled_data(:,1)<=timestamp_end,:);

%% get velocity
diff_data=zeros([length(resampled_data),size(resampled_data,2)-1]);
diff_data(2:end,:)=diff(resampled_data(:,2:end))/resample_dt;
resampled_data_with_velocity=[resampled_data,diff_data];

%% plot timeseries data
fig_timeseries=figure();clf;
plot(resampled_data_with_velocity(:,1),resampled_data_with_velocity(:,2));
hold on; grid on;
plot(resampled_data_with_velocity(:,1),resampled_data_with_velocity(:,3));
plot(resampled_data_with_velocity(:,1),resampled_data_with_velocity(:,4));
plot(resampled_data_with_velocity(:,1),resampled_data_with_velocity(:,5));
% legend({"x [m]","y[m]","\theta [rad]","\phi [rad]"})
xlabel("Time [s]")
ylabel("Position")
yyaxis right
plot(resampled_data_with_velocity(:,1),resampled_data_with_velocity(:,6));
hold on; grid on;
plot(resampled_data_with_velocity(:,1),resampled_data_with_velocity(:,7));
plot(resampled_data_with_velocity(:,1),resampled_data_with_velocity(:,8));
plot(resampled_data_with_velocity(:,1),resampled_data_with_velocity(:,9));
ylabel("Velocity")
legend({"x [m]","y[m]","\theta [rad]","\phi [rad]","v_x [m/s]","v_y [m/s]","\omega_\theta [rad/s]","\omega_\phi [rad/s]"})
saveas(fig_timeseries,"C:\Users\hayashide\kazu_ws\sotsuron_experiment\matlab_ws/results/20240201/20240201_timeseries_odom_800.png")

%% FFT
L = length(resampled_data_with_velocity);
t = resampled_data_with_velocity(:,1);

Y = zeros([length(resampled_data_with_velocity),size(resampled_data_with_velocity,2)]);
for idx = 2:size(resampled_data_with_velocity,2)
    Y(:,idx)=fft(resampled_data_with_velocity(:,idx));
end

%% plot results of FFT
fig_FFT=figure();clf;
% Position
titles=["t","x","y","\theta","\phi"];
for idx = 1:4
    subplot(4,2,2*idx-1);
    plot(resample_hz/L*(0:(L-1)),abs(Y(:,idx+1)),"LineWidth",2);
    hold on; grid on;
    title(titles(idx+1))
    xlabel("f (Hz)")
    ylabel("|fft(X)|")
end
% Velocity
titles=["t","v_x","v_y","\omega_\theta","\omega_\phi"];
for idx = 1:4
    subplot(4,2,2*idx);
    plot(resample_hz/L*(0:(L-1)),abs(Y(:,5+idx)),"LineWidth",2);
    hold on; grid on;
    title(titles(idx+1))
    xlabel("f (Hz)")
    ylabel("|fft(X)|")
end
saveas(fig_FFT,"C:\Users\hayashide\kazu_ws\sotsuron_experiment\matlab_ws/results/20240201/20240201_fft_odom_800.png")
