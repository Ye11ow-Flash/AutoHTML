#include<bits/stdc++.h>

int main(){

	int n,i,j;
	char f[2001][2001];
	vector<int> v[2001];
	scanf("%d",&n);
	for(i=0;i<n;i++){
		scanf("%s",f[i]);
	}
	for(i=0;i<n;i++){
		for(j=i+1;j<n;j++){
			if(f[i][j] == '1'){
				v[i].push_back(j);
				v[j].push_back(i);
			}
		}
	}
	int count=0;
	for(i=0;i<n;i++){
		for(j=i+1;j<n;j++){
			if (f[i][j] == '0')
			{
				for(int u: v[i]){
					if(g[u][j] == '1'){
						count+=2;
						break;
					}
				}
			}
		}
	}
	printf("%d",count);
	return 0;
}