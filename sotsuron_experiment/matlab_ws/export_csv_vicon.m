clc;clear;

vcn_mat=readmatrix("C:\Users\hayashide\kazu_ws\sotsuron_experiment\sotsuron_experiment\results\20230605\vicon\walk15.csv");
vcn_mat1=vcn_mat(6:6+1235,:)/1000;
vcn_mat2=vcn_mat(1252:1252+1235,:)/1000;
size(vcn_mat2,2)
x1=vcn_mat1(:,3:3:size(vcn_mat1,2));
y1=vcn_mat1(:,4:3:size(vcn_mat1,2));
z1=vcn_mat1(:,5:3:size(vcn_mat1,2));

x2=vcn_mat2(:,3:3:size(vcn_mat2,2));
y2=vcn_mat2(:,4:3:size(vcn_mat2,2));
z2=vcn_mat2(:,5:3:size(vcn_mat2,2));

r.no=109;
l.no=39;
r.mat=[x1(:,r.no),y1(:,r.no),z1(:,r.no)];
l.mat=[x1(:,l.no),y1(:,l.no),z1(:,l.no)];

plot3(r.mat(:,1),r.mat(:,2),r.mat(:,3),".")
grid on
hold on
plot3(l.mat(:,1),l.mat(:,2),l.mat(:,3),".")
daspect([1 1 1])
export_matrix1=[x1,y1,z1];
export_matrix2=[x2,y2,z2];
writematrix(export_matrix1,"C:\Users\hayashide\kazu_ws\sotsuron_experiment\sotsuron_experiment\matlab_ws\result_vcn1.csv")
writematrix(export_matrix2,"C:\Users\hayashide\kazu_ws\sotsuron_experiment\sotsuron_experiment\matlab_ws\result_vcn2.csv")
clf;
for i = 1:10:length(vcn_mat1)
    plot3(x1(1:i,:),y1(1:i,:),z1(1:i,:),".")
    hold on
    drawnow
end

%% VICON
% RKJC: 109
% LKJC: 39
% RAJC: 75?
% LAJC: 6

