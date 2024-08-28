function uv_values = cvtColorSpaceByIccMattrc(prof_path, color_values, direction, colorspace)
    profile = iccread(prof_path);

    cform = makecform("mattrc", profile, "Direction", direction);
    XYZ_values = applycform(color_values, cform);

    % Convert XYZ to u`v`
    cform_arg = "";
    if strcmp(colorspace, 'uv')
        cform_arg = "xyz2upvpl";
    end

    cform = makecform(cform_arg);
    uv_values = applycform(XYZ_values, cform);

end