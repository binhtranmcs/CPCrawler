#include<bits/stdc++.h>
using namespace std;
const int N = 2e5+5;
const int G = 3;
const int mod = 998244353;
 
int fac[N],rev[N];
 
int qpow(int a,int b){
	int r=1;
	while(b){
		if(b&1)r=1ll*r*a%mod;
		b>>=1;a=1ll*a*a%mod; 
	}
	return r;
}
 
struct NTT{
	int n,m,rev[N<<1];
	int a[N<<1],b[N<<1];
	
	void init(int len){
		for(n=1,m=0;n<=len;n<<=1,m++);
		for(int i=0;i<n;++i){
			rev[i]=rev[i>>1]>>1|(1&i)<<(m-1);
			a[i]=b[i]=0;
		}
	}
	
	void FFT(int *a,int f){
		for(int i=0;i<n;++i)if(i<rev[i])swap(a[i],a[rev[i]]);
		for(int i=1;i<n;i<<=1){
			int wn=qpow(G,(mod-1)/(i<<1));
			if(f==-1)wn=qpow(wn,mod-2);
			for(int j=0;j<n;j+=i<<1){
				int w=1;
				for(int k=0;k<i;++k,w=1ll*w*wn%mod){
					int x=a[j+k],y=1ll*a[j+k+i]*w%mod;
					a[j+k]=(x+y)%mod;a[j+k+i]=(x-y+mod)%mod;
				} 
			}
		}
		if(f==-1){
			int rn=qpow(n,mod-2);
			for(int i=0;i<n;++i)a[i]=1ll*a[i]*rn%mod;
		}
	}
	
	void work(){
		FFT(a,1);FFT(b,1);
		for(int i=0;i<n;++i)a[i]=1ll*a[i]*b[i]%mod;
		FFT(a,-1);
	}
}B;
 
void init(){
	fac[0]=1;
	for(int i=1;i<N;++i)fac[i]=1ll*fac[i-1]*i%mod;
	rev[N-1]=qpow(fac[N-1],mod-2);
	for(int i=N-2;~i;--i)rev[i]=1ll*rev[i+1]*(i+1)%mod;
}
 
int C(int n,int m){
	if(n<m||m<0)return 0;
	return 1ll*fac[n]*rev[m]%mod*rev[n-m]%mod;
}
 
int n,ans[N];
 
int main(){
	init();
	cin>>n;
	int len=0;
	ans[0]=1;
	for(int i=1,a,b;i<=n;++i){
		cin>>a>>b;
		B.init(2*len+a-b);
		for(int k=-len;k<=len+a-b;++k)B.a[k+len]=C(a+b,b+k);
		for(int j=0;j<=len;++j)B.b[j]=ans[j];
		B.work();
		for(int k=0;k<=len+a-b;++k){
			ans[k]=B.a[k+len];
		}
		len+=a-b;
	}
	int res=0;
	for(int i=0;i<=len;++i)(res+=ans[i])%=mod;
	cout<<res<<endl;
}
 	   	      			 		 	  		 		  		