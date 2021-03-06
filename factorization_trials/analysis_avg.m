%% Summary:
% Method 5. Use weighted averages to guess rating
% 
% Details: 
%   - for each user, get its average rating
%   - for each business, get its average rating
%   - predict rating(u,b) by taking convex combination of average user
%   rating for user u and average business rating for business b
%   - weights are the number of ratings for that user/business over the
%   total number of ratings for that test point


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
      
mask = ratings~=0;

% ==== Select only users and businesses with more than 2 ratings
% us = sum(mask,2);
% us_ind = us>2;
% ratings0 = ratings0(us_ind,:);
% ratings1 = ratings1(us_ind,:);
% ratings2 = ratings2(us_ind,:);
% ratings3 = ratings3(us_ind,:);
% ratings4 = ratings4(us_ind,:);
% ratings5 = ratings5(us_ind,:);
% ratings6 = ratings6(us_ind,:);
% ratings7 = ratings7(us_ind,:);
% ratings8 = ratings8(us_ind,:);
% ratings = ratings0+ratings1+ratings2+ratings3+...
%           ratings4+ratings5+ratings6+ratings7+...
%           ratings8;
% test = test(us_ind,:);
% bu = sum(mask,1);
% bu_ind = bu>2;
% ratings0 = ratings0(:,bu_ind);
% ratings1 = ratings1(:,bu_ind);
% ratings2 = ratings2(:,bu_ind);
% ratings3 = ratings3(:,bu_ind);
% ratings4 = ratings4(:,bu_ind);
% ratings5 = ratings5(:,bu_ind);
% ratings6 = ratings6(:,bu_ind);
% ratings7 = ratings7(:,bu_ind);
% ratings8 = ratings8(:,bu_ind);
% ratings = ratings0+ratings1+ratings2+ratings3+...
%           ratings4+ratings5+ratings6+ratings7+...
%           ratings8;
% test = test(:,bu_ind);
% mask = ratings~=0;

n_bus = sum(mask,1);
n_users = sum(mask,2);
bus = sum(ratings,1)./n_bus;
users = sum(ratings,2)./n_users;
users(isnan(users))=0;
bus(isnan(bus))=0;
tmean = sum(sum(ratings))/size(nonzeros(ratings),1);

users = users.*n_users;
bus = bus.*n_bus;


% make predictions
[rows,cols,vals] = find(test);
pred_vals = zeros(size(rows,1),1);
% assign predictions to each test point
for i=1:size(vals,1)
    row = rows(i); col = cols(i);
    % if there are no training ratings for this user and business
    % simply assign the overall mean value
    if (n_bus(col)==0) && (n_users(row)==0)
        pred_vals(i) = tmean;
    % otherwise, assign weighted average of user rating and business rating
    else
        num = n_users(row)+n_bus(col);
        pred_vals(i) = (users(row)+bus(col))/num;
    end
end
predictions = sparse(rows,cols,pred_vals);

% calculate error
[mse,mae] = calculate_error(test,predictions)





