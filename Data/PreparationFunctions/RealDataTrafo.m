%function surface_generator(year,stock_ind,Strikes,Maturity,path,bound,plot,vecormat,saver,volaprice,method)
close all;
path = '/Users/User/Documents/GitHub/SeminarOptions/Data/Datasets';
%path ='/Users/Lukas/Documents/GitHub/SeminarOptions/Data/Datasets';
stock_ind = 'SP500';
Strikes = 0.9:0.02:1.1;
Maturity = 30:30:240;
Nstrikes = length(Strikes);
Nmaturities = length(Maturity);
S0 = 1;
r = 0.005;
bound =[100,100];
for years = 2010:2015
    surface = surface_generator(years,stock_ind,Strikes,Maturity,path,bound,1,1,1,0,'linear');
end
%%
dates =SP500_date_prices_returns(1,:); 
log_returns= log(1+SP500_date_prices_returns(3,:));
dates =year(datetime(dates,'ConvertFrom','datenum'));
i = 1;
vola = zeros(6,1);
bs_prices = zeros(Nstrikes,Nmaturities);
bs = zeros(6,Nstrikes*Nmaturities);
for years = 2010:2015
    logr = log_returns(dates==years);
    vola(i) = sqrt(252*var(logr));
    for t = 1:Nmaturities
        for k = 1:Nstrikes
            [bs_prices(k,t),~] = blsprice(S0, Strikes(k),r,Maturity(t)/252,vola(i));
        end
    end
    bs(i,:) = reshape(bs_prices,[1,Nmaturities*Nstrikes]);
    i=i+1;
end
save('bs_prices','bs')
save('vola','vola')