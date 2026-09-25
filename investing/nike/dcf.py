# Nike (NKE) 3-scenario DCF. Units: $B except per-share. Price/as-of: $36, Sep 2026.
# Run: python3 dcf.py
REV0=46.4; NETDEBT=2.0; SH=1.48; PRICE=36.0
S={
 "Bear":dict(g=[-.03,.01,.02,.02,.02],m=[.05,.06,.065,.07,.075],tg=.02,w=.095,div=[1.64,0.80,0.80,0.80,0.80],shr=0.0),
 "Base":dict(g=[-.01,.02,.04,.04,.04],m=[.055,.07,.085,.095,.10],tg=.03,w=.09,div=[1.64,1.68,1.72,1.76,1.80],shr=.005),
 "Bull":dict(g=[.01,.06,.07,.07,.06],m=[.065,.09,.11,.12,.125],tg=.035,w=.085,div=[1.64,1.72,1.80,1.90,2.00],shr=.015),
}
res={}
for k,s in S.items():
    r=REV0; pv=0; rows=[]
    for i in range(5):
        r*=1+s['g'][i]; f=r*s['m'][i]; pv+=f/(1+s['w'])**(i+1); rows.append((round(r,1),round(f,2)))
    tv=f*(1+s['tg'])/(s['w']-s['tg'])
    ev=pv+tv/(1+s['w'])**5
    sh5=SH*(1-s['shr'])**5
    iv=(ev-NETDEBT)/SH
    p5=(tv-NETDEBT)/sh5              # price in yr5 = DCF value then
    tot=p5+sum(s['div'])
    cagr=(tot/PRICE)**(1/5)-1
    pcagr=(p5/PRICE)**(1/5)-1
    mult=(tv-NETDEBT)/(f*1)          # implied EV/FCF-ish
    res[k]=(iv,p5,pcagr,cagr)
    print(k,rows,"TV",round(tv,1),"EV",round(ev,1),"IV/sh",round(iv,1),"P5",round(p5,1),"priceCAGR",round(pcagr*100,1),"totCAGR",round(cagr*100,1),"P/FCF exit",round(p5/(f/sh5),1))
w={"Bear":.3,"Base":.5,"Bull":.2}
print("PW IV",round(sum(w[k]*res[k][0] for k in w),1),"PW P5",round(sum(w[k]*res[k][1] for k in w),1))
pwtot=sum(w[k]*(res[k][1]+sum(S[k]['div'])) for k in w); print("PW totCAGR",round(((pwtot/PRICE)**.2-1)*100,1))
# reverse DCF: base growth, flat margin m, WACC 9%, tg 3% -> margin that justifies $36
def val(m):
    r=REV0;pv=0
    for i,g in enumerate(S['Base']['g']):
        r*=1+g;f=r*m;pv+=f/1.09**(i+1)
    return (pv+f*1.03/0.06/1.09**5-NETDEBT)/SH
lo,hi=0.0,.2
for _ in range(50):
    mid=(lo+hi)/2
    if val(mid)<PRICE: lo=mid
    else: hi=mid
print("implied steady FCF margin",round(mid*100,2))
