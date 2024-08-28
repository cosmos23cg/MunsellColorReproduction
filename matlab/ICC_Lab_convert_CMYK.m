% This script used to read the Lab data and then convert it to CMYK using
% an ICC profile. Save the CMYK file as csv.

clear;
clc;


lab_path = "C:\Users\cghsi\OneDrive\NTUST_CIT\Lab\Munsell_reproduction\Dataset_BabelColour_HVC_RGB_Lab_D50\Dataset_BabelColour_HVC_RGB_Lab_D50_50_combine.csv";
data_table = readtable(lab_path);
lab_data = data_table{:, 7:9};  % Extract the Lab columns as a numeric array

% ICC profile path
% CMYK_icc_path = "C:\Users\cghsi\OneDrive\NTUST_CIT\Lab\Munsell_Reproduction\ICC\NXP_CMYK_2Glossy_GCR.icm";
% CMYKB_icc_path = "C:\Users\cghsi\OneDrive\NTUST_CIT\Lab\Munsell_Reproduction\ICC\NXP_BLUE_2Glossy_GCR.icm";
Epson_icc_path = "C:\Users\cghsi\OneDrive\NTUST_CIT\Lab\Munsell_Reproduction\ICC\epson9700_IT8.7-4 CMYK random_Chart 1617 Patches_08-03-24.icm";

cmyk_data = cvtLab2CMYK(Epson_icc_path, lab_data);

header = data_table(:, 1:3);
combined_data = [header array2table(cmyk_data) array2table(lab_data)];
writetable(combined_data, 'EPSON.csv')


function cmyk_data = cvtLab2CMYK(profile_path, Lab_data)
    profile = iccread(profile_path);
    cform = makecform("clut", profile, "BToA0"); % PCS to device: perceptual rendering intent
    cmyk_data = applycform(Lab_data, cform);
end