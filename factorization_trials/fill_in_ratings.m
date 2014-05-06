function [ratings_f] = fill_in_ratings(ratings,num)

n_bus = size(ratings,2);

mask = ratings~=0;
n_bratings = sum(mask,1);
n_uratings = sum(mask,2);
avg_bratings = sum(ratings,1)./n_bratings;

user_ind = n_uratings < num;

[rows,cols,vals] = find(user_ind);
ratings_f = ratings;

for row=1:size(rows,1)
    ind = randi([1 n_bus],1,num);
    ratings_f(rows(row),ind) = avg_bratings(ind);
    if mod(row,5000)==0
        row
    end
end

ratings_f;

end