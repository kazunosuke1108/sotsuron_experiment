clc;clear;
format long;

%% load data
customVariableNames_odom = {'timestamp', 'x', 'y', 'theta', 'phi'};
odom_data=readmatrix("C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/_2023-12-21-10-22-39/_2023-12-21-10-22-39_od_raw.csv",'Delimiter',',');
odom_data(:,1)=odom_data(:,1);
[unique_timestamps, idx] = unique(odom_data(:, 1));
unique_odo_data = odom_data(idx, :);

customVariableNames_laplacian = {'timestamp', 'laplacian', 'min_x', 'max_x', 'min_y', 'max_y'};
laplacian_data=readmatrix("C:\Users\hayashide\kazu_ws\sotsuron_experiment\sotsuron_experiment\analysis\velocity_error\_2023-12-21-10-22-39_laplacian_rgb_hmn.csv",'Delimiter',',');
laplacian_data(:,1)=laplacian_data(:,1);

%% resample data
timestamp_start=max([odom_data(1,1),laplacian_data(1,1)]);
timestamp_end=min([odom_data(end,1),laplacian_data(end,1)]);
resample_dt=0.1;
resmaple_time_array=timestamp_start:resample_dt:timestamp_end;

resampled_odom_data=zeros([length(resmaple_time_array),5]);
resampled_laplacian_data=zeros([length(resmaple_time_array),6]);

resampled_odom_data(:,1)=interp1(unique_odo_data(:,1),unique_odo_data(:,1),resmaple_time_array);
resampled_odom_data(:,2)=interp1(unique_odo_data(:,1),unique_odo_data(:,2),resmaple_time_array);
resampled_odom_data(:,3)=interp1(unique_odo_data(:,1),unique_odo_data(:,3),resmaple_time_array);
resampled_odom_data(:,4)=interp1(unique_odo_data(:,1),unique_odo_data(:,4),resmaple_time_array);
resampled_odom_data(:,5)=interp1(unique_odo_data(:,1),unique_odo_data(:,5),resmaple_time_array);

resampled_laplacian_data(:,1)=interp1(laplacian_data(:,1),laplacian_data(:,1),resmaple_time_array);
resampled_laplacian_data(:,2)=interp1(laplacian_data(:,1),laplacian_data(:,2),resmaple_time_array);
resampled_laplacian_data(:,3)=interp1(laplacian_data(:,1),laplacian_data(:,3),resmaple_time_array);
resampled_laplacian_data(:,4)=interp1(laplacian_data(:,1),laplacian_data(:,4),resmaple_time_array);
resampled_laplacian_data(:,5)=interp1(laplacian_data(:,1),laplacian_data(:,5),resmaple_time_array);
resampled_laplacian_data(:,6)=interp1(laplacian_data(:,1),laplacian_data(:,6),resmaple_time_array);

writematrix(resampled_odom_data,"C:\Users\hayashide\kazu_ws\sotsuron_experiment\sotsuron_experiment\analysis\velocity_error\_2023-12-21-10-22-39_od_raw_resampled.csv")
writematrix(resampled_laplacian_data,"C:\Users\hayashide\kazu_ws\sotsuron_experiment\sotsuron_experiment\analysis\velocity_error\_2023-12-21-10-22-39_laplacian_rgb_hmn_resampled.csv")

%% detrend
detrend_n=8;
detrended_odom_data=detrend(resampled_odom_data,detrend_n);
detrended_laplacian_data=detrend(resampled_laplacian_data,detrend_n);


%% FFT
Fs = 1/resample_dt;                                         % Sampling frequency                    
T = 1/Fs;                                                   % Sampling period       
L = resampled_laplacian_data(end,1)-resampled_laplacian_data(1,1);    % Length of signal
t = detrended_odom_data(:,1);                               % Time vector
length(Fs/L*(0:T:L))
length(detrended_odom_data(:,1))
Y_odom=zeros([length(detrended_odom_data),5]);
Y_odom(:,2) = fft(detrended_odom_data(:,2));
Y_odom(:,3) = fft(detrended_odom_data(:,3));
Y_odom(:,4) = fft(detrended_odom_data(:,4));
Y_odom(:,5) = fft(detrended_odom_data(:,5));
Y_lapl=zeros([length(detrended_laplacian_data),6]);
Y_lapl(:,2) = fft(detrended_laplacian_data(:,2));
Y_lapl(:,3) = fft(detrended_laplacian_data(:,3));
Y_lapl(:,4) = fft(detrended_laplacian_data(:,4));
Y_lapl(:,5) = fft(detrended_laplacian_data(:,5));
Y_lapl(:,6) = fft(detrended_laplacian_data(:,6));

% plot(Fs/L*(0:T:L),abs(Y_odom(:,2:end)),"LineWidth",2)

% plot(resampled_odom_data(:,1),resampled_laplacian_data(:,2))
% hold on; grid on; 
% plot(resampled_odom_data(:,1),detrended_laplacian_data(:,2))
plot(Fs/L*(0:T:L),abs(Y_lapl(:,2)),"LineWidth",2)
title("Complex Magnitude of fft Spectrum")
xlabel("f (Hz)")
ylabel("|fft(X)|")

%% SST
