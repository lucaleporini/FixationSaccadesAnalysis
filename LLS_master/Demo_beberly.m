% Space-time Saliency detection Demo
% [HISTORY]
% Apr 25, 2011 : created by Hae Jong Seo

% video v12 e v35 danno errore DA CONTROLLARE

function result_as_tuples = low_level_saliency

    a = dir(['images_for_low_level_saliency/images_v01/*.png']);
    n_frames = numel(a);

    for j = 1:n_frames
        img = double(imread(['images_for_low_level_saliency/images_v01/frame_' num2str(j) '.png']));
        Y(:,:,j) = img;
        S = imresize(img,[64 64],'bilinear');
        Seq(:,:,j) = S/std(S(:));
    end
    Seq = Seq/std(Seq(:));

    %% Parameters
    param.wsize = 3; % LARK spatial window size
    param.wsize_t = 3; % LARK temporal window size
    param.alpha = 0.42; % LARK sensitivity parameter
    param.h = 1;  % smoothing parameter for LARK
    param.sigma = 0.7; % fall-off parameter for self-resemblamnce

    %% Compute 3-D LARKs
    tic;
    LARK = ThreeDLARK(Seq,param);
    disp(['3-D LARK computation : ' num2str(toc) 'sec']);

    %% Compute space-time saliency
    tic;
    SM = SpaceTimeSaliencyMap(Seq,LARK,param.wsize,param.wsize_t,param.sigma);
    disp(['SpaceTimeSaliencyMap : ' num2str(toc) 'sec']);

    %% save max salient pixels of heatmaps
    result = zeros(1,2,size(SM, 3));
    % result_as_tuples = zeros(size(SM, 3), size(SM, 3));
    for k=1:size(SM, 3)
        a = imresize(SM(:,:,k),[size(Y,1) size(Y,2)]);
        maximum = max(max(a));
        [x,y] = find(a==maximum);
        result(1,1,k) = x;
        result(1,2,k) = y;
        result_as_tuples(k,:) = [x y];
    end

    disp('-------------------------------------------------------------------------');
    %disp(result)

    %result_as_tuples = zeros(n_frames);
    %for index= 1: n_frames
    %    result_as_tuples(index) =
    %fid=fopen(['low_level_saliency/saliency_v01.csv'],'wt');
    % for k=1:size(result, 3)
    %       fprintf(fid,'%5.1f,',result(1,1,k)) %#ok<PRTCAL>
    %       fprintf(fid,'%5.1f\n',result(1,2,k)) %#ok<PRTCAL>
    %    result_vett = [result_vett [result(1,1,k),result(1,2,k)]]
    % end
    %fclose(fid);
end




%% Visualize saliency values on top of video frame
% disp(size(Seq,3))
%
% % figure(1),
% for i = 1:size(Seq,3)
%     a = imresize(SM(:,:,i),[size(Y,1) size(Y,2)]);

    %     b = sc(cat(3,a, Y(:,:,i)),'prob_jet');
    %     imwrite(b,['images_sm/frame_' num2str(i) '.png'],'png');
    %     % pause(.01);
    % end
