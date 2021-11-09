clc
clear

%% 求解供应商周期内每周最大供货能力
load('Q.mat')
[m, n] = size(Q);

C = [];
for r = 1:m
    R = reshape(Q(r, :), [24, 10])';
    Avg = [];
    for col = 1:24
        Col = R(:, col);
        avg = mean(maxk(Col, 2));
        Avg(end+1) = avg;
    end
    C = [C; Avg];
end

%% 求解供应商周期内每周平均供货能力
load('D.mat')

C = [];
for r = 1:m
    R1 = reshape(Q(r, :), [24, 10])';
    R2 = reshape(D(r, :), [24, 10])';
    Avg = [];
    for col = 1:24
        Col1 = R1(:, col);
        Col2 = R2(:, col);
        if sum(Col2 > 0) == 0
            avg = 0
        else
            avg = sum(Col1) / sum(Col2 > 0);
        end
        Avg(end+1) = avg;
    end
    C = [C; Avg];
end
