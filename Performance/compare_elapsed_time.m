clear;clc
close all

%%
data = dlmread('full/time-particles.dat');
n = data(:,1);
t = data(:,2);

semilogx(n,t,'-o','DisplayName','Full')
hold on 

%%
data = dlmread('no-cpl/time-particles.dat');
n = data(:,1);
t = data(:,2);

loglog(n,t,'-s','DisplayName','No coupling')
hold on 

%%
data = dlmread('no-pp/time-particles.dat');
n = data(:,1);
t = data(:,2);

loglog(n,t,'-^','DisplayName','No particle-particle')
hold on 

%%
legend Location best
