function OptionPrice=HestonNandi1(S_0,X,Sig_,T,r)

OptionPrice=.5*S_0+(exp(-r*T)/pi)*quad(@Integrand1,eps,100)-X*exp(-r*T)*(.5+(1/pi)*quad(@Integrand2,eps,100));
    % function Integrand1 and Integrand2 return the values inside the 
    % first and the second integrals
    
    function f1=Integrand1(phi)
        f1=real((X.^(-i*phi).*charac_fun(i*phi+1))./(i*phi));
    end

    function f2=Integrand2(phi)
        f2=real((X.^(-i*phi).*charac_fun(i*phi))./(i*phi));
    end

    % function that returns the value for the characteristic function
    function f=charac_fun(phi)
        f = 2;
%         phi=phi';    % the input has to be a row vector
%         % GARCH parameters
%         lam=2;
%         lam_=-.5;                   % risk neutral version of lambda
%         a=.000005;
%         b=.85;
%         g=150;                      % gamma coefficient
%         g_=g+lam+.5;                % risk neutral version of gamma
%         w=Sig_*(1-b-a*g^2)-a;       % GARCH intercept
%         
%         % recursion for calculating A(t,T,Phi)=A_ and B(t,T,Phi)=B_
%         A(:,T-1)=phi.*r;
%         B(:,T-1)=lam_.*phi+.5*phi.^2;
%         
%         for i=2:T-1
%             A(:,T-i)=A(:,T-i+1)+phi.*r+B(:,T-i+1).*w-.5*log(1-2*a.*B(:,T-i+1));
%             B(:,T-i)=phi.*(lam_+g_)-.5*g_^2+b.*B(:,T-i+1)+.5.*(phi-g_).^2./(1-2.*a.*B(:,T-i+1));
%         end
% 
%         A_=A(:,1)+phi.*r+B(:,1).*w-.5*log(1-2.*a.*B(:,1));                    % A(t;T,phi)
%         B_=phi.*(lam_+g_)-.5*g_^2+b.*B(:,1)+.5*(phi-g_).^2./(1-2.*a.*B(:,1)); % B(t;T,phi)
% 
%         f=S_0.^phi.*exp(A_+B_.*Sig_);
%         f=f'; % the output is a row vector

    end

end




