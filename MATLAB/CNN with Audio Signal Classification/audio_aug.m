%% Read files ending with -0.wav,-1.wav,-2.wav
K = 3; % consider 3 classes

N = 44.1e3*5; % we already know each audio signal has N coordinates
L = 240; % we already know each class has 40 files - 5 new ones per class will give 240
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
        [s,fs] = audioread(append(folder,FileName));
        data_raw(:,6*(i-1)+1+k*L)=s;
        augmenter = audioDataAugmenter( ...
            "AugmentationMode","sequential", ...
            "NumAugmentations",5, ...
            ...
            "TimeStretchProbability",0.0, ...
            "SpeedupFactorRange", [1.3,1.4], ...
            ...
            "PitchShiftProbability",0, ...
            ...
            "VolumeControlProbability",0.8, ...
            "VolumeGainRange",[-5,5], ...
            ...
            "AddNoiseProbability",0.1, ...
            ...
            "TimeShiftProbability",0.8, ...
            "TimeShiftRange", [-500e-3,500e-3]);
        moredata = augment(augmenter,s,fs);
        for j = 1:5
            data_raw(:,i+k*240+j) = moredata.Audio{j};
        end
    end
end

%%
L = 6615; %6615 and 400
win = hamming(L,'periodic');
overl = 400;
NumCoef = 13;
[data_mc,data_delta] = mfcc(data_raw,fs,'Window',win,...
    'OverlapLength',overl,'NumCoeffs',NumCoef);
data_mc1 = reshape(data_mc, [size(data_mc,1)*size(data_mc,2),size(data_mc,3)]);
data_mc_delta = [data_mc1;reshape(data_delta, [size(data_mc,1)*size(data_mc,2),size(data_mc,3)])];

%% cross validation set up
r = 0.8; % 80% will be training
Y_c = categorical(Y);
Y_categ = categories(Y_c);
K = length(Y_categ); % number of categories

NumOfFold = floor(1/(1-r));
rng(2);
cv = cvpartition(Y,'KFold',NumOfFold,'Stratify',true);

% training(cv,i) is the training index for ith set
%% PCA
[coeff,score,latent,tsquared,explained] = pca(data_mc1');
% each row should be a clip
S = repmat([25,25,25],40,1);
C = repmat([5,3,4],40,1);
s = S(:);
c = C(:);
%scatter3(score(:,1),score(:,2),score(:,3),s,c,'filled')
figure(1)
scatter3(score(1:40,1),score(1:40,2),score(1:40,3),s(1:40),'red','filled')
hold on
scatter3(score(41:80,1),score(41:80,2),score(41:80,3),s(1:40),'blue','filled')
scatter3(score(81:120,1),score(81:120,2),score(81:120,3),s(1:40),'m','filled')
legend('dog','rooster','pig')
axis equal
xlabel('1st Principal Component')
ylabel('2nd Principal Component')
zlabel('3rd Principal Component')
%% knn
% in fitcknn, each row needs to be a clip
Mdl = fitcknn(data_mc1',Y','NumNeighbors',1,'Standardize',true,'CVPartition',cv);

%Mdl.ModelParameters
%Mdl.Partition
%Mdl.ScoreTransform
%kfoldPredict(Mdl)
knn_success = 1-kfoldLoss(Mdl)

%% CNN
imd1 = size(data_mc,1)
imd2 = size(data_mc,2)
Nch = 1;
layers = [ ...
    imageInputLayer([imd1,imd2, Nch],'Name','input') % 17*14
    convolution2dLayer([2,2],3,'Name','conv1') % flexible
    reluLayer('Name','relu1')
    %dropoutLayer('Name','drop1')
    maxPooling2dLayer([2 1],'Stride',2,'Name','max1') %flexible
    convolution2dLayer([1,3],4,'Name','conv2')%flexible
    reluLayer('Name','relu2')
    maxPooling2dLayer([1 3],'Stride',3,'Name','max2')
    fullyConnectedLayer(5000,'Name','full1')
    reluLayer('Name','relu3')
    dropoutLayer(0.8,'Name','drop1')
    fullyConnectedLayer(5000,'Name','full2')
    reluLayer('Name','relu4')
    dropoutLayer('Name','drop2')
    fullyConnectedLayer(K,'Name','full')
    softmaxLayer('Name','soft')
    classificationLayer('Name','clf')];
lgraph = layerGraph(layers);
analyzeNetwork(lgraph) 
data_mc_cnn = reshape(data_mc,[imd1, imd2, Nch,length(Y)]);
data_mc_cnn_tr = data_mc_cnn(:,:,:,training(cv,1));
data_mc_cnn_test = data_mc_cnn(:,:,:,test(cv,1));
options = trainingOptions('sgdm', ...
    'MaxEpochs',10,...
    'InitialLearnRate',1e-1, ...
    'LearnRateSchedule','piecewise' ,...
    'Verbose',false, ...
    'MiniBatchSize',20,...
    'Plots','training-progress');

net = trainNetwork(data_mc_cnn,Y_c',layers,options);


