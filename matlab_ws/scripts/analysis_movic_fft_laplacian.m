%% initialize
clc;clear;
format long;
set(groot,'DefaultAxesFontName',  'Times New Roman');

%% load data
laplacian_data=readmatrix("C:\Users\hayashide\kazu_ws\sotsuron_experiment\sotsuron_experiment\analysis\velocity_error\_2023-12-21-10-22-39_laplacian_rgb_hmn_01x.csv",'Delimiter',',');
laplacian_data=laplacian_data(:,1:2);

%% extract data
timestamp_start=1703121800;
timestamp_end=timestamp_start+2;
data=laplacian_data(laplacian_data(:,1)>=timestamp_start-1,:);
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
% diff_data=zeros([length(resampled_data),size(resampled_data,2)-1]);
% diff_data(2:end,:)=diff(resampled_data(:,2:end))/resample_dt;
% resampled_data_with_velocity=[resampled_data,diff_data];
resampled_data_with_velocity=resampled_data;

%% detrend
resampled_data_with_velocity=[resampled_data_with_velocity,detrend(resampled_data_with_velocity(:,2),1)];

%% plot timeseries data
fig_timeseries=figure();clf;
plot(resampled_data_with_velocity(:,1),resampled_data_with_velocity(:,2));
hold on; grid on;
plot(resampled_data_with_velocity(:,1),resampled_data_with_velocity(:,3));
% legend({"x [m]","y[m]","\theta [rad]","\phi [rad]"})
xlabel("Time [s]")
ylabel("Value of the blur parameter")
legend({"blur parameter (raw)","blur parameter (detrended)"})
saveas(fig_timeseries,"C:\Users\hayashide\kazu_ws\sotsuron_experiment\matlab_ws/results/20240201/20240201_timeseries_lapl_800.png")

%% FFT
L = length(resampled_data_with_velocity);
t = resampled_data_with_velocity(:,1);

Y = zeros([length(resampled_data_with_velocity),size(resampled_data_with_velocity,2)]);
for idx = 2:size(resampled_data_with_velocity,2)
    Y(:,idx)=fft(resampled_data_with_velocity(:,idx));
end

%% plot results of FFT
fig_FFT=figure();clf;
titles=["blur parameter (raw)","blur parameter (detrended)"];
for idx =2:size(resampled_data_with_velocity,2)
    subplot(2,1,idx-1)
    plot(resample_hz/L*(0:(L-1)),abs(Y(:,idx)),"LineWidth",2);
    hold on; grid on;
    title(titles(idx-1))
    xlabel("f (Hz)")
    ylabel("|fft(X)|")
end
saveas(fig_FFT,"C:\Users\hayashide\kazu_ws\sotsuron_experiment\matlab_ws/results/20240201/20240201_fft_lapl_800.png")
