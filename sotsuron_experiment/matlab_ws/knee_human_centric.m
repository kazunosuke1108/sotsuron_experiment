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

%% human centric plot
knee_center=1/2*(r.mat+l.mat);

r.relative_mat=r.mat-knee_center;
l.relative_mat=l.mat-knee_center;
rbt.relative_mat=rbt.mat-[knee_center(:,1:2),zeros(length(knee_center),2)];

fig1=figure(1);
frames(length(knee_center)) = struct('cdata',[],'colormap',[]);
frames(1)=getframe(fig1);
for i = 1:length(r.relative_mat)
    plot(r.relative_mat(max(i-5,1):i,1),r.relative_mat(max(i-5,1):i,2),"r","LineWidth",5);
    hold on
    grid on
    plot(l.relative_mat(max(i-5,1):i,1),l.relative_mat(max(i-5,1):i,2),"b","LineWidth",5);
    hold on
    rbt_position=rectangle('Position',[rbt.relative_mat(i,1)-0.3,rbt.relative_mat(i,2)-0.3,0.6,0.6],'Curvature',[1 1],'EdgeColor','b');
    hold on
    rbt_direction=plot([rbt.relative_mat(i,1),rbt.relative_mat(i,1)+0.3*cos(rbt.relative_mat(i,3)+rbt.relative_mat(i,4))],[rbt.relative_mat(i,2),rbt.relative_mat(i,2)+0.3*sin(rbt.relative_mat(i,3)+rbt.relative_mat(i,4))],'b','LineWidth',2);
    hold on
    plt_ocl_idx=ocl_idx(find(ocl_idx<=i));
    plot(rbt.relative_mat(plt_ocl_idx,1),rbt.relative_mat(plt_ocl_idx,2),"xk","MarkerSize",10);
    hold off
    xlim([-6,6])
    ylim([-1,3])
    title("human centric view")
    xlabel("position x [m]")
    ylabel("position y [m]")
    daspect([1 1 1])
    drawnow
    frames(i)=getframe(fig1);
end
v = VideoWriter('Hayashide_'+"human_centric"+'_knee.mp4','MPEG-4');
v.FrameRate=1/0.05;
open(v);
writeVideo(v,frames);
close(v);

%% 角度と欠損のヒストグラム
bins=0:10:180;
clf;
fig1 = figure(1);
atan_list=rad2deg(atan(rbt.relative_mat(:,2)./rbt.relative_mat(:,1)))
atan_list=atan_list.*(atan_list>=0)+(180+atan_list).*(atan_list<0)
ocl_atan_list=rad2deg(atan(rbt.relative_mat(ocl_idx,2)./rbt.relative_mat(ocl_idx,1)));
ocl_atan_list=ocl_atan_list.*(ocl_atan_list>=0)+(180+ocl_atan_list).*(ocl_atan_list<0)
ocl_atan_list=ocl_atan_list+90*(ocl_atan_list<0);
% subplot(2,2,1)
% h_all=histogram(-atan_list,bins)
% subplot(2,2,2)
% h_ocl=histogram(-ocl_atan_list,bins)
% h_ocl.Data
% subplot(2,2,3)
h_all=histogram(-atan_list,length(ocl_idx),"FaceColor","k")
h_all_values=h_all.Values
h_all_BinEdges=h_all.BinEdges
hold on
h_ocl=histogram(-ocl_atan_list,length(ocl_idx),"FaceColor","r")
h_ocl_values=h_ocl.Values
h_ocl_BinEdges=h_ocl.BinEdges
hold on
plot(h_ocl_BinEdges(1:length(h_ocl_values)),h_ocl_values./h_all_values,"oy-","LineWidth",2)
xlabel("人の進行方向を -180 deg とした時の相対角度 [deg]")
ylabel("フレーム数 [枚]")
ylim([0,10])
legend("全フレーム数","隠れ発生数","隠れ発生比率","Location","northwest")
grid on
saveas(fig1,"histgram.png")
% subplot(2,2,4)

%% robot centric plot

r.relative_mat_rbt=zeros(length(r.mat),2)
l.relative_mat_rbt=zeros(length(l.mat),2)
for i = 1:length(r.relative_mat)
    rotate_matrix=[cos(rbt.mat(i,3)+rbt.mat(i,4)),sin(rbt.mat(i,3)+rbt.mat(i,4));...
        -sin(rbt.mat(i,3)+rbt.mat(i,4)),cos(rbt.mat(i,3)+rbt.mat(i,4))];
    r.relative_mat_rbt(i,:)=transpose(rotate_matrix*[r.mat(i,1)-rbt.mat(i,1);r.mat(i,2)-rbt.mat(i,2)]);
    l.relative_mat_rbt(i,:)=transpose(rotate_matrix*[l.mat(i,1)-rbt.mat(i,1);l.mat(i,2)-rbt.mat(i,2)]);
end

fig2=figure(2);
fig2.Position=[100 100 700 800];
frames(length(knee_center)) = struct('cdata',[],'colormap',[]);
hold on;
grid on;
daspect([1 1 1]);
xlabel("position x [m]");
ylabel("position y [m]");
title("robot centric view");

arc_resolution=100;
arc_rad = linspace(-sns.phi,sns.phi,arc_resolution);
arc_r1_x = sns.r1*cos(arc_rad);
arc_r1_y = sns.r1*sin(arc_rad);
arc_r2_x = sns.r2*cos(arc_rad);
arc_r2_y = sns.r2*sin(arc_rad);
arc_r1 = plot(arc_r1_x,arc_r1_y,'g');
arc_r2 = plot(arc_r2_x,arc_r2_y,'g');
arc_right = plot([arc_r1_x(1),arc_r2_x(1)],[arc_r1_y(1),arc_r2_y(1)],'g');
arc_left = plot([arc_r1_x(end),arc_r2_x(end)],[arc_r1_y(end),arc_r2_y(end)],'g');
arc_right_helper=plot([0,arc_r1_x(1)],[0,arc_r1_y(1)],'--g');
arc_left_helper=plot([0,arc_r1_x(end)],[0,arc_r1_y(end)],'--g');
rbt_position=rectangle('Position',[0-0.3,0-0.3,0.6,0.6],'Curvature',[1 1],'EdgeColor','b');
rbt_direction=plot([0,0.3],[0,0],'b','LineWidth',2);

r_plot=plot(r.relative_mat_rbt(1,1),r.relative_mat_rbt(1,2),"r","LineWidth",1.5)
l_plot=plot(l.relative_mat_rbt(1,1),l.relative_mat_rbt(1,2),"b","LineWidth",1.5)
r_plot_hist=plot(r.relative_mat_rbt(1,1),r.relative_mat_rbt(1,2),"r","LineWidth",0.25)
l_plot_hist=plot(l.relative_mat_rbt(1,1),l.relative_mat_rbt(1,2),"b","LineWidth",0.25)

ocl_plot=plot(r.relative_mat_rbt(1,1),rbt.relative_mat(plt_ocl_idx,2),"xk","MarkerSize",10);

frames(1)=getframe(fig2);

for i = 1:length(r.relative_mat_rbt)
    plt_ocl_idx=ocl_idx(find(ocl_idx<=i));
    set(ocl_plot,"XData",l.relative_mat_rbt(plt_ocl_idx,1),"YData",l.relative_mat_rbt(plt_ocl_idx,2));
    set(r_plot,"XData",r.relative_mat_rbt(max(i-5,1):i,1),"YData",r.relative_mat_rbt(max(i-5,1):i,2));
    set(l_plot,"XData",l.relative_mat_rbt(max(i-5,1):i,1),"YData",l.relative_mat_rbt(max(i-5,1):i,2));
    set(r_plot_hist,"XData",r.relative_mat_rbt(1:i,1),"YData",r.relative_mat_rbt(1:i,2));
    set(l_plot_hist,"XData",l.relative_mat_rbt(1:i,1),"YData",l.relative_mat_rbt(1:i,2));
    drawnow
    frames(i)=getframe(fig2);
end

v = VideoWriter('Hayashide_'+"robot_centric"+'_knee.mp4','MPEG-4');
v.FrameRate=1/0.05;
open(v);
writeVideo(v,frames);
close(v);