clc; clear all; close all

theta = pi/4
R2D = [cos(theta), -sin(theta); sin(theta) cos(theta)]

przes = [1, 0];
P2D = [-1, -1;
    1, -1;
    1, 1;
    -1, 1;
    -1, -1 ];

P2D = P2D + przes

figure();
plot(P2D(:, 1), P2D(:, 2), "bo-", "MarkerSize", 12)
xlim([-2, 2])
ylim([-2, 2])
axis square
hold on;

obroconeP = (R2D * P2D')';

plot(obroconeP(:, 1), obroconeP(:, 2), "ro-", "MarkerSize", 12)
plot(0, 0, "w+", "MarkerSize", 10)


%% 3D
figure();

rotX = 0 %pi/4
rotY = 0 %pi/4
rotZ = pi/4

R3Dx = [1, 0, 0;
        0, cos(rotX), -sin(rotX);
        0, sin(rotX), cos(rotX)];

R3Dy = [cos(rotY), 0, sin(rotY);
        0, 1, 0;
        -sin(rotY), 0, cos(rotY)];

R3Dz = [cos(rotZ), -sin(rotZ), 0;
      sin(rotZ), cos(rotZ), 0;
      0, 0, 1];

P3D = [-1, -1, -1; 
        1, -1, -1; 
        1,  1, -1;
       -1,  1, -1;
       -1, -1, -1;

       -1, -1,  1;
        1, -1,  1;
        1,  1,  1;
       -1,  1,  1;
       -1, -1,  1;

       -1, -1,  1;
       -1, -1,  -1;

       1, -1,  1;
       1,  -1, -1;

       1,  1,  1;
       1,  1,  -1;

       -1, 1, 1;
       -1, 1, -1;

       -1, -1, 1;
       ];

plot3(P3D(:, 1), P3D(:, 2), -P3D(:, 3), "b.-");
% xlim([[-2, 2]]);
% ylim([[-2, 2]]);
% zlim([[-2, 2]]);
hold on;

obrP3D = (R3Dx * R3Dy * R3Dz * P3D')'

plot3(obrP3D(:, 1), obrP3D(:, 2), -obrP3D(:, 3), "r.-");
% xlim([[-2, 2]]);
% ylim([[-2, 2]]);
% zlim([[-2, 2]]);
xlabel("x");
ylabel("y");
zlabel("z");
axis equal;

% biala linia
plot3([0,0], [0,0], [-2,2], "w-");