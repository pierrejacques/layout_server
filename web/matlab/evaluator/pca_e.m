k = 0.95; % �趨���������ֵ

[pc,score,latent] = princomp(features);
topK = 0;

for i=1:length(latent)
    if(sum(latent(1:i))/sum(latent)>k)
        sum(latent(1:i))/sum(latent)
        topK = i;
        break;
    end
end

topK
convertM = pc(:,1:topK);

PCAFeatures = features * convertM;
