clc;clear;
% fig=figure();clf;

mat_general=readmatrix("C:\Users\hayashide\kazu_ws\sotsuron_experiment\sotsuron_experiment\results\0117\csv\20230117_d_060_1_Hayashide.csv");
mat=readmatrix("C:\Users\hayashide\kazu_ws\sotsuron_experiment\sotsuron_experiment\matlab_ws\result.csv")
labelList=getLabel();
r.no=13;
l.no=12;

t=fixTimeBug(mat);
r.mat=[mat(:,r.no),mat(:,r.no+17),mat(:,r.no+17*2)];

sysY=tfest([t r.mat(:,3)],3)

noise=wgn(length(t),1,1);
% sysV=tfest([t noise],3)
sysV=tf([1],[1,0]);
sysH=sysY/sysV

b=sysH.Numerator;
a=sysH.Denominator;

% bode(sysH.Numerator,sysH.Denominator)

% hold on
% bode(sysH)

sysX=sysH^-1
% bode(sysX)
step(sysX)



% txy=tfestimate(noise,r.mat(:,3))

% [pxx,w]=periodogram(r.mat(:,3));
% [pxx,f]=periodogram(r.mat(:,3));
% hz=w;
% dB=20*log(pxx);

% [Be, Ae]=invfreqz(pxx.*exp(i*w),w,3,4)

% % p=polyfit(hz,dB,2)
% subplot(2,1,1)
% plot(hz,dB,"r")
% grid on
% hold on
% bode(Be,Ae)

% %%System Identification Toolbox での解析例 
% % デモ用の同定入力の作成 
% clc;clear;
% b=[2,1]; % 分子係数 
% a=[1,3,2]; % 分母係数 
% nb=length(b)-1; % 分子の次数 
% na=length(a)-1; % 分母の次数 
% sys=tf(b,a); % 伝達関数モデルの定義 
% [mag,phase,w]=bode(sys); % mag:振幅, phase:位相, w:周波数ベクトル 
% mag=squeeze(mag); % 1の次元を削除 
% phase=squeeze(phase);   
% z = mag.*exp(i*phase/180*pi); % z: 複素周波数応答 
% % IDFRD(同定用の周波数応答データ)オブジェクト作成 
% data = idfrd(z,w,0);      % 連続システムの周波数応答データとして定義  
% % 各手法での伝達関数モデル推定例 
% m1 = oe(data,[nb+1,na]); 
% m2 = pem(data,na);        % 分母分子のそれぞれの次数は指定不可 
% m3 = n4sid(data,na);      % 分母分子のそれぞれの次数は指定不可 
% % TF(伝達関数)オブジェクトに変換 
% sys1=tf(m1,'m')    % 'm'をつけることで、ノイズ入力を無視 
% sys2=tf(m2,'m') 
% sys3=tf(m3,'m') 
% bode(sys,sys1,sys2,sys3) % 結果の検証のため、ボード線図を比較表示