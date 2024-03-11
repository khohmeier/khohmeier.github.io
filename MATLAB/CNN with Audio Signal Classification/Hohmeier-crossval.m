%% Read files ending with -0.wav,-1.wav,-2.wav
K = 3; % consider 3 classes

N = 44.1e3*5; % we already know each audio signal has N coordinates
L = 40; % we already know each class has 40 files
data_raw = zeros(N,L*K);
% data_raw will store all the audio signals. A big matrix.
% Each column is one clip, so we have 40*K many columns
Y = zeros(1,L*K); % Y will contain all the labels

folder = 'C:/Users/Kaitlyn/Documents/Documents - Old Laptop/College Work/4th Year Senior/MAT 495/Data/ESC-50-master/audio/';
%Files=dir(append(folder,'*-0.*'));
for k=0:(K-1)
    % change the number 0 to the string '0'
    Y(L*k+1:L*(k+1))=k;
    str = string(k); %'0'
    Files=dir(append(folder,'*-',str,'.*'));
    % for k=0, this will be dir("ESC-50-master/audio/*-0.*")
    % so pulling out all files ending with -0
    for i = 1:length(Files)
        FileName = Files(i).name;
        data_raw(:,i+k*L)=audioread(append(folder,FileName));
    end
end

%%  mfcc
fs = 44100;
data_mfcc = mfcc(data_raw,fs);
data_mfcc = reshape(data_mfcc,[size(data_mfcc,1)*size(data_mfcc,2),size(data_mfcc,3)]);
%% cross validation
r = 0.8;
Y_categ=categorical(Y);
NumFolds = floor(1/(1-r));
rng(1)
cv = cvpartition(Y,'KFold',NumFolds,'Stratify',true)
%% knn
model = fitcknn(data_mfcc',Y','NumNeighbors',1,'Standardize',true,'CVPartition',cv);
classError = kfoldLoss(model);
accuracy = 1 - classError

%% naive classification for test data
% training(cv,i) is the training index for ith set
% test(cv,i) is the testing index for the ith set
K = length(Y_categ);
center = zeros(size(data_mfcc,1),K);
average = zeros(size(data_mfcc,1),NumFolds);  % used to take the averages over the five folds
% find the centers of each class
for i=1:NumFolds
    for k=1:K
        Ind_k_tr = training(cv,i);
        %average(:,i) = mean(data_mfcc(:,Ind_k_tr),2);
        %center(:,k) = mean(average,2);
        center(:,k) = mean(data_mfcc(:,Ind_k_tr),2);
    end
end

% perform classification
for i=1:NumFolds
    for k=1:K
        data_test = data_mfcc(:,test(cv,i));
        diff = data_test - center(:,k);
        distance(:,k)=sum(diff.^2,1);
        end
[~,lab_predicted] = min(distance,[],2);
lab_predicted = categorical(lab_predicted - 1);
success_rate(i) = length(find(lab_predicted==Y_categ(test(cv,i))'))/length(test(cv,i));
end
