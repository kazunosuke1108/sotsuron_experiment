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

dt=mat_general(2,1)-mat_general(1,1);
thR=mat_general(:,9)-mat_general(1,9);
pan=mat_general(:,10)-mat_general(1,10);

xR=mat_general(:,7)-mat_odom(1,1);
yR=mat_general(:,8)-mat_odom(1,2);
thR=mat_general(:,9)-mat_odom(1,3);
xH=xR+z_hmn_cam.*cos(thR+pan)+x_hmn_cam.*sin(thR+pan);
yH=yR+z_hmn_cam.*sin(thR+pan)-x_hmn_cam.*cos(thR+pan);
zH=-y_hmn_cam+1;
flg=sqrt((xH-xR).^2+(yH-yR).^2)<6;
flg=flg(:,find(sum(flg)==min(sum(flg))));
flg_idx=find(flg~=0);
observable_xH=xH(flg_idx,:);
observable_yH=yH(flg_idx,:);
observable_zH=zH(flg_idx,:);
observable_xR=xR(flg_idx);
observable_yR=yR(flg_idx);
observable_thR=thR(flg_idx);
observable_pan=pan(flg_idx);

cutfirst=22;
cutend=25;
observable_xH=observable_xH(cutfirst:end-cutend,:);
observable_yH=observable_yH(cutfirst:end-cutend,:);
observable_zH=observable_zH(cutfirst:end-cutend,:);
observable_xR=observable_xR(cutfirst:end-cutend);
observable_yR=observable_yR(cutfirst:end-cutend);
observable_thR=observable_thR(cutfirst:end-cutend);
observable_pan=observable_pan(cutfirst:end-cutend);

% plot(mat_general(:,2),mat_general(:,3));
% plot3(mat_general(:,2),mat_general(:,3),mat_general(:,4));
% hold on
% plot(xR,yR)
% plot(1:length(thR),thR)
% hold on
% plot(1:length(pan),pan)
% plot3(mat_kp(:,1),mat_kp(:,2),mat_kp(:,3));
% daspect([1 1 1])

% 手順：部位の位置➡つながり
mat_part=getPartsPositions(observable_xH,observable_yH,observable_zH)


fig=figure(1);clf;
bone_1=plot3([observable_xH(1,1),observable_xH(1,2)],[observable_yH(1,1),observable_yH(1,2)],[observable_zH(1,1),observable_zH(1,2)],'k');
hold on
bone_2=plot3([observable_xH(1,1),observable_xH(1,3)],[observable_yH(1,1),observable_yH(1,3)],[observable_zH(1,1),observable_zH(1,3)],'k');
bone_3=plot3([observable_xH(1,2),observable_xH(1,4)],[observable_yH(1,2),observable_yH(1,4)],[observable_zH(1,2),observable_zH(1,4)],'k');
bone_4=plot3([observable_xH(1,3),observable_xH(1,5)],[observable_yH(1,3),observable_yH(1,5)],[observable_zH(1,3),observable_zH(1,5)],'k');
bone_5=plot3([observable_xH(1,1),1/2*(observable_xH(1,12)+observable_xH(1,13))],[observable_yH(1,1),1/2*(observable_yH(1,12)+observable_yH(1,13))],[observable_zH(1,1),1/2*(observable_zH(1,12)+observable_zH(1,13))],'k');
bone_6=plot3([observable_xH(1,6),observable_xH(1,7)],[observable_yH(1,6),observable_yH(1,7)],[observable_zH(1,6),observable_zH(1,7)],'k');
bone_7=plot3([observable_xH(1,6),observable_xH(1,8)],[observable_yH(1,6),observable_yH(1,8)],[observable_zH(1,6),observable_zH(1,8)],'k');
bone_8=plot3([observable_xH(1,7),observable_xH(1,9)],[observable_yH(1,7),observable_yH(1,9)],[observable_zH(1,7),observable_zH(1,9)],'k');
bone_9=plot3([observable_xH(1,8),observable_xH(1,10)],[observable_yH(1,8),observable_yH(1,10)],[observable_zH(1,8),observable_zH(1,10)],'k');
bone_10=plot3([observable_xH(1,9),observable_xH(1,11)],[observable_yH(1,9),observable_yH(1,11)],[observable_zH(1,9),observable_zH(1,11)],'k');
bone_11=plot3([observable_xH(1,12),observable_xH(1,14)],[observable_yH(1,12),observable_yH(1,14)],[observable_zH(1,12),observable_zH(1,14)],'k');
bone_12=plot3([observable_xH(1,13),observable_xH(1,15)],[observable_yH(1,13),observable_yH(1,15)],[observable_zH(1,13),observable_zH(1,15)],'k');
bone_13=plot3([observable_xH(1,14),observable_xH(1,16)],[observable_yH(1,14),observable_yH(1,16)],[observable_zH(1,14),observable_zH(1,16)],'k');
bone_14=plot3([observable_xH(1,15),observable_xH(1,17)],[observable_yH(1,15),observable_yH(1,17)],[observable_zH(1,15),observable_zH(1,17)],'k');
bone_15=plot3([observable_xH(1,12),observable_xH(1,13)],[observable_yH(1,12),observable_yH(1,13)],[observable_zH(1,12),observable_zH(1,13)],'k');
rbt_position=rectangle('Position',[observable_xR(1)-0.3,observable_yR(1)-0.3,0.6,0.6],'Curvature',[1 1],'EdgeColor','b')
rbt_direction=plot([observable_xR(1),observable_xR(1)+0.3*cos(observable_thR(1)+observable_pan(1))],[observable_yR(1),observable_yR(1)+0.3*sin(observable_thR(1)+observable_pan(1))],'b')
frames(length(observable_xH)) = struct('cdata',[],'colormap',[]);
frames(1)=getframe(fig);

for i=1:length(observable_xH)
    plot3(observable_xH(1:i,:),observable_yH(1:i,:),observable_zH(1:i,:),"o","Markersize",0.5)
    plot3(observable_xR(1:i),observable_yR(1:i),zeros(i,1),'b');
    
    % plot3(mat_part(1:i,1:3:end),mat_part(1:i,2:3:end),mat_part(1:i,3:3:end),"LineWidth",1)
    grid on
    set(bone_1,"XData",[observable_xH(i,1),observable_xH(i,2)],"YData",[observable_yH(i,1),observable_yH(i,2)],"ZData",[observable_zH(i,1),observable_zH(i,2)]);
    set(bone_2,"XData",[observable_xH(i,1),observable_xH(i,3)],"YData",[observable_yH(i,1),observable_yH(i,3)],"ZData",[observable_zH(i,1),observable_zH(i,3)]);
    set(bone_3,"XData",[observable_xH(i,2),observable_xH(i,4)],"YData",[observable_yH(i,2),observable_yH(i,4)],"ZData",[observable_zH(i,2),observable_zH(i,4)]);
    set(bone_4,"XData",[observable_xH(i,3),observable_xH(i,5)],"YData",[observable_yH(i,3),observable_yH(i,5)],"ZData",[observable_zH(i,3),observable_zH(i,5)]);
    set(bone_5,"XData",[observable_xH(i,1),1/2*(observable_xH(i,12)+observable_xH(i,13))],"YData",[observable_yH(i,1),1/2*(observable_yH(i,12)+observable_yH(i,13))],"ZData",[observable_zH(i,1),1/2*(observable_zH(i,12)+observable_zH(i,13))]);
    set(bone_6,"XData",[observable_xH(i,6),observable_xH(i,7)],"YData",[observable_yH(i,6),observable_yH(i,7)],"ZData",[observable_zH(i,6),observable_zH(i,7)]);
    set(bone_7,"XData",[observable_xH(i,6),observable_xH(i,8)],"YData",[observable_yH(i,6),observable_yH(i,8)],"ZData",[observable_zH(i,6),observable_zH(i,8)]);
    set(bone_8,"XData",[observable_xH(i,7),observable_xH(i,9)],"YData",[observable_yH(i,7),observable_yH(i,9)],"ZData",[observable_zH(i,7),observable_zH(i,9)]);
    set(bone_9,"XData",[observable_xH(i,8),observable_xH(i,10)],"YData",[observable_yH(i,8),observable_yH(i,10)],"ZData",[observable_zH(i,8),observable_zH(i,10)]);
    set(bone_10,"XData",[observable_xH(i,9),observable_xH(i,11)],"YData",[observable_yH(i,9),observable_yH(i,11)],"ZData",[observable_zH(i,9),observable_zH(i,11)]);
    set(bone_11,"XData",[observable_xH(i,12),observable_xH(i,14)],"YData",[observable_yH(i,12),observable_yH(i,14)],"ZData",[observable_zH(i,12),observable_zH(i,14)]);
    set(bone_12,"XData",[observable_xH(i,13),observable_xH(i,15)],"YData",[observable_yH(i,13),observable_yH(i,15)],"ZData",[observable_zH(i,13),observable_zH(i,15)]);
    set(bone_13,"XData",[observable_xH(i,14),observable_xH(i,16)],"YData",[observable_yH(i,14),observable_yH(i,16)],"ZData",[observable_zH(i,14),observable_zH(i,16)]);
    set(bone_14,"XData",[observable_xH(i,15),observable_xH(i,17)],"YData",[observable_yH(i,15),observable_yH(i,17)],"ZData",[observable_zH(i,15),observable_zH(i,17)]);
    set(bone_15,"XData",[observable_xH(i,12),observable_xH(i,13)],"YData",[observable_yH(i,12),observable_yH(i,13)],"ZData",[observable_zH(i,12),observable_zH(i,13)]);
    set(rbt_position,"Position",[observable_xR(i)-0.3,observable_yR(i)-0.3,0.6,0.6]);
    set(rbt_direction,"XData",[observable_xR(i),observable_xR(i)+0.3*cos(observable_thR(i)+observable_pan(i))],"YData",[observable_yR(i),observable_yR(i)+0.3*sin(observable_thR(i)+observable_pan(i))])

    xlabel("x [m]")
    ylabel("y [m]")
    zlabel("z [m]")
    daspect([1,1,1])
    view([-110,15])
    xlim([-7,7])
    ylim([-1,3])
    zlim([0,2])
    drawnow
    frames(i)=getframe(fig);

end

v = VideoWriter('ROBOMECH_anim.mp4','MPEG-4');
v.FrameRate=1/dt;
open(v);
writeVideo(v,frames);
close(v);
% plot3(observable_xH,observable_yH,observable_zH,"o","Markersize",1)
% hold on
plot3(mat_part(:,1:3:end),mat_part(:,2:3:end),mat_part(:,3:3:end))

function mat_part=getPartsPositions(observable_xH,observable_yH,observable_zH);
    head=[mean(observable_xH(:,1:5),2),mean(observable_yH(:,1:5),2),mean(observable_zH(:,1:5),2)]
    neck=[mean(observable_xH(:,1:3),2),mean(observable_yH(:,1:5),2),mean(observable_zH(:,1:5),2)]
    body=[mean(observable_xH(:,[5,6,11,12]),2),mean(observable_yH(:,[5,6,11,12]),2),mean(observable_zH(:,[5,6,11,12]),2)]
    upper_arm_L=[mean(observable_xH(:,[6,8]),2),mean(observable_yH(:,[6,8]),2),mean(observable_zH(:,[6,8]),2)]
    upper_arm_R=[mean(observable_xH(:,[7,9]),2),mean(observable_yH(:,[7,9]),2),mean(observable_zH(:,[7,9]),2)]
    lower_arm_L=[mean(observable_xH(:,[8,10]),2),mean(observable_yH(:,[8,10]),2),mean(observable_zH(:,[8,10]),2)]
    lower_arm_R=[mean(observable_xH(:,[9,11]),2),mean(observable_yH(:,[9,11]),2),mean(observable_zH(:,[9,11]),2)]
    hand_L=[observable_xH(:,10),observable_yH(:,10),observable_zH(:,10)]
    hand_R=[observable_xH(:,11),observable_yH(:,11),observable_zH(:,11)]
    upper_leg_L=[mean(observable_xH(:,[12,14]),2),mean(observable_yH(:,[12,14]),2),mean(observable_zH(:,[12,14]),2)]
    upper_leg_R=[mean(observable_xH(:,[13,15]),2),mean(observable_yH(:,[13,15]),2),mean(observable_zH(:,[13,15]),2)]
    lower_leg_L=[mean(observable_xH(:,[14,16]),2),mean(observable_yH(:,[14,16]),2),mean(observable_zH(:,[14,16]),2)]
    lower_leg_R=[mean(observable_xH(:,[15,17]),2),mean(observable_yH(:,[15,17]),2),mean(observable_zH(:,[15,17]),2)]
    foot_L=[observable_xH(:,16),observable_yH(:,16),observable_zH(:,16)]
    foot_R=[observable_xH(:,17),observable_yH(:,17),observable_zH(:,17)]
    mat_part=[head,neck,body,upper_arm_L,upper_arm_R,lower_arm_L,lower_arm_R,hand_L,hand_R,upper_leg_L,upper_leg_R,lower_leg_L,lower_leg_R,foot_L,foot_R]
end