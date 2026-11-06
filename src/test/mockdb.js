(()=>{const store={};const subs=[];let idn=0;
const colOf=p=>{store[p]=store[p]||{};return store[p];};
const notify=()=>subs.forEach(f=>f());
const snap=(id,d)=>({id,exists:!!d,data:()=>d?JSON.parse(JSON.stringify(d)):undefined});
function Q(path,o={}){return{orderBy:(f,dir)=>Q(path,{...o,f,dir}),limit:n=>Q(path,{...o,n}),
 _docs(){let a=Object.entries(colOf(path)).map(([id,d])=>snap(id,d));if(o.f)a.sort((x,y)=>{const A=x.data()[o.f],B=y.data()[o.f];return (A>B?1:A<B?-1:0)*(o.dir==='desc'?-1:1);});if(o.n)a=a.slice(0,o.n);return a;},
 onSnapshot(next){const run=()=>{const d=this._docs();next({docs:d,size:d.length,empty:!d.length});};subs.push(run);setTimeout(run,10);return()=>{};},
 async get(){const d=this._docs();return{docs:d,size:d.length,empty:!d.length};},
 async add(data){const id='m'+(++idn);colOf(path)[id]=JSON.parse(JSON.stringify(data));setTimeout(notify,5);return{id};},
 doc:id=>D(path+'/'+id)};}
function D(path){const i=path.lastIndexOf('/'),c=path.slice(0,i),id=path.slice(i+1);return{
 async set(d){colOf(c)[id]=JSON.parse(JSON.stringify(d));setTimeout(notify,5);},async update(d){colOf(c)[id]={...colOf(c)[id],...d};setTimeout(notify,5);},
 async delete(){delete colOf(c)[id];setTimeout(notify,5);},async get(){return snap(id,colOf(c)[id]);}};}
const db={collection:p=>Q(p),doc:p=>D(p),incr:async(p,f)=>{const d=D(p);const g=await d.get();await d.set({[f]:(g.exists?g.data()[f]:0)+1});}};
window.__store=store;
window.claude={use:async n=>n==='db'?db:n==='user'?{id:async()=>'u1',isOwner:async()=>window.__OWNER!==false,can:async()=>true,profiles:async()=>({})}:null};
})();
