/* Momentum Growth — scroll story: opening clip -> satellite zoom-out video -> interactive night globe.
   Progressive enhancement: without JS / WebGL / with reduced motion, the static stacked layout in story.css is used. */
(function(){
'use strict';
var root=document.getElementById('mg-story');if(!root)return;
var D=root.dataset;
var reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
function webglOK(){try{var c=document.createElement('canvas');return !!(window.WebGLRenderingContext&&(c.getContext('webgl')||c.getContext('experimental-webgl')));}catch(e){return false;}}
if(reduce||!webglOK()||!('IntersectionObserver' in window))return;

var host=root.querySelector('.mg-gl'),vid=root.querySelector('.mg-vid'),sV=root.querySelector('.mg-scene'),cap=root.querySelector('.mg-cap'),
    steps=[].slice.call(root.querySelectorAll('.mg-step')),prog=root.querySelector('.mg-prog'),bar=root.querySelector('.mg-prog b'),hint=root.querySelector('.mg-hint');
root.classList.add('mg-live');

function giveUp(){root.classList.remove('mg-live');running=false;dead=true;}
var running=false,dead=false,started=false;

var io=new IntersectionObserver(function(en){
  if(en[0].isIntersecting&&!started){started=true;io.disconnect();loadThree();}
},{rootMargin:'150% 0px'});
io.observe(root);

function loadThree(){
  if(window.THREE){init();return;}
  var s=document.createElement('script');s.src=D.three;s.async=true;
  s.onload=function(){try{init();}catch(e){giveUp();}};
  s.onerror=giveUp;
  document.head.appendChild(s);
}

function init(){
var MAD={lat:24.47,lon:39.61};
var renderer;
try{renderer=new THREE.WebGLRenderer({antialias:true,alpha:true,powerPreference:'high-performance'});}catch(e){giveUp();return;}
var mobile=innerWidth<=900||(matchMedia&&matchMedia('(pointer:coarse)').matches);
renderer.setPixelRatio(Math.min(window.devicePixelRatio||1,mobile?1.5:2));
renderer.setClearColor(0x000000,0);
host.appendChild(renderer.domElement);
renderer.domElement.addEventListener('webglcontextlost',function(e){e.preventDefault();giveUp();},false);
var scene=new THREE.Scene();
var FOV=18,TF=Math.tan(FOV*Math.PI/360);
var camera=new THREE.PerspectiveCamera(FOV,1,.1,100);
var globe=new THREE.Group();scene.add(globe);
function ll(lat,lon,r){r=r||1;var a=lat*Math.PI/180,o=lon*Math.PI/180;return new THREE.Vector3(r*Math.cos(a)*Math.cos(o),r*Math.sin(a),-r*Math.cos(a)*Math.sin(o));}
var mgr=new THREE.LoadingManager(function(){host.classList.add('on');});
var ld=new THREE.TextureLoader(mgr),maxA=Math.min(8,renderer.capabilities.getMaxAnisotropy());
var tp=ld.load(mobile?D.packM:D.pack),tn=ld.load(mobile?D.nightM:D.night);
[tp,tn].forEach(function(x){x.anisotropy=maxA;x.generateMipmaps=true;x.minFilter=THREE.LinearMipmapLinearFilter;x.magFilter=THREE.LinearFilter;x.wrapS=THREE.RepeatWrapping;});
var uni={pk:{value:tp},nt:{value:tn},time:{value:0}};
var earth=new THREE.Mesh(new THREE.SphereGeometry(1,mobile?128:192,mobile?96:128),new THREE.ShaderMaterial({
 uniforms:uni,
 vertexShader:'varying vec2 vUv;varying vec3 vN;varying vec3 vV;'+
 'void main(){vUv=uv;vN=normalize(normalMatrix*normal);vec4 mv=modelViewMatrix*vec4(position,1.);vV=normalize(-mv.xyz);gl_Position=projectionMatrix*mv;}',
 fragmentShader:'precision highp float;'+
 'uniform sampler2D pk;uniform sampler2D nt;uniform float time;varying vec2 vUv;varying vec3 vN;varying vec3 vV;'+
 'float h(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}'+
 'void main(){'+
 ' vec3 N=normalize(vN),V=normalize(vV);'+
 ' vec3 L=normalize(vec3(-.62,.62,.48));'+
 ' vec3 s=texture2D(pk,vUv).rgb;'+
 ' float land=smoothstep(.3,.7,s.r);'+
 ' float relief=(s.g-.5)*2.;'+
 ' float elev=s.b;'+
 ' float ndl=dot(N,L),ndv=max(dot(N,V),0.);'+
 ' float lit=smoothstep(-.55,1.,ndl);lit=.07+.93*lit*lit;'+
 ' float g=(.215+.12*elev)*(1.+relief*(relief>0.?1.15:.8));'+
 ' vec3 landc=vec3(1.,.995,.975)*max(g,.02)*lit;'+
 ' float sheen=pow(max(dot(reflect(-L,N),V),0.),5.);'+
 ' vec3 ocean=vec3(.010,.020,.045)*(.55+.9*lit)+vec3(.020,.032,.060)*sheen;'+
 ' vec3 col=mix(ocean,landc,land);'+
 ' col*=mix(.5,1.,smoothstep(0.,.42,ndv));'+
 ' col+=vec3(.16,.16,.15)*pow(1.-ndv,6.)*lit;'+
 ' float nl=texture2D(nt,vUv).r;'+
 ' float glow=texture2D(nt,vUv,2.5).r;'+
 ' float tw=.9+.1*sin(time*1.3+h(floor(vUv*vec2(1600.,800.)))*40.);'+
 ' float core=pow(nl,1.7);'+
 ' vec3 lc=mix(vec3(1.,.74,.36),vec3(1.,.95,.82),smoothstep(.15,.8,core));'+
 ' col+=(lc*core*2.3*tw+vec3(1.,.78,.45)*glow*.13)*(1.12-.3*lit)*smoothstep(0.,.25,ndv);'+
 ' col+=(h(gl_FragCoord.xy+fract(time))-.5)/255.;'+
 ' gl_FragColor=vec4(col,1.);}'}));
globe.add(earth);

var mdir=ll(MAD.lat,MAD.lon).normalize();
var marker=new THREE.Group();marker.position.copy(mdir.clone().multiplyScalar(1.002));
marker.quaternion.setFromUnitVectors(new THREE.Vector3(0,0,1),mdir);globe.add(marker);
var dot=new THREE.Mesh(new THREE.CircleGeometry(.0065,32),new THREE.MeshBasicMaterial({color:0xffe9b8}));dot.position.z=.001;marker.add(dot);
var W=1,H=1,wide=true,RHO=.45,CX=.3,CY=.52;
function resize(){W=host.clientWidth||innerWidth;H=host.clientHeight||innerHeight;renderer.setSize(W,H,false);wide=W>900;var aspect=W/H;
 RHO=wide?Math.max(.3,Math.min(.42,(.56*W-260)/H)):Math.min(.6*aspect,.29);CX=wide?.3:.5;CY=wide?.53:.37;camera.aspect=aspect;}
var P0=.40,AX=new THREE.Vector3(1,0,0),AY=new THREE.Vector3(0,1,0),qa=new THREE.Quaternion(),qb=new THREE.Quaternion();
var yaw=0,pitch=P0;
var yawM=Math.atan2(-mdir.x,mdir.z);
function apply(){qa.setFromAxisAngle(AY,yaw);qb.setFromAxisAngle(AX,pitch);globe.quaternion.copy(qb).multiply(qa);}
function ease(x){return x<0?0:x>1?1:x*x*(3-2*x);}

var target=0,ps=0,vis=false;
function readScroll(){var r=root.getBoundingClientRect();var total=Math.max(1,r.height-innerHeight);target=Math.max(0,Math.min(1,-r.top/total));
 vis=r.bottom>-50&&r.top<innerHeight+50;if(vis&&!running&&!dead){running=true;last=performance.now();requestAnimationFrame(frame);}}
addEventListener('scroll',readScroll,{passive:true});
addEventListener('resize',function(){resize();readScroll();});
resize();readScroll();ps=target;

/* drag (enabled only once the camera has pulled back to the globe) */
var dyaw=0,dpitch=0,vx=0,vy=0,drag=false,px=0,py=0,lastMove=0;
function sens(){return Math.min(.005,3.6/Math.max(W,H));}
host.addEventListener('pointerdown',function(e){if(ps<.56)return;drag=true;px=e.clientX;py=e.clientY;vx=vy=0;lastMove=performance.now();try{host.setPointerCapture(e.pointerId);}catch(_){}});
host.addEventListener('pointermove',function(e){if(!drag)return;var k=sens(),dx=e.clientX-px,dy=e.clientY-py;px=e.clientX;py=e.clientY;vx=dx*k;vy=dy*k*.45;lastMove=performance.now();dyaw+=vx;dpitch=Math.max(-.6,Math.min(.5,dpitch+vy));});
function end(){drag=false;if(performance.now()-lastMove>80){vx=vy=0;}}
host.addEventListener('pointerup',end);host.addEventListener('pointercancel',end);

/* video scrubbing */
var NEWV=!mobile; /* desktop uses the v5 Earth Studio clip; mobile keeps the older clip until its framing is re-exported */
var LON0=NEWV?42:43.5,R0=NEWV?.49:.625,SXV=NEWV?-.01:-.0102,SY=NEWV?.485:.483,YAW0=Math.atan2(-Math.cos(LON0*Math.PI/180),-Math.sin(LON0*Math.PI/180)),PIT0=.43;
var cv=renderer.domElement;
var vidReady=false,want=0,seeking=false,seekTimer=0,FPS=NEWV?30:20;
function seek(){
  if(!vidReady||seeking)return;
  var t=Math.round(want*FPS)/FPS;
  if(Math.abs(t-vid.currentTime)<.01)return;
  seeking=true;clearTimeout(seekTimer);seekTimer=setTimeout(function(){seeking=false;},400);
  try{vid.currentTime=t;}catch(_){seeking=false;}
}
vid.addEventListener('seeked',function(){seeking=false;clearTimeout(seekTimer);seek();});
vid.addEventListener('loadedmetadata',function(){
  vidReady=true;
  try{var pr=vid.play();if(pr&&pr.then)pr.then(function(){vid.pause();}).catch(function(){});else vid.pause();}catch(_){}
});
vid.addEventListener('error',function(){vidReady=false;});
vid.preload='auto';
var VSRC=(!NEWV&&D.videoM)?D.videoM:D.video;
if(NEWV&&D.poster)vid.poster=D.poster;
/* load the whole clip into memory first, so every scrub seek is served locally (no range requests) */
function useDirect(){vid.src=VSRC;vid.load();}
try{
  fetch(VSRC).then(function(r){if(!r.ok)throw 0;return r.blob();}).then(function(b){
    if(dead)return;vid.src=URL.createObjectURL(b);vid.load();
  }).catch(useDirect);
}catch(_){useDirect();}

var cache={};
function setStyle(el,key,prop,val){if(cache[key]!==val){cache[key]=val;el.style[prop]=val;}}
var globeOn=false;
function layout(p){
 var aV=ease(p/.03)*(1-ease((p-.31)/.09));
 var dk=ease((p-.20)/.20);
 setStyle(vid,'vf','filter','brightness('+(1-.55*dk).toFixed(2)+') saturate('+(1-.45*dk).toFixed(2)+')');
 setStyle(sV,'vo','opacity',aV.toFixed(3));
 if(vidReady&&aV>.001&&isFinite(vid.duration)){
   var Dd=vid.duration-.04;
   want=NEWV?Math.min(Dd,Math.max(0,p/.31)*Dd):(p<.10?(p/.10)*1.6:Math.min(Dd,1.6+(p-.10)/.21*(Dd-1.6)));
   seek();
 }
 setStyle(cap,'co','opacity',(p>.04&&p<.30)?'1':'0');
 var go=ease((p-.28)/.02);cv.style.opacity=go;globeOn=go>.01;
 var e1=ease((p-.38)/.17),e2=ease((p-.95)/.05),pg=Math.max(0,p-.44);
 var kv=Math.max(1,W/H*9/16),R0v=R0*kv,SX=.5+SXV*16/9*H/W*kv,SYv=.5+(SY-.5)*kv; /* match the video's object-fit:cover framing */
 var rho=Math.exp(Math.log(R0v)+(Math.log(RHO)-Math.log(R0v))*e1)*(1-.08*e2);
 var cx=SX+(CX-SX)*e1,cy=SYv+(CY-SYv)*e1-e2*.06;
 camera.position.set(0,0,1/(2*TF*rho));
 marker.scale.setScalar(Math.min(1,(RHO/rho)*1.4));
 camera.setViewOffset(W,H,(.5-cx)*W,(.5-cy)*H,W,H);camera.updateProjectionMatrix();
 yaw=YAW0+(yawM-YAW0)*e1+dyaw;pitch=Math.max(-.2,Math.min(.95,PIT0+(P0-PIT0)*e1+dpitch));apply();
 for(var i=0;i<steps.length;i++){
   var s0=.52+i*.15,a=ease((p-s0)/.04);
   if(i<steps.length-1)a*=1-ease((p-s0-.115)/.035);
   steps[i].style.opacity=a.toFixed(3);steps[i].style.translate='0 '+((1-a)*26).toFixed(1)+'px';
 }
 setStyle(prog,'po','opacity',p>.38?'1':'0');
 bar.style.width=(Math.max(0,Math.min(1,(p-.38)/.6))*100).toFixed(1)+'%';
 var can=p>=.56;
 host.classList.toggle('mg-can',can);
}

var last=0,clock=0;
function frame(now){
 if(dead)return;
 if(!vis){running=false;return;}
 requestAnimationFrame(frame);
 var dt=Math.min((now-last)/1000||.016,.05);last=now;clock+=dt;
 uni.time.value=clock;
 ps+=(target-ps)*(1-Math.pow(.001,dt));
 if(ps<.56){var T=Math.PI*2;dyaw-=Math.round(dyaw/T)*T;var k=ps<.3?1:1-Math.pow(.003,dt);dyaw-=dyaw*k;dpitch-=dpitch*k;vx=vy=0;drag=false;}
 if(!drag){if(ps>=.56)dyaw-=.12*dt*Math.min(1,(ps-.56)/.03);dyaw+=vx;dpitch=Math.max(-.6,Math.min(.5,dpitch+vy));var f=Math.pow(.94,dt*60);vx*=f;vy*=f;}
 layout(ps);
 if(globeOn)renderer.render(scene,camera);
}
}
})();
