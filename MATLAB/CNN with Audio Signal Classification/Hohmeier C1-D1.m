%% Read files ending with -0.wav,-1.wav,-2.wav
K = 3; % consider 3 classes

N = 44.1e3*5; % we already know each audio signal has N coordinates
L = 40; % we already know each class has 40 files
data_raw = zeros(N,L*K);
% data_raw will store all the audio signals. A big matrix.
% Each column is one clip, so we have 40*K many columns

folder = 'C:/Users/Kaitlyn/Documents/Documents - Old Laptop/College Work/4th Year Senior/MAT 495/Data/ESC-50-master/audio/';
Files=dir(append(folder,'*-0.*'));
for k=0:(K-1)    
    % change the number 0 to the string '0'
    str = string(k); %'0'
    Files=dir(append(folder,'*-',str,'.*'));
    % for k=0, this will be dir("ESC-50-master/audio/*-0.*")
    % so pulling out all files ending with -0
    for i = 1:length(Files)
        FileName = Files(i).name;
        data_raw(:,i+k*L)=audioread(append(folder,FileName));
    end
end
%% Clip & downsample
%clip
clip=220500/5*2;
new_data_raw = data_raw(1:clip,:);
%downsample
fs=44100;
newfs=8000;
[P,Q]= rat(newfs/fs);
audionew = resample(new_data_raw,P,Q);
%% Subset training and test data
train_ind = [1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 41 42 43 44 45 46 47 48 ... 
    49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 ...
    97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112];
    % array with the indices to be obtained from audionew to build the training set. the remaining data is test set
data_train = audionew(:,train_ind);

test_ind = [33 34 35 36 37 38 39 40 73 74 75 76 77 78 79 80 113 114 115 116 117 118 119 120];
data_test = audionew(:,test_ind);

%% classification - find center
dog=data_train(:,1:32);
rooster=data_train(:,33:64);
pig=data_train(:,65:96);
% take the mean for each class. 2 = by column
avgdog=mean(dog,2,'double');
avgr=mean(rooster,2,'double');
avgpig=mean(pig,2,'double');
%% classification for test data
class_matrix = zeros(1,24);
for i=1:24
    new_clip=data_test(:,i);
    d1=norm(new_clip-avgdog)
    d2=norm(new_clip-avgr)
    d3=norm(new_clip-avgpig)
    temp=[d1 d2 d3];
    if d1==min(temp)
        class_matrix(1,i) = 1;
    end
    if d2==min(temp)
        class_matrix(1,i) = 2;
    end
    if d3==min(temp)
        class_matrix(1,i) = 3;
    end
end
%% change to categories
% Y = [0 0 1 1 2 2]
% Y = categorical(Y)






