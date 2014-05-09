function [predictions] = predict_netflix_avg(test,bu,bb)

% find nonzeros
[rows,cols,vals] = find(test);
sz = size(rows);
len = sz(1);

predictions = sparse(rows,cols,zeros(len,1));

for i=1:len
   row = rows(i);
   col = cols(i);
   
   predictions(row,col) = max(1,min(5,bu(row)+bb(col))); 
end

predictions;

end