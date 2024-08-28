% This script plot the ICC gamut in a*b* diagram, splitting L* from 10 to 90
% in steps of 10

clear;
clc;

figure("Units","inches","Position",[1,1,8,8]);
hold on;

% ICC profile path
iso_icc_path = "C:\Users\cghsi\OneDrive\NTUST_CIT\Lab\Munsell_Reproduction\ICC\PSOcoated_v3.icc";
CMYK_icc_path = "C:\Users\cghsi\OneDrive\NTUST_CIT\Lab\Munsell_Reproduction\ICC\NXP_CMYK_2Glossy_GCR.icm";
CMYKB_icc_path = "C:\Users\cghsi\OneDrive\NTUST_CIT\Lab\Munsell_Reproduction\ICC\NXP_BLUE_2Glossy_GCR.icm";
Epson_icc_path = "C:\Users\cghsi\OneDrive\NTUST_CIT\Lab\Munsell_Reproduction\ICC\epson9700_IT8.7-4 CMYK random_Chart 1617 Patches_08-03-24.icm";

% CMYK value
[C, M, Y, S] = ndgrid(0:0.05:1);
CMYK = [C(:) M(:) Y(:) zeros(size(C(:)))];
CMYKS = [C(:) M(:) Y(:) zeros(size(C(:))) S(:)]; 

L_values = 10:10:90;  % L* values from 10 to 90

% Plotting
plot_handles = [];
for i = 1:length(L_values)
    L_star = L_values(i);
    
    subplot(3, 3, i);  % Create a subplot grid of 3x3
    hold on;
    title(['L* = ', num2str(L_star)]);
    
    % Plot CMYK Gamut Area for L* = L_star
    [handle1] = plotCMYKGamutAreaAtL(iso_icc_path, CMYK, 'k', '-', 'k', 1.3, L_star);
    [handle2] = plotCMYKGamutAreaAtL(Epson_icc_path, CMYK, 'b', '--', 'b', 1.3, L_star);
    
    % Axis settings
    xlim([-128 128]);
    ylim([-128 128]);
    grid on;
    xlabel('a*');
    ylabel('b*');
    
    % Collect plot handles for legend
    if i == 2
        plot_handles = [handle1, handle2];
    end
end

% Create a separate axis for the legend
legendSetting(plot_handles, 'ISO 12647', 'EPSON 9900')


%% Helper function: Plot CMYK Gamut Area at L*
function [plotHandle] = plotCMYKGamutAreaAtL(profile_path, cmyk_values, cfill, line_style, line_color, line_width, L_star)
    profile = iccread(profile_path); % Read ICC Profile

    % CMYK to Lab
    cform = makecform("clut", profile, "AToB0");
    gamut_lab = applycform(cmyk_values, cform);
    gamut_lab = lab2double(gamut_lab);

    % Filter by L* value
    idx = abs(gamut_lab(:, 1) - L_star) < 5;  % Filter within ±5 of L* value
    gamut_a = gamut_lab(idx, 2);
    gamut_b = gamut_lab(idx, 3);
    
    % Calculate and plot boundary (using fill function)
    b = boundary(gamut_a, gamut_b); 
    plotHandle = fill(gamut_a(b), gamut_b(b), cfill, 'FaceAlpha', 0.3, 'EdgeColor', line_color, 'LineStyle', line_style, 'LineWidth', line_width);
end

%% Helper function: Legend settings
function legendSetting(legend_handles, lable1, lable2)
    legend_axis = axes('Position', [0 0.95 1 0.05], 'Box', 'off', 'XTick', [], 'YTick', [], 'Color', 'none');
    legend(legend_axis, legend_handles, {lable1, lable2}, 'Location', 'northoutside', 'Orientation', 'horizontal', 'FontSize', 10);
    legend_axis.Visible = 'off';
end
