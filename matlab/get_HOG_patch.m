function hog = get_HOG_patch(imgID, posInfo, imgDir)
    posInfo = posInfo(2:length(posInfo)-1);
    pos = textscan(posInfo, '%d %d %d %d', 'delimiter', ',');
    try
        fname = [imgDir imgID '.jpg'];
        img = imread(fname);
    catch
        fname = [imgDir imgID '.png'];
        img = imread(fname);
    end
    img = im2single(rgb2gray(img));
    img = img(pos{2}+1:pos{2}+pos{4}, pos{1}+1:pos{1}+pos{3});
    img = imresize(img, [144, 96]);
    cellSize = 8 ;
    hog = vl_hog(img, cellSize) ;
%     imwrite(img, ['../xx/', dd, '/', imgID, posInfo, '.jpg'], 'jpg');
%     imhog = vl_hog('render', hog, 'variant', 'dalaltriggs') ;
%     imwrite(imhog, ['../yy/', dd, '/', imgID, posInfo, '.jpg'], 'jpg');
end