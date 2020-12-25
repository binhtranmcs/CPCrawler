for s in[*open(0)][2::2]:
 a=s.split();n=len(a)-1;i=0
 while 2*i<=n:print(a[i],('',a[~i])[2*i<n]);i+=1