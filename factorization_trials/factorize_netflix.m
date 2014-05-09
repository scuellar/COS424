% solves eq. 5 in Y. Koren's paper (factorization with biases)

function [W,H,user_mean_offsets,bus_mean_ratings] = factorize_netflix(ratings,k,lambda,lrate,maxiter)

% find nonzeros
[rows,cols,vals] = find(ratings);
sz = size(rows);
len = sz(1);                % number of nonzero elements
% initialize factorized matrices
[nUsers,nBus] = size(ratings);
W = zeros(nUsers,k);
H = zeros(k,nBus);
% initialize error vector
err = zeros(len,1);

% global average rating
global_average = sum(sum(ratings))/len;
% number of ratings each user made
user_num_ratings = sum(ratings~=0,2);
% business average ratings (accounting for priors)
bus_num_ratings = sum(ratings~=0,1);
bus_mean_ratings = sum(ratings,1)./bus_num_ratings;
bus_mean_ratings(isnan(bus_mean_ratings))=0;
var_ratio = var(vals)/var(bus_mean_ratings);
bus_mean_ratings = (global_average*var_ratio+sum(ratings,1))./(var_ratio+bus_num_ratings);
% get user average offsets from mean
user_mean_offsets = zeros(size(user_num_ratings));
for i=1:nBus
    % get average user offsets from movie averages
    ind = ratings(:,i)~=0;
    user_mean_offsets(ind) = user_mean_offsets(ind)+ratings(ind,i)-bus_mean_ratings(i);
end
user_mean_offsets(isnan(user_mean_offsets))=0;
offset_avg = mean(user_mean_offsets);
user_mean_offsets = (offset_avg*var_ratio+user_mean_offsets)./(var_ratio+user_num_ratings);
% fix NaNs
user_mean_offsets(isnan(user_mean_offsets)) = 0;
bus_mean_ratings(isnan(bus_mean_ratings)) = global_average;

% optimize each feature
for f=1:k
    W(:,f) = 0.1*ones(nUsers,1);
    H(f,:) = 0.1*ones(1,nBus);
    % do a bunch of iterations
    for i=1:maxiter
        % run though all nonzero points
        for j=1:len
            row = rows(j);
            col = cols(j);
            rating = vals(j);
            err(j) = rating-(bus_mean_ratings(col)+user_mean_offsets(row)+W(row,:)*H(:,col));
            wv = W(row,f);
            W(row,f) = W(row,f)+lrate*(err(j)*H(f,col)-lambda*W(row,f));
            H(f,col) = H(f,col)+lrate*(err(j)*wv-lambda*H(f,col));
        end
        norm(err)
    end
    f
end

end