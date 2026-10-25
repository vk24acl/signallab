/* SignalLab. All estimators operate on the same seeded, synthetic user ledger. */
(function(root){
  const sum=(xs,fn=x=>x)=>xs.reduce((n,x,i)=>n+fn(x,i),0);
  function wilson(x,n,z=1.959963984540054){
    if(!n)return [0,1];
    const p=x/n,d=1+z*z/n,c=(p+z*z/(2*n))/d,h=z*Math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d;
    return [Math.max(0,c-h),Math.min(1,c+h)];
  }
  function normalCDF(x){
    const t=1/(1+.2316419*Math.abs(x)),d=.3989422804014327*Math.exp(-x*x/2);
    const q=d*t*(.319381530+t*(-.356563782+t*(1.781477937+t*(-1.821255978+t*1.330274429))));
    return x>=0?1-q:q;
  }
  function compare(x1,n1,x2,n2){
    if(!n1||!n2)return null;
    const p1=x1/n1,p2=x2/n2,diff=p2-p1,pool=(x1+x2)/(n1+n2);
    const variance=pool*(1-pool)*(1/n1+1/n2),z=variance>0?diff/Math.sqrt(variance):0;
    const a=wilson(x1,n1),b=wilson(x2,n2);
    const ci=[diff-Math.hypot(p2-b[0],a[1]-p1),diff+Math.hypot(b[1]-p2,p1-a[0])];
    return {p1,p2,diff,relative:p1?diff/p1:null,ci,p:variance>0?Math.max(0,Math.min(1,2*(1-normalCDF(Math.abs(z))))):1,z,n1,n2,x1,x2};
  }
  function sampleSize(p1,relativeMDE){
    const p2=p1*(1+relativeMDE),pbar=(p1+p2)/2;
    if(p1<=0||p2>=1||p2<=p1)return Infinity;
    return Math.ceil((1.959963984540054*Math.sqrt(2*pbar*(1-pbar))+.8416212335729143*Math.sqrt(p1*(1-p1)+p2*(1-p2)))**2/(p2-p1)**2);
  }
  function select(data,weeks=12,group="All channels"){
    const ids=new Set(data.channels.filter(c=>group==="All channels"||c.group===group).map(c=>c.id));
    return {rows:data.rows.filter(r=>r[1]>=12-weeks&&ids.has(r[2])),costs:data.costs.filter(r=>r[0]>=12-weeks&&ids.has(r[1]))};
  }
  function summary(rows,costs){
    const n=rows.length,act=sum(rows,r=>r[4]),eligible=rows.filter(r=>r[1]<=7),ret=sum(eligible,r=>(r[6]&16)?1:0),spend=sum(costs,r=>r[2]);
    return {n,started:sum(rows,r=>r[3]),act,published:sum(rows,r=>r[5]),rate:n?act/n:0,eligible:eligible.length,ret,retRate:eligible.length?ret/eligible.length:null,spend,cpa:act?spend/act:null};
  }
  function channels(data,weeks=12,group="All channels"){
    const selected=select(data,weeks,group);
    return data.channels.filter(c=>group==="All channels"||c.group===group).map(c=>{
      const metrics=summary(selected.rows.filter(r=>r[2]===c.id),selected.costs.filter(r=>r[1]===c.id));
      return {...c,...metrics};
    });
  }
  function experiment(data){
    return [1,2].map(a=>{const rows=data.rows.filter(r=>r[7]===a);return {n:rows.length,act:sum(rows,r=>r[4]),ret:sum(rows,r=>(r[6]&16)?1:0),sessions:sum(rows,r=>r[3]),good:sum(rows,r=>r[8])};});
  }
  // Concave saturating response, calibrated only to synthetic baseline.
  // This is an illustrative planning assumption, NOT an identified causal MMM.
  function optimise(chans,fraction=.2,saturation=1){
    const cs=chans.filter(c=>c.paid&&c.spend>0&&c.act>0),total=sum(cs,c=>c.spend);
    const current=cs.map(c=>c.spend),allocation=current.map(x=>x*(1-fraction));
    const response=(i,b)=>{const k=current[i]*saturation;return cs[i].act*(1-Math.exp(-b/k))/(1-Math.exp(-current[i]/k));};
    let remaining=total-sum(allocation),step=total/1600;
    // Greedy marginal allocation under a per-channel +/- fraction constraint.
    for(let pass=0;remaining>1e-7&&pass<20000;pass++){
      let best=-1,gain=-Infinity,amount=0;
      for(let i=0;i<cs.length;i++){
        const room=current[i]*(1+fraction)-allocation[i],delta=Math.min(step,remaining,room);
        if(delta>1e-7){const g=(response(i,allocation[i]+delta)-response(i,allocation[i]))/delta;
          if(g>gain){gain=g;best=i;amount=delta;}}
      }
      if(best<0)break;allocation[best]+=amount;remaining-=amount;
    }
    const base=sum(cs,c=>c.act),predicted=sum(allocation,(b)=>b); // exact spend is verified separately.
    const expected=sum(cs,(_,i)=>response(i,allocation[i]));
    return {total,base,expected,lift:base?Math.max(0,expected/base-1):0,remaining,allocated:predicted,
      rows:cs.map((c,i)=>({...c,allocated:allocation[i],change:allocation[i]/current[i]-1,expected:response(i,allocation[i])})).sort((a,b)=>b.change-a.change)};
  }
  const API={sum,wilson,compare,sampleSize,select,summary,channels,experiment,optimise};
  if(typeof module!=="undefined"&&module.exports)module.exports=API;else root.SL=API;
})(typeof window!=="undefined"?window:globalThis);
