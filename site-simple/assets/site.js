document.documentElement.classList.add('js');
const TABS=['home','buildings','rent-to-own','delivery','contact'];
const SUB={'buildings-lp':'buildings','buildings-vinyl':'buildings','buildings-garages':'buildings','buildings-pavilions':'buildings'};
function show(){
 const h=(location.hash||'#home').slice(1);
 const tab=TABS.includes(h)?h:(SUB[h]||'home');
 document.querySelectorAll('.tab').forEach(t=>t.classList.toggle('on',t.id===tab));
 document.querySelectorAll('nav.tabs a').forEach(a=>{a.getAttribute('href')==='#'+tab?a.setAttribute('aria-current','page'):a.removeAttribute('aria-current')});
 document.getElementById('tabs').classList.remove('open');document.getElementById('menu-btn').setAttribute('aria-expanded','false');
 if(SUB[h]){const el=document.getElementById(h);requestAnimationFrame(()=>el&&el.scrollIntoView({block:'start'}));}else window.scrollTo(0,0);
}
addEventListener('hashchange',show);show();
document.getElementById('menu-btn').addEventListener('click',e=>{const n=document.getElementById('tabs');const o=n.classList.toggle('open');e.currentTarget.setAttribute('aria-expanded',o)});
document.getElementById('quote').addEventListener('submit',e=>{e.preventDefault();
 const v=id=>document.getElementById(id).value.trim();
 const t=`Quote request – Classic Shed Builders\nName: ${v('q-name')}\nPhone: ${v('q-phone')}\nEmail: ${v('q-email')}\nTown: ${v('q-town')}\nBuilding: ${v('q-type')}\n\n${v('q-msg')}`;
 document.getElementById('q-text').textContent=t;document.getElementById('q-out').classList.add('show');});
document.getElementById('q-copy').addEventListener('click',e=>{const t=document.getElementById('q-text').textContent;const b=e.currentTarget;
 navigator.clipboard.writeText(t).then(()=>{b.textContent='Copied'},()=>{const r=document.createRange();r.selectNodeContents(document.getElementById('q-text'));const s=getSelection();s.removeAllRanges();s.addRange(r);b.textContent='Text selected, copy it'});});

/* reviews: always auto-scroll; arrows, swipe or drag move it, then it resumes */
(()=>{const m=document.getElementById('rv');if(!m)return;const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
 const fine=matchMedia('(hover:hover) and (pointer:fine)').matches;
 let pause=0,last=performance.now(),pos=m.scrollLeft,drag=null;const half=()=>m.scrollWidth/2;const step=()=>{const c=m.querySelector('.mcard');return c?c.offsetWidth+18:340};
 const hold=ms=>{pause=performance.now()+ms};
 function wrap(){if(m.scrollLeft>=half())m.scrollLeft-=half();pos=m.scrollLeft;}
 function tick(t){const dt=Math.min(t-last,60);last=t;
  if(!reduce&&!drag&&t>pause&&!(fine&&m.matches(':hover'))){pos+=dt*0.045;m.scrollLeft=pos;if(m.scrollLeft>=half()){m.scrollLeft-=half();pos=m.scrollLeft;}}
  else pos=m.scrollLeft;
  requestAnimationFrame(tick);}
 requestAnimationFrame(tick);
 function go(d){hold(2500);if(d<0&&m.scrollLeft<step()){m.scrollLeft+=half();}m.scrollTo({left:m.scrollLeft+d*step(),behavior:'smooth'});setTimeout(wrap,700);}
 document.querySelector('.rvnav.prev').addEventListener('click',()=>go(-1));
 document.querySelector('.rvnav.next').addEventListener('click',()=>go(1));
 m.addEventListener('touchstart',()=>hold(2500),{passive:true});
 m.addEventListener('touchend',()=>{hold(2500);setTimeout(wrap,600)},{passive:true});
 m.addEventListener('pointerdown',e=>{if(e.pointerType!=='mouse'||e.target.closest('button'))return;drag={x:e.clientX,s:m.scrollLeft};m.style.cursor='grabbing';e.preventDefault();});
 addEventListener('pointermove',e=>{if(!drag)return;m.scrollLeft=drag.s-(e.clientX-drag.x);});
 addEventListener('pointerup',()=>{if(!drag)return;drag=null;m.style.cursor='grab';hold(2000);wrap();});
 m.style.cursor='grab';
 m.addEventListener('keydown',e=>{if(e.key==='ArrowRight')go(1);if(e.key==='ArrowLeft')go(-1);});})();

/* photo viewer: auto-advance, arrows, thumbnails, swipe, full screen */
(()=>{const g=document.getElementById('gal');if(!g)return;const slides=[...g.querySelectorAll('.slide')],thumbs=[...g.querySelectorAll('.thumb')];
 const lb=document.getElementById('lb'),lbi=lb.querySelector('img'),lbc=lb.querySelector('.lbcap');const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
 thumbs.forEach((t,k)=>{t.querySelector('img').src=slides[k].querySelector('img').src});
 let i=0,timer;
 function show(n){i=(n+slides.length)%slides.length;slides.forEach((s,k)=>s.classList.toggle('on',k===i));thumbs.forEach((t,k)=>t.classList.toggle('on',k===i));
  g.querySelector('.gcount b').textContent=i+1;const img=slides[i].querySelector('img');img.loading='eager';
  if(!lb.hidden){lbi.src=img.src;lbi.alt=img.alt;lbc.textContent=img.alt;}
  const tb=g.querySelector('.thumbs'),t=thumbs[i];tb.scrollTo({left:t.offsetLeft-tb.clientWidth/2+t.offsetWidth/2,behavior:'smooth'});}
 function auto(){clearInterval(timer);if(!reduce)timer=setInterval(()=>{if(lb.hidden&&!document.hidden)show(i+1)},5000);}
 g.querySelector('.stage .prev').onclick=()=>{show(i-1);auto()};g.querySelector('.stage .next').onclick=()=>{show(i+1);auto()};
 thumbs.forEach((t,k)=>t.onclick=()=>{show(k);auto()});
 const open=()=>{lb.hidden=false;show(i);document.body.style.overflow='hidden';lb.querySelector('.lbclose').focus();};
 const close=()=>{lb.hidden=true;document.body.style.overflow='';auto();};
 g.querySelector('.gzoom').onclick=open;slides.forEach(s=>s.querySelector('img').onclick=open);
 lb.querySelector('.lbclose').onclick=close;lb.querySelector('.lbp').onclick=()=>show(i-1);lb.querySelector('.lbn').onclick=()=>show(i+1);
 lb.addEventListener('click',e=>{if(e.target===lb)close()});
 addEventListener('keydown',e=>{if(lb.hidden)return;if(e.key==='Escape')close();if(e.key==='ArrowRight')show(i+1);if(e.key==='ArrowLeft')show(i-1);});
 let sx=null;[g.querySelector('.stage'),lb].forEach(el=>{el.addEventListener('touchstart',e=>{sx=e.touches[0].clientX},{passive:true});
  el.addEventListener('touchend',e=>{if(sx===null)return;const dx=e.changedTouches[0].clientX-sx;if(Math.abs(dx)>40){show(i+(dx<0?1:-1));auto();}sx=null;},{passive:true});});
 auto();})();
