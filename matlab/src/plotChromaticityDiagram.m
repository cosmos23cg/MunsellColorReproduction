function plotChromaticityDiagram(colorspace)
    % plotChromaticityDiagram plots the chromaticity diagram for a given color space.
    %
    % Parameters:
    %   colorspace (string): The color space to be used for plotting the chromaticity diagram.
    %                        Accepted values are 'uv', 'xy', or any other supported color space.
    %
    % This function uses the built-in plotChromaticity function to plot the chromaticity diagram
    % based on the specified color space. It then overlays a semi-transparent white mask to
    % improve visualization and adjusts the plot limits to fit the diagram tightly.
    %
    % Example:
    %   plotChromaticityDiagram('uv');

    plotChromaticity('ColorSpace',colorspace);
    
    axis tight;
    ax = gca;
    xLimits = ax.XLim;
    yLimits = ax.YLim;
    
    % apply a alpha mask
    fill([xLimits(1) xLimits(2) xLimits(2) xLimits(1)], ...
         [yLimits(1) yLimits(1) yLimits(2) yLimits(2)], ...
         'w', 'FaceAlpha', 0.5, 'EdgeColor', 'none');
end
