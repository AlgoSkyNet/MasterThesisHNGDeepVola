clearvars
load('/Users/Lukas/Documents/GitHub/SeminarOptions/Data/Datasets/SP500/SP500_date_prices_returns.mat');
load('/Users/Lukas/Documents/GitHub/SeminarOptions/Data/Datasets/SP500/Calls2015.mat');
SP500_dates1 = datetime(SP500_date_prices_returns(1,:),'ConvertFrom','datenum');
SP500_dates1.Format = 'dd.MM.yyyy';
%SP500_year = year(SP500_dates);
SP500_dates = SP500_date_prices_returns(1,:);
SP500_year = year(SP500_dates1);

SP500_prices(1,:) = SP500_date_prices_returns(2,:);
%SP500_logreturns(1,:) = zeros(size(SP500_date_prices_returns(2,:)));
%SP500_logreturns(1,2:end) = log(SP500_date_prices_returns(2,2:end)./...
%    SP500_date_prices_returns(2,1:end-1));
SP500_returns(1,:) = SP500_date_prices_returns(3,:);

SP500 = struct;
SP500.date = SP500_dates';
SP500.year = SP500_year';
SP500.price = SP500_prices';
SP500.returns = SP500_returns';
%SP500.logreturn = SP500_logreturns';
writetable(struct2table(SP500), 'SP500_data_1.txt')