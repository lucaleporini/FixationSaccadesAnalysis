function result = low_level_saliency(result_path)
    images_dir = dir([result_path '/LLS_images/*.png']);
    numFrames = numel(images_dir);

    tic
    for j = 1:numFrames
        img = double(imread([result_path '/LLS_images/frame_' num2str(j) '.png']));
        Y(:,:,j) = img;
        S = imresize(img,[64 64],'bilinear');
        Seq(:,:,j) = S/std(S(:));
    end
    Seq = Seq/std(Seq(:));
    disp(['Pre-computation of video: ' num2str(toc) 'sec']);

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
    % result = zeros(1,2,size(SM, 3));
    % result_as_tuples = zeros(size(SM, 3), size(SM, 3));
    for k=1:size(SM, 3)
        a = imresize(SM(:,:,k),[size(Y,1) size(Y,2)]);
        maximum = max(max(a));
        [x,y] = find(a==maximum);
        % result(1,1,k) = x;
        % result(1,2,k) = y;
        result(k,:) = [x y];
    end


    %for k=1:size(result, 3)
    %    fprintf(fid,'%5.1f,',result(1,1,k)) %#ok<PRTCAL>
    %    fprintf(fid,'%5.1f\n',result(1,2,k)) %#ok<PRTCAL>
    %end
    %% Visualize saliency values on top of video frame
    % disp(size(Seq,3))
    %
    % % figure(1),
    % for i = 1:size(Seq,3)
    %    a = imresize(SM(:,:,i),[size(Y,1) size(Y,2)]);
    %    b = sc(cat(3,a, Y(:,:,i)),'prob_jet');
    %    imwrite(b,['images_sm/frame_' num2str(i) '.png'],'png');
    %    pause(.01);
    %end
end