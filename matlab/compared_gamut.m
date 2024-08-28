% This script plot the maxumun chroma in ab diagram

clear;
clc

figure("Units","inches","Position",[1,1,7,7]);
hold on;


%% ICC profile path
% iso_icc_path = "C:\Users\cghsi\OneDrive\NTUST_CIT\Lab\Munsell_Reproduction\ICC\PSOcoated_v3.icc";
CMYK_icc_path = "C:\Users\cghsi\OneDrive\NTUST_CIT\Lab\Munsell_Reproduction\ICC\NXP_CMYK_2Glossy_GCR.icm";
% CMYKR_icc_path = "C:\Users\cghsi\OneDrive\NTUST_CIT\Lab\Munsell_Reproduction\ICC\NXP_RED_2Glossy_GCR.icm";
% CMYKG_icc_path = "C:\Users\cghsi\OneDrive\NTUST_CIT\Lab\Munsell_Reproduction\ICC\NXP_GREEN_2Glossy_GCR.icm";
CMYKB_icc_path = "C:\Users\cghsi\OneDrive\NTUST_CIT\Lab\Munsell_Reproduction\ICC\NXP_BLUE_2Glossy_GCR.icm";
Epson_icc_path = "C:\Users\cghsi\OneDrive\NTUST_CIT\Lab\Munsell_Reproduction\ICC\epson9700_IT8.7-4 CMYK random_Chart 1617 Patches_08-03-24.icm";

% CMYK value
[C, M, Y, S] = ndgrid(0:0.05:1);
CMYK = [C(:) M(:) Y(:) zeros(size(C(:)))];
CMYKS = [C(:) M(:) Y(:) zeros(size(C(:))) S(:)]; 

% plot area
[handel1, area1, poly1] = plotCMYKGamutArea(CMYKB_icc_path, CMYKS, 'k', '-', 'k', 1.3);


%% Munsell gamut
ref = "C:\Users\cghsi\OneDrive\NTUST_CIT\Lab\Munsell_Reproduction\Dataset_BabelColour_HVC_RGB_Lab_D50\Dataset_BabelColour_HVC_RGB_Lab_D50_50_combine.csv";
toner_4c = "C:\Users\cghsi\OneDrive\NTUST_CIT\Lab\Munsell_Reproduction\SunSui\SunSui_deReport_CSV\4C\4C_50_combined.csv";
toner_4c_b ="C:\Users\cghsi\OneDrive\NTUST_CIT\Lab\Munsell_Reproduction\SunSui\SunSui_deReport_CSV\4C-B_unfinished\4C-B_unfinished_50_combined.csv";
% toner_4c_g = "C:\Users\cghsi\OneDrive\NTUST_CIT\Lab\Munsell_Reproduction\SunSui\SunSui_deReport_CSV\4C-G_unfinished\4C-G_unfinished_50_combined.csv";
% toner_4c_r = "C:\Users\cghsi\OneDrive\NTUST_CIT\Lab\Munsell_Reproduction\SunSui\SunSui_deReport_CSV\4C-R\4C-R_50_combined.csv";
inkjet = "C:\Users\cghsi\OneDrive\NTUST_CIT\Lab\Munsell_Reproduction\Deepblue\NTUST_50_20240315_rgb.csv";

output_filename1 = 'output/vector_length_ref.txt';
output_filename2 = 'output/vector_length_CMYKB.txt';
handel2 = plotPrinterGamut(ref, '#0072BD', 'k', true, output_filename1);
handel3 = plotPrinterGamut(toner_4c_b, '#A2142F','b', false, output_filename2);

legend([handel1, handel2, handel3], {'Kodak CMYKB 色域', 'Munsell 標準資料集', 'Kodak CMYKB 印刷樣本'}, 'Location', 'northeast');


xline(0, 'HandleVisibility', 'off');
yline(0, 'HandleVisibility', 'off')
xlim([-135 135]);
ylim([-120 140]);
xlabel('a*')
ylabel('b*')

grid on

%% funtion helper
function [plotHandle, area, poly] = plotCMYKGamutArea(profile_path, cmyk_values, cfill, line_style, line_color, line_width)
    % Read ICC Profile
    profile = iccread(profile_path);
    cform = makecform("clut", profile, "AToB0");

    % CMYK to Lab
    gamut_lab = applycform(cmyk_values, cform);
    gamut_lab = lab2double(gamut_lab);
    gamut_a = gamut_lab(:, 2);
    gamut_b = gamut_lab(:, 3);

    % Calculate and plot boundary (using fill function)
    b = boundary(gamut_a, gamut_b); 
    plotHandle = fill(gamut_a(b), gamut_b(b), cfill, 'FaceAlpha', 0.2, 'EdgeColor', line_color, 'LineStyle', line_style, 'LineWidth', line_width);
    
    % 將填充區域轉換為多邊形物件
    poly = polyshape(gamut_a(b), gamut_b(b));
    
    % Caculate area
    x = poly.Vertices(:,1);  % 獲取多邊形頂點的 x 坐標
    y = poly.Vertices(:,2);  % 獲取多邊形頂點的 y 坐標
    area = polyarea(x, y);  % 計算面積
end

function result_table = maxCab(data)
    keys = data{:, 1};
    Lab_values = data{:, 7:end};
    Cab_values = sqrt(Lab_values(:, 2).^2 + Lab_values(:, 3).^2);

    unique_keys = unique(keys);
    max_Cab = zeros(length(unique_keys), 1);
    corresponding_Lab = zeros(length(unique_keys), 3);
    
    for i = 1:length(unique_keys)
        key = unique_keys{i};
        idx = strcmp(keys, key);  % find the correspond index of key
        [max_Cab(i), max_idx] = max(Cab_values(idx));  % find the correspond index of max cab
        corresponding_Lab(i, :) = Lab_values(find(idx, 1) + max_idx - 1, :);  % correspond lab value
    end
    
    result_table = table(unique_keys, max_Cab, corresponding_Lab);
end

function plotHandle = plotPrinterGamut(dataPath, mFaceColor, lineColor, add_text, output_filename)
    data = readtable(dataPath, 'HeaderLines', 1);
    
    cabTable = maxCab(data);
    
    key_name = cabTable(:, 'unique_keys');
    key_name = table2cell(key_name); % Convert table to cell array for text labels
    max_lab = cabTable(:, 'corresponding_Lab');
    max_lab = table2array(max_lab);
    max_lab = lab2double(max_lab);

    gamut_a = max_lab(:, 2);
    gamut_b = max_lab(:, 3);

    % Calculate boundary
    k = boundary(gamut_a, gamut_b);
    
    % Prepare to store vector lengths and key names
    vector_lengths = zeros(length(k), 1);
    key_vector_lengths = cell(length(k), 1);

    hold on;
    
    % Draw lines from the origin to each boundary point
    origin = [0, 0];
    for i = 1:length(k)
        a = gamut_a(k(i));
        b = gamut_b(k(i));

        plotHandle = scatter(a, b, 'filled', 'o', MarkerFaceColor=mFaceColor);

        plot([origin(1), a], [origin(2), b],Color=mFaceColor, LineStyle=':',LineWidth=1.3);
        
        % Calculate vector length
        vector_length = sqrt(a^2 + b^2);
        vector_lengths(i) = vector_length;
        key_vector_lengths{i} = sprintf('%s: %.2f', key_name{k(i)}, vector_length);
        
        % Calculate angle of the line
        angle = atan2d(b - origin(2), a - origin(1));
        
        % Adjust rotation for the third boundary line (if condition met)
        if a < 0 && b < 20
            angle = angle + 180; % Rotate by 180 degrees
        end
        
        % Add text label near the boundary point if add_text is true
        if add_text
            if a < 0 && b < 20
                text(a, b, key_name{k(i)} + "   ", 'VerticalAlignment', 'middle', ...
                    'HorizontalAlignment', 'right', 'FontSize', 10, ...
                    'Color', lineColor, 'Rotation', angle);
            else    
                text(a, b, "   "+key_name{k(i)}, 'VerticalAlignment', 'middle', ...
                    'HorizontalAlignment', 'left', 'FontSize', 10, ...
                    'Color', lineColor, 'Rotation', angle);
            end
        end
    end
    hold off;
    
    % Write vector lengths and key names to a text file
    fid = fopen(output_filename, 'w');
    for i = 1:length(key_vector_lengths)
        fprintf(fid, '%s\n', key_vector_lengths{i});
    end
    fclose(fid);
end







