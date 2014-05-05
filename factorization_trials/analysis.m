%% Summary:
% Method 3. Use factorization model with mean and business bias but no user
% bias
%
% Assumption: users have too few ratings and therefore estimating user bias
% based on the ratings is dangerous
%
% Details:
%   - do 9-fold cross-validation for 3 values of lambda and 3 values of
%   rank
%   - pick best one and fit model to all training data
%   - calculate error

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

lambda = [0.1,0.5,1.0];
numlf = [10,30,50];
lrate = [0.15,0.10,0.05];

ratings = ratings0+ratings1+ratings2+ratings3+...
          ratings4+ratings5+ratings6+ratings7+...
          ratings8;


% cross validation
count = 0;
minmse = 1000;
minmae = 1000;
b_lambda = 0;
b_numlf = 0;
for l=1:size(lambda,2)
    for k=1:size(numlf,2)
        training = ratings-eval(strcat('ratings',num2str(count)));
        cvtest = eval(strcat('ratings',num2str(count)));
        [U,B,mymu,bb] = factorize_no_user_bias(training,numlf(k),lambda(l),lrate(k),50);
        predictions = predict_no_user_bias(cvtest,U,B,mymu,bb);
        lambda(l)
        numlf(k)
        [mse,mae] = calculate_error(predictions,cvtest)
        if (mae<minmae)
            b_lambda = lambda(l);
            b_numlf = numlf(k);
            minmae = mae;
        end
        count = count+1;
    end
end

[U,B,mymu,bb] = factorize_no_user_bias(ratings,b_numlf,b_lambda,0.1,60);
predictions = predict_no_user_bias(test,U,B,mymu,bb);
[mse,mae] = calculate_error(test,predictions)

% cluster businesses
bclusters = kmeans(bb,5);

% factorize on individually clustered ratings matrix
c_ratings1 = ratings(:,bclusters==1);
c_ratings2 = ratings(:,bclusters==2);
c_ratings3 = ratings(:,bclusters==3);
c_ratings4 = ratings(:,bclusters==4);
c_ratings5 = ratings(:,bclusters==5);
c_test1 = test(:,bclusters==1);
c_test2 = test(:,bclusters==2);
c_test3 = test(:,bclusters==3);
c_test4 = test(:,bclusters==4);
c_test5 = test(:,bclusters==5);

for i=1:5
    disp(strcat('Cluster ',num2str(i)));
    [c_U,c_B,c_mymu,c_bb] = factorize_no_user_bias(eval(strcat('c_ratings',num2str(i))),...
        b_numlf,b_lambda,0.1,60);
    predictions = predict_no_user_bias(eval(strcat('c_','test',num2str(i))),c_U,c_B,c_mymu,c_bb);
    [mse,mae] = calculate_error(eval(strcat('c_','test',num2str(i))),predictions)
end



