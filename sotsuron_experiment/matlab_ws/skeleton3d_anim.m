clc;clear;

% addpath "C:\Users\hayashide\kazu_ws\sotsuron_experiment\sotsuron_experiment\results\0117"
mat_general=readmatrix("C:\Users\hayashide\kazu_ws\sotsuron_experiment\sotsuron_experiment\results\0117\csv\20230117_d_060_1_Hayashide.csv");
mat_kp=readmatrix("C:\Users\hayashide\kazu_ws\sotsuron_experiment\sotsuron_experiment\results\0117\csv\20230117_d_060_1_Hayashide_kp.csv");
mat_odom=readmatrix("C:\Users\hayashide\kazu_ws\sotsuron_experiment\sotsuron_experiment\results\0117\odom_csv\20230117_d_060_1_Hayashide.csv");

% x_hmn_cam=mat_general(:,2)/1000;
% y_hmn_cam=mat_general(:,3)/1000;
% z_hmn_cam=mat_general(:,4)/1000;

x_hmn_cam=mat_kp(:,[1:4:end])/1000;
y_hmn_cam=mat_kp(:,[2:4:end])/1000;
z_hmn_cam=mat_kp(:,[3:4:end])/1000;


thR=mat_general(:,9)-mat_general(1,9);
pan=mat_general(:,10)-mat_general(1,10);

xR=mat_general(:,7)-mat_odom(1,1);
yR=mat_general(:,8)-mat_odom(1,2);
xH=xR+z_hmn_cam.*cos(thR+pan)+x_hmn_cam.*sin(thR+pan);
yH=yR+z_hmn_cam.*sin(thR+pan)-x_hmn_cam.*cos(thR+pan);
zH=y_hmn_cam+1;
flg=sqrt((xH-xR).^2+(yH-yR).^2)<6;
observable_xH=xH.*flg;
observable_yH=yH.*flg;
observable_zH=zH.*flg;
% plot(mat_general(:,2),mat_general(:,3));
% plot3(mat_general(:,2),mat_general(:,3),mat_general(:,4));
% hold on
% plot(xR,yR)
% plot(1:length(thR),thR)
% hold on
% plot(1:length(pan),pan)
for i=1:length(observable_xH)
    % plot3(observable_xH(1:i,:),observable_yH(1:i,:),observable_zH(1:i,:),"o","Markersize",1)
    hold on
    % if mod(i,100)==0
    %     plot3(observable_xH(i))
    % end
    % drawnow
end
plot3(observable_xH,observable_yH,observable_zH)%,"o","Markersize",1)
% plot3(mat_kp(:,1),mat_kp(:,2),mat_kp(:,3));
% daspect([1 1 1])
xlabel("x [m]")
ylabel("y [m]")
zlabel("z [m]")

