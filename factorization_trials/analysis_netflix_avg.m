clear;clc;

k = 9;     % k-fold cross validation

ratings0 = mm_to_msm('ratings0.mtx');
ratings1 = mm_to_msm('ratings1.mtx');
ratings2 = mm_to_msm('ratings2.mtx');
ratings3 = mm_to_msm('ratings3.mtx');
ratings4 = mm_to_msm('ratings4.mtx');
ratings5 = mm_to_msm('ratings5.mtx');
ratings6 = mm_to_msm('ratings6.mtx');
ratings7 = mm_to_msm('ratings7.mtx');
ratings8 = mm_to_msm('ratings8.mtx');
test = mm_to_msm('ratings9.mtx');

ratings = ratings0+ratings1+ratings2+ratings3+...
          ratings4+ratings5+ratings6+ratings7+...
          ratings8;
      
% find nonzeros
[rows,cols,vals] = find(ratings);
sz = size(rows);
len = sz(1);                % number of nonzero elements
[nUsers,nBus] = size(ratings);
err = zeros(len,1);
      
mask = ratings~=0;

for var_ratio=1:25
    
    % global average rating
    global_average = sum(sum(ratings))/len;
    % number of ratings each user made
    user_num_ratings = sum(ratings~=0,2);
    % business average ratings (accounting for priors)
    bus_num_ratings = sum(ratings~=0,1);
    bus_mean_ratings = sum(ratings,1)./bus_num_ratings;
    bus_mean_ratings(isnan(bus_mean_ratings))=0;
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
    
    predictions = predict_netflix_avg(test,user_mean_offsets,bus_mean_ratings);
    [mse,mae] = calculate_error(test,predictions)

end