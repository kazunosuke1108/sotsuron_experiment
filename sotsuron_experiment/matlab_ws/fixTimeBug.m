function time_compensated=fixTimeBug(mat)
    % mat=load("C:\Users\hayashide\kazu_ws\sotsuron_experiment\sotsuron_experiment\matlab_ws\result.csv");
    % fig=figure();clf;
    time_series=mat(:,end)-mat(1,end);
    time_compensated=zeros(size(time_series));
    frame_idx=1:length(time_series);

    time_compensated(1)=time_series(1);
    time_compensated(2)=time_series(2);

    outlier_flg=false;
    recent_outlier=1;

    for i = 2:length(time_series)-1
        if time_series(i+1)-time_series(i)>2.5*(time_compensated(i)-time_compensated(i-1)) || time_series(i+1)-time_series(i)<0
            if ~outlier_flg
                recent_outlier=frame_idx(i);
            end
            outlier_flg=true;
            time_compensated(i+1)=(time_series(recent_outlier)-time_series(recent_outlier-1))*(frame_idx(i+1)-frame_idx(i))+time_compensated(i);
            % scatter(frame_idx(i+1),time_compensated(i+1));
        else
            time_compensated(i+1)=time_series(i+1);
            outlier_flg=false;
        end
    end
end
% % time_compensated=smoothdata(time_series)
% plot(frame_idx,mat(:,end)-mat(1,end))
% hold on
% % plot(frame_idx,straight(1)*frame_idx)
% plot(frame_idx,time_compensated)
% xlabel("frame no.")
% ylabel("time [s]")
% legend("raw time [s]","compensated time [s]")
% saveas(fig,"C:\Users\hayashide\kazu_ws\sotsuron_experiment\sotsuron_experiment\matlab_ws\time_noise.png")