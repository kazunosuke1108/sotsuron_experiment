clc;clear;
format long;

%% load data
% customVariableNames_odom = {'timestamp', 'x', 'y', 'theta', 'phi'};
odom_data=readmatrix("C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/_2023-12-21-10-22-39/_2023-12-21-10-22-39_od_raw.csv",'Delimiter',',');
[unique_timestamps, idx] = unique(odom_data(:, 1));
unique_odo_data = odom_data(idx, :);

% customVariableNames_laplacian = {'timestamp', 'laplacian', 'min_x', 'max_x', 'min_y', 'max_y'};
laplacian_data=readmatrix("C:\Users\hayashide\kazu_ws\sotsuron_experiment\sotsuron_experiment\analysis\velocity_error\_2023-12-21-10-22-39_laplacian_rgb_hmn.csv",'Delimiter',',');
% laplacian_data(:,1)=laplacian_data(:,1);

%% resample data
timestamp_start=max([unique_odo_data(1,1),laplacian_data(1,1)]);
timestamp_end=min([unique_odo_data(end,1),laplacian_data(end,1)]);
resample_dt=0.1;
resmaple_time_array=timestamp_start:resample_dt:timestamp_end;

resampled_laplacian_data=zeros([length(resmaple_time_array),2]);

resampled_laplacian_data(:,1)=interp1(laplacian_data(:,1),laplacian_data(:,1),resmaple_time_array);
resampled_laplacian_data(:,2)=interp1(laplacian_data(:,1),laplacian_data(:,2),resmaple_time_array);
% resampled_laplacian_data(:,3)=interp1(laplacian_data(:,1),laplacian_data(:,3),resmaple_time_array);
% resampled_laplacian_data(:,4)=interp1(laplacian_data(:,1),laplacian_data(:,4),resmaple_time_array);
% resampled_laplacian_data(:,5)=interp1(laplacian_data(:,1),laplacian_data(:,5),resmaple_time_array);
% resampled_laplacian_data(:,6)=interp1(laplacian_data(:,1),laplacian_data(:,6),resmaple_time_array);

% writematrix(resampled_odom_data,"C:\Users\hayashide\kazu_ws\sotsuron_experiment\sotsuron_experiment\analysis\velocity_error\_2023-12-21-10-22-39_od_raw_resampled.csv")
% writematrix(resampled_laplacian_data,"C:\Users\hayashide\kazu_ws\sotsuron_experiment\sotsuron_experiment\analysis\velocity_error\_2023-12-21-10-22-39_laplacian_rgb_hmn_resampled.csv")

%% get velocity of the odometry
% diff_data=zeros([length(resampled_odom_data),4]);
% diff_data(2:end,:)=diff(resampled_odom_data(:,2:end))./(resampled_odom_data(2:end,1)-resampled_odom_data(1:end-1,1));
% resampled_odom_data=[resampled_odom_data,diff_data];

%% detrend
detrend_n=8;
% detrended_odom_data=detrend(resampled_odom_data,detrend_n);
detrended_laplacian_data=detrend(resampled_laplacian_data,detrend_n);


%% FFT
Fs = 1/resample_dt;                                         % Sampling frequency                    
T = 1/Fs;                                                   % Sampling period       
L = length(resampled_laplacian_data);    % Length of signal
% t = detrended_odom_data(:,1);                               % Time vector
% length(detrended_odom_data(:,1))
Y_lapl=zeros([length(detrended_laplacian_data),2]);
Y_lapl(:,2) = fft(detrended_laplacian_data(:,2));
% Y_lapl(:,3) = fft(detrended_laplacian_data(:,3));
% Y_lapl(:,4) = fft(detrended_laplacian_data(:,4));
% Y_lapl(:,5) = fft(detrended_laplacian_data(:,5));
% Y_lapl(:,6) = fft(detrended_laplacian_data(:,6));

fig1=figure();clf;
plot(resampled_laplacian_data(:,1),resampled_laplacian_data(:,2),"LineWidth",2)
hold on; grid on; 
plot(resampled_laplacian_data(:,1),detrended_laplacian_data(:,2),"LineWidth",2)
legend({"raw data","detrended data"});
title("Results of detrend (resample 10Hz)")
xlabel("f (Hz)")
ylabel("|fft(X)|")
saveas(fig1,"C:\Users\hayashide\kazu_ws\sotsuron_experiment\sotsuron_experiment\analysis\velocity_error/laplacian_fft_10Hz_detrend.png")
fig2=figure();clf;
plot(Fs/L*(0:(L-1)),abs(Y_lapl(:,2)),"LineWidth",2)
title("Complex Magnitude of fft Spectrum (resample 10Hz)")
xlabel("f (Hz)")
ylabel("|fft(X)|")
saveas(fig2,"C:\Users\hayashide\kazu_ws\sotsuron_experiment\sotsuron_experiment\analysis\velocity_error/laplacian_fft_10Hz.png")

% % % plot(resampled_odom_data(:,1),resampled_laplacian_data(:,2))

% %% SST
