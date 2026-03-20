function stop = optim_out(x,~,state)
persistent ph
global x0
global xEND
global fun
global custom_domain_range

if isempty(custom_domain_range)
    % Użyj domyślnej wartości, jeśli zmienna nie została wcześniej ustawiona
    domain_range = [-2, 2;  -1, 3];
else
    domain_range = custom_domain_range;
end

stop = false;
switch state
    case 'init'
       newplot
       xx = domain_range(1, 1):.2:domain_range(1, 2);
       yy = domain_range(2, 1):.2:domain_range(2, 2);
       [xx,yy] = meshgrid(xx,yy);
       zz = zeros(size(xx));
       for xi=1:size(xx, 1)
            for yi=1:size(xx, 2)
                x_coord = xx(xi, yi);
                y_coord = yy(xi, yi);
                zz(xi, yi) = fun([x_coord, y_coord]);
            end
       end
       % Set up the appropriate colormap
       % In this case, the colormap has been chosen to give the surf plot
       % a nice healthy banana color.
       hsv2 = hsv;  % hsv, hot, cool, pink, parula, spring, summer, autumn, winter, jet
     % hsv2 = hsv2(end:-1:1,:);
       hsv3 = [hsv2(11:64,:); hsv2(1:10,:)];
     % hsv3 = hsv2; [hsv2(24:-1:1,:); hsv2(64:-1:25,:)];

       % draw the surf plot
       surface(xx,yy,zz,'EdgeColor',[0.8,0.8,0.8]);
       xlabel 'x(1)'
       ylabel 'x(2)'
       view(10,55);
       colormap(hsv3);
       hold on;
       [~,contHndl] = contour3(xx,yy,zz,[100,500],'k');
       contHndl.Color = [0.8,0.8,0.8];
       
       if(1) % BLACK
          plot3(x0(1),x0(2),fun(x0),'ko','MarkerSize',15,'LineWidth',2);
          text(x0(1),x0(2)+0.5,267.62,'   Start','Color',[0 0 0]);
          plot3(xEND(1),xEND(2),fun(xEND),'ko','MarkerSize',15,'LineWidth',2);
          text(xEND(1),xEND(2)+0.5,fun(xEND),'   Solution','Color',[0 0 0]);
       else % WHITE
          plot3(x0(1),x0(2),fun(x0),'wo','MarkerSize',15,'LineWidth',2);
          text(x0(1),x0(2)+0.5,fun(x0),'   Start','Color',[1 1 1]);
          plot3(xEND(1),xEND(2),fun(xEND),'wo','MarkerSize',15,'LineWidth',2);
          text(xEND(1),xEND(2)+0.5,fun(xEND),'   Solution','Color',[1 1 1]);
       end    
       drawnow

    case 'iter'
        x1 = x(1);
        y1 = x(2);
        z1 = fun([x1, y1]);
        if(1) % RED CIRCLE
           ph = plot3(x1,y1,z1,'r.','MarkerSize',25);
        else  % YELLOW CIRCLE
           ph = plot3(x1,y1,z1,'y.','MarkerSize',25);
        end    
        h = gca;
        h.SortMethod = 'childorder';
        drawnow;
        
    case 'done'
        legend(ph,'Iterative steps','Location','east')
        hold off
end