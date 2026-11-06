import os,re
src=os.path.join(os.path.dirname(os.path.abspath(__file__)),'homepage.html')
out=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
body=open(src,encoding='utf-8').read()
title=re.search(r'<title>(.*?)</title>',body).group(1)
body=body.replace('<title>'+title+'</title>\n','',1)
head='''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>'''+title+'''</title>
<meta name="description" content="어서 오세요! 유채의 레트로 홈페이지, 야채마을입니다.">
<style>:root{color-scheme:light}body{margin:0;font:14px system-ui,sans-serif}img{max-width:100%}[hidden]{display:none!important}</style>
<script src="firebase-config.js"></script>
<script>
/* claude.ai 밖에서는 Firebase로 게시판·방명록·명예의 전당을 연결해요 */
(function(){
  if(window.claude||!window.YACHAE_FIREBASE)return;
  let res;const FB=new Promise(r=>res=r);window.__ycFBres=res;
  window.claude={use:async n=>{const fb=await FB;if(!fb)return null;return n==='db'?fb.db:n==='user'?fb.user:null;}};
  window.YC_SETNAME=async n=>{const fb=await FB;if(fb)await fb.setName(n);};
  window.YC_STANDALONE=true;
  setTimeout(()=>res(null),15000);
})();
</script>
<script type="module">
if(window.__ycFBres){
const V='https://www.gstatic.com/firebasejs/10.12.2/';
try{
const {initializeApp}=await import(V+'firebase-app.js');
const {getAuth,onAuthStateChanged,signInAnonymously,GoogleAuthProvider,signInWithPopup,signOut}=await import(V+'firebase-auth.js');
const F=await import(V+'firebase-firestore.js');
const app=initializeApp(window.YACHAE_FIREBASE);const auth=getAuth(app);
const fs=window.YACHAE_DB?F.getFirestore(app,window.YACHAE_DB):F.getFirestore(app);
const me=await new Promise(r=>{let d=false;onAuthStateChanged(auth,u=>{if(u){if(!d){d=true;r(u);}}else signInAnonymously(auth).catch(()=>{if(!d){d=true;r(null);}});});});
const OWN=(window.YACHAE_OWNER_EMAIL||'').toLowerCase();
const wrapSnap=d=>({id:d.id,exists:d.exists(),data:()=>d.data()});
function Q(path,cons){return{
  orderBy:(f,dir)=>Q(path,[...cons,F.orderBy(f,dir||'asc')]),
  limit:n=>Q(path,[...cons,F.limit(n)]),
  onSnapshot:(next,err)=>F.onSnapshot(F.query(F.collection(fs,path),...cons),s=>next({docs:s.docs.map(wrapSnap),size:s.size,empty:s.empty}),e=>err&&err({code:e.code,message:e.message})),
  get:async()=>{const s=await F.getDocs(F.query(F.collection(fs,path),...cons));return{docs:s.docs.map(wrapSnap),size:s.size,empty:s.empty};},
  add:async data=>{const r=await F.addDoc(F.collection(fs,path),data);return{id:r.id};},
  doc:id=>D(path+'/'+id)};}
function D(path){return{
  set:data=>F.setDoc(F.doc(fs,path),data),update:data=>F.updateDoc(F.doc(fs,path),data),delete:()=>F.deleteDoc(F.doc(fs,path)),
  get:async()=>wrapSnap(await F.getDoc(F.doc(fs,path)))};}
const db={collection:p=>Q(p,[]),doc:p=>D(p),incr:(p,f)=>F.setDoc(F.doc(fs,p),{[f]:F.increment(1)},{merge:true})};
const user={id:async()=>me?me.uid:null,isOwner:async()=>!!(me&&me.email&&OWN&&me.email.toLowerCase()===OWN),can:async()=>true,canEdit:async()=>false,
  profiles:async ids=>{const out={};await Promise.all([].concat(ids).map(async id=>{try{const s=await F.getDoc(F.doc(fs,'names/'+id));out[id]={id,name:s.exists()?(s.data().name||''):''};}catch(e){out[id]={id,name:''};}}));return out;}};
const setName=async n=>{if(me)try{await F.setDoc(F.doc(fs,'names/'+me.uid),{name:String(n).slice(0,12)});}catch(e){}};
window.__ycFBres({db,user,setName});
const login=async()=>{try{await signInWithPopup(auth,new GoogleAuthProvider());location.reload();}catch(e){alert('로그인하지 못했어요: '+(e&&e.code||''));}};
const logout=()=>signOut(auth).then(()=>location.reload());
const c=document.querySelector('.copy');if(c){const b=document.createElement('button');b.className='lk';b.style.marginLeft='8px';
  if(me&&!me.isAnonymous){b.textContent='🔓 로그아웃';b.onclick=logout;}else{b.textContent='🔑';b.title='주인장 로그인';b.onclick=login;}c.appendChild(b);}
document.querySelectorAll('.gbnick').forEach(i=>{i.hidden=false;try{i.value=localStorage.getItem('yc-nick')||'';}catch(e){}});
}catch(e){console.error(e);window.__ycFBres(null);}
}
</script>
</head>
<body>
'''
open(os.path.join(out,'index.html'),'w',encoding='utf-8').write(head+body+'\n</body>\n</html>\n')
print('built',len(head+body))
