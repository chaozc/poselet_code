function get_HOG_in_file(hogDir, fname, savename, imgDir, info)
    fid = fopen(fname);
    lines = textscan(fid, '%s %s %d %s %*[^\n]', 'delimiter', '#');
    fclose(fid);
    [nolines, tmp] = size(lines{1});
    for i = 1:nolines
        tmp = get_HOG_patch(lines{1}{i}, lines{2}{i}, imgDir);
        [a, b, c] = size(tmp);
        hog = reshape(tmp, [1, a*b*c]);
        %disp(size(hog));
        dlmwrite([hogDir savename '.hogs'], hog, '-append', 'precision', '%.8f');
        disp([hogDir savename '.mat ' num2str(i), '/', num2str(nolines), ' ', info]);
    end
end