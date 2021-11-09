clear all;
table = load('原始指标数据.txt');
table = table(2:403, 2:11);
table_standard = zscore(table);
P = cov(table_standard);
[M,D] = eig(P);
d = diag(D);
S_eig = sort(d,'descend');
m = fliplr(M);
i = 0;
j = 0;
% 重要性排序后从大到小找到加和第一次超过93%所需的特征值个数
while i/sum(S_eig) < 0.93
    j = j + 1;
    i = i + S_eig(j);
end
[pc,latent,explained] = pcacov(P);
num = 5;
pc = pc.*(sign(sum(pc)));
dataframe = P * pc(:,[1:num]);
total_score = dataframe * explained(1:num)/100;
% 计算主成分得分并按照降序排列
[descend_score , number] = sort(total_score,'descend');
descend_score = descend_score';
number = number';
