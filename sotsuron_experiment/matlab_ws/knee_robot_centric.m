clc;clear;
close all;
load("C:\Users\hayashide\kazu_ws\sotsuron_simulator\matlab_ws\230117\results\230117_7F\230117_200325_vx060_y050\230117_200325_.mat");
mat_general=readmatrix("C:\Users\hayashide\kazu_ws\sotsuron_experiment\sotsuron_experiment\results\0117\csv\20230117_d_060_1_Hayashide.csv");
mat=readmatrix("C:\Users\hayashide\kazu_ws\sotsuron_experiment\sotsuron_experiment\matlab_ws\result.csv");
labelList=getLabel();
r.no=15;
l.no=14;

% [~,ind] = sort(mat(:,end));
% mat= mat(ind,:);
% t=mat(:,56)-mat(1,56)
t=fixTimeBug(mat);
r.mat=[mat(:,r.no),mat(:,r.no+17),mat(:,r.no+17*2)];
l.mat=[mat(:,l.no),mat(:,l.no+17),mat(:,l.no+17*2)];
rbt.mat = [mat(:,52),mat(:,53),mat(:,54),mat(:,55)];

%% occulusion detector
distance=sqrt((r.mat(:,1)-l.mat(:,1)).^2+(r.mat(:,2)-l.mat(:,2)).^2+(r.mat(:,3)-l.mat(:,3)).^2);
not_ocl_idx=find(distance>=0.1);
ocl_idx=find(distance<0.1);


% knee_center=1/2*(r.mat+l.mat);

% r.relative_mat=r.mat-knee_center;
% l.relative_mat=l.mat-knee_center;
% rbt.relative_mat=rbt.mat-[knee_center(:,1:2),zeros(length(knee_center),2)];

% fig1=figure(1);
% frames(length(knee_center)) = struct('cdata',[],'colormap',[]);
% frames(1)=getframe(fig1);
% for i = 1:length(r.relative_mat)
%     plot(r.relative_mat(max(i-5,1):i,1),r.relative_mat(max(i-5,1):i,2),"r","LineWidth",5);
%     hold on
%     grid on
%     plot(l.relative_mat(max(i-5,1):i,1),l.relative_mat(max(i-5,1):i,2),"b","LineWidth",5);
%     hold on
%     rbt_position=rectangle('Position',[rbt.relative_mat(i,1)-0.3,rbt.relative_mat(i,2)-0.3,0.6,0.6],'Curvature',[1 1],'EdgeColor','b');
%     hold on
%     rbt_direction=plot([rbt.relative_mat(i,1),rbt.relative_mat(i,1)+0.3*cos(rbt.relative_mat(i,3)+rbt.relative_mat(i,4))],[rbt.relative_mat(i,2),rbt.relative_mat(i,2)+0.3*sin(rbt.relative_mat(i,3)+rbt.relative_mat(i,4))],'b','LineWidth',2);
%     hold on
%     plt_ocl_idx=ocl_idx(find(ocl_idx<=i));
%     plot(rbt.relative_mat(plt_ocl_idx,1),rbt.relative_mat(plt_ocl_idx,2),"xk","MarkerSize",10);
%     hold off
%     xlim([-6,6])
%     ylim([-1,3])
%     title("human centric view")
%     xlabel("position x [m]")
%     ylabel("position y [m]")
%     daspect([1 1 1])
%     drawnow
%     frames(i)=getframe(fig1);
% end
% v = VideoWriter('Hayashide_'+"human_centric"+'_knee.mp4','MPEG-4');
% v.FrameRate=1/0.05;
% open(v);
% writeVideo(v,frames);
% close(v);