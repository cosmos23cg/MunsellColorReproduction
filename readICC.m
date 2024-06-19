clear;

%% Main script
% Plot chromaticity
figure("Units","inches","Position",[1,1,7,7]);
plotChromaticityDiagram();

% Plot spectrum locus
spectrum_path = "C:\Users\cghsi\OneDrive\NTUST_CIT\Color_data_set\CIE_xyz_1931_2deg.csv";
spec_uv = getSpectrumLocusData(spectrum_path); 
plot(spec_uv(:, 1), spec_uv(:, 2), '- .', 'Color', 'k', 'LineWidth', 1, 'MarkerIndices', 1:20:length(spec_uv), 'MarkerSize', 15);

% Plot sRGB
sRGB = [255 0 0;
    0 255 0;
    0 0 255];
sRGB_icc_path = "C:\Windows\System32\spool\drivers\color\sRGB Color Space Profile.icm";
srgb_plot = plotRGBGamutArea(sRGB_icc_path, sRGB, '-', 'black', 1.3);

% Plot AdobeRGB
AdobeRGB = [255 0 0;
    0 255 0;
    0 0 255];
adobe_icc_path = "C:\Windows\System32\spool\drivers\color\AdobeRGB1998.icc";
adobe_plot = plotRGBGamutArea(adobe_icc_path, AdobeRGB, '-', 'red', 1.3);

% Plot NXP CMYK
% NXP CMYK
% cmyk_rgb = [0 1 1 0; % r
%             0 1 0 0; % m
%             1 1 0 0; % b
%             1 0 0 0; % c
%             1 0 1 0; % g
%             0 0 1 0]; % y
% printer_icc_path = "C:\Users\cghsi\OneDrive\NTUST_CIT\Experiments\Munsell_Reproduction\ICC\NXP_CMYK_2Glossy_GCR.icm";
% printer_plot = plotCMYKGamutArea(printer_icc_path, cmyk_rgb, '--', 'black', 1.3);

% NXP CMYK+B
% cmyk_b_rgb = [0 1 1 0 0; % r
%             0 1 0 0 0; % m
%             1 1 0 0 1; % b
%             1 0 0 0 0; % c
%             1 0 1 0 0; % g
%             0 0 1 0 0]; % y
% 
% printer_icc_path = "C:\Users\cghsi\OneDrive\NTUST_CIT\Experiments\Munsell_Reproduction\ICC\NXP_BLUE_2Glossy_GCR.icm";
% printer_plot = plotCMYKGamutArea(printer_icc_path, cmyk_b_rgb, '--', 'black', 1.3);


% NXP CMYK+G
% cmyk_g_rgb = [0 1 1 0 0; % r
%             0 1 0 0 0; % m
%             1 1 0 0 0; % b
%             1 0 0 0 0; % c
%             1 0 1 0 1; % g
%             0 0 1 0 0]; % y
% 
% printer_icc_path = "C:\Users\cghsi\OneDrive\NTUST_CIT\Experiments\Munsell_Reproduction\ICC\NXP_GREEN_2Glossy_GCR.icm";
% printer_plot = plotCMYKGamutArea(printer_icc_path, cmyk_g_rgb, '--', 'black', 1.3);

% NXP CMYK+R
% cmyk_r_rgb = [0 1 1 0 1; % r
%             0 1 0 0 0; % m
%             1 1 0 0 0; % b
%             1 0 0 0 0; % c
%             1 0 1 0 0; % g
%             0 0 1 0 0]; % y
% 
% printer_icc_path = "C:\Users\cghsi\OneDrive\NTUST_CIT\Experiments\Munsell_Reproduction\ICC\NXP_RED_2Glossy_GCR.icm";
% printer_plot = plotCMYKGamutArea(printer_icc_path, cmyk_r_rgb, '--', 'black', 1.3);

% EPSON 9700
cmyk_rgb = [0 1 1 0; % r
            0 1 0 0; % m
            1 1 0 0; % b
            1 0 0 0; % c
            1 0 1 0; % g
            0 0 1 0]; % y
printer_icc_path = "C:\Users\cghsi\OneDrive\NTUST_CIT\Experiments\Munsell_Reproduction\ICC\epson9700_IT8.7-4 CMYK random_Chart 1617 Patches_08-03-24.icm";
printer_plot = plotCMYKGamutArea(printer_icc_path, cmyk_rgb, '--', 'black', 1.3);

% Add legend
legend([srgb_plot, adobe_plot, printer_plot], {'sRGB / Rec.709', 'Adobe RGB', 'EPSON 9700'}, 'Location', 'northeast');

hold off;

% Axis settings
% title("CIE u′v′ chromaticity diagram");
xlabel("u`");
ylabel("v`");
xlim([-0.05 0.7]);
ylim([-0.05 0.7]);


%% Helper functions
function plotChromaticityDiagram()
    plotChromaticity('ColorSpace','uv');
    hold on;
    
    axis tight;
    ax = gca;
    xLimits = ax.XLim;
    yLimits = ax.YLim;
    
    % apply a alpha mask
    fill([xLimits(1) xLimits(2) xLimits(2) xLimits(1)], ...
         [yLimits(1) yLimits(1) yLimits(2) yLimits(2)], ...
         'w', 'FaceAlpha', 0.5, 'EdgeColor', 'none');
end

function spec_uv = getSpectrumLocusData(filePath)
    spec_loc = readtable(filePath);

    % Fetch the data range from 380~780nm
    XYZ_spec = spec_loc{61:350, 2:4};
    cform = makecform("xyz2upvpl");
    spec_uv = applycform(XYZ_spec, cform);

    wavelengths = spec_loc{61:311, 1};
    for i = 1:20:length(wavelengths)
        if spec_uv(i, 1) > 0.01 && spec_uv(i, 2) > 0.5
            text(spec_uv(i, 1), spec_uv(i, 2) + 0.02, num2str(wavelengths(i)), 'FontSize', 8, 'HorizontalAlignment', 'center');
        else
            text(spec_uv(i, 1) - 0.01, spec_uv(i, 2), num2str(wavelengths(i)), 'FontSize', 8, 'HorizontalAlignment', 'right');
        end
    end
    % mark 680nm
    text(spec_uv(280, 1) + 0.005, spec_uv(280, 2) + 0.02, "680", "FontSize", 8, "HorizontalAlignment", "left");
end

function plotHandle = plotRGBGamutArea(profile_path, rgb_values, line_style, line_color, line_width)
    % Read ICC
    profile = iccread(profile_path);

    % RGB to XYZ
    cform = makecform("mattrc", profile, "Direction", "forward");
    XYZ_values = applycform(rgb_values, cform);

    % XYZ to u`v`
    cform = makecform("xyz2upvpl");
    uv_values = applycform(XYZ_values, cform);
    
    % Duplicate the first points to the last for closing the plot area
    u_values = vertcat(uv_values(:, 1), uv_values(1, 1));
    v_values = vertcat(uv_values(:, 2), uv_values(1, 2)); 

    plotHandle = plot(u_values, v_values, 'LineStyle', line_style, 'Color', line_color, 'LineWidth', line_width);
end

function plotHandle = plotCMYKGamutArea(profile_path, cmyk_values, line_style, line_color, line_width)
    % Read ICC
    profile = iccread(profile_path);
    cform = makecform("clut", profile, "AToB0");

    % CMYK to Lab
    npx_lab = applycform(cmyk_values, cform);
    npx_lab = lab2double(npx_lab);

    % Lab to XYZ
    npx_XYZ = lab2xyz(npx_lab, "WhitePoint", "d50");

    % XYZ to u`v`
    cform = makecform("xyz2upvpl");
    npx_uv = applycform(npx_XYZ, cform);

    % Duplicate the first points to the last for closing the plot area
    u_values = vertcat(npx_uv(:, 1), npx_uv(1, 1));
    v_values = vertcat(npx_uv(:, 2), npx_uv(1, 2));
    area = calculatePolygonArea(u_values, v_values);
    disp(area)

    plotHandle = plot(u_values, v_values, 'LineStyle', line_style, 'Color', line_color, 'LineWidth', line_width);
end

function area = calculatePolygonArea(u, v)
    % Calculate the polygon area using the shoelace formula
    n = length(u);
    area = 0;
    for i = 1:n-1
        area = area + (u(i) * v(i+1) - v(i) * u(i+1));
    end
    area = area + (u(n) * v(1) - v(n) * u(1));
    area = 0.5 * abs(area);
end