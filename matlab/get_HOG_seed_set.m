function get_HOG_seed_set(hogDir, imgDir, seed_sample_Dir)
    files = dir([seed_sample_Dir, '*.sample']);
    len = length(files);
    for i = 1:len
        fname = files(i).name;
%         mkdir(['../xx/', num2str(i)]);
%         mkdir(['../yy/', num2str(i)]);
        get_HOG_in_file(hogDir, [seed_sample_Dir, fname], fname, imgDir, [num2str(i),'/',num2str(len),' sets processing']);
        disp([num2str(i),'/',num2str(len),' sets finished']);
    end
end