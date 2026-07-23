const COLORS={"Deep Learning":"#396a93","Generative Models":"#775a9e","Multimodal":"#2d7f87","World Models":"#8b6d3d","Physical AI":"#1d6b55","Robot Learning":"#d7753f","Computer Vision":"#b1912f","Robotics":"#5f7f72","Construction Physical AI":"#a64f58"}
let DATA, selected=null, scope="All"
const $=s=>document.querySelector(s)
const svg=(tag,attrs={})=>{const el=document.createElementNS("http://www.w3.org/2000/svg",tag);Object.entries(attrs).forEach(([k,v])=>el.setAttribute(k,v));return el}
const esc=s=>(s||"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]))
const extent=(arr,key)=>[Math.min(...arr.map(key)),Math.max(...arr.map(key))]
const scale=(v,a,b,c,d)=>a===b?(c+d)/2:c+(v-a)*(d-c)/(b-a)

fetch("./data.json?v=20260723-ontology2").then(r=>{if(!r.ok)throw Error("dataset unavailable");return r.json()}).then(data=>{
  DATA=data
  $("#stamp").textContent=`${data.paperCount.toLocaleString()} published papers · ${data.years[0]}–${data.years.at(-1)} · updated ${data.generated}`
  buildFilters(); render()
}).catch(err=>{$("#stamp").textContent=err.message;$("#detail").innerHTML="<h2>Dataset unavailable</h2><p>Run the Research Radar compiler before building the site.</p>"})

function buildFilters(){
  const preferred=["Deep Learning","Computer Vision","Generative Models","Multimodal","Physical AI","World Models","VLM & VLA","Robot Learning","Robotics","Construction Physical AI"]
  const available=new Set(DATA.scopes||DATA.topics.flatMap(t=>t.scopes||[]))
  const groups=["All",...preferred.filter(x=>available.has(x))]
  $("#scopeFilters").innerHTML=groups.map(g=>`<button class="chip ${g==="All"?"active":""}" data-group="${esc(g)}">${esc(g)}</button>`).join("")
  $("#scopeFilters").addEventListener("click",e=>{if(!e.target.matches(".chip"))return;scope=e.target.dataset.group;document.querySelectorAll(".chip").forEach(x=>x.classList.toggle("active",x===e.target));render()})
  $("#statusFilter").onchange=render
}
function filtered(){
  const status=$("#statusFilter").value
  return DATA.topics.filter(t=>(scope==="All"||(t.scopes||[]).includes(scope))&&(status==="All"||t.status===status))
}
function render(){
  const topics=filtered()
  const rising=topics.filter(t=>["Fast Rising","Emerging"].includes(t.status)).length
  $("#metrics").innerHTML=[
    [topics.length,"visible topics"],[topics.reduce((a,t)=>a+t.recentVolume,0),"matched papers · recent"],
    [rising,"rising signals"],[new Set(topics.flatMap(t=>t.venues)).size,"venue breadth"]
  ].map(([v,l])=>`<div class="metric"><b>${v}</b><span>${l}</span></div>`).join("")
  renderRadar(topics);renderRanks(topics);renderMethod()
  if(!selected||!topics.some(t=>t.id===selected.id)) selected=topics.sort((a,b)=>b.trendScore-a.trendScore)[0]
  if(selected){renderTimeline(selected);renderDetail(selected)}
}
function renderRadar(topics){
  const root=$("#radar");root.innerHTML=""
  const W=760,H=470,p={l:60,r:25,t:25,b:45},xVals=topics.map(t=>Math.log1p(t.recentVolume)),yVals=topics.map(t=>t.momentum)
  const scaleLeaders=new Set([...topics].sort((a,b)=>b.recentVolume-a.recentVolume).slice(0,6).map(t=>t.id))
  const trendLeaders=new Set([...topics].filter(t=>["Fast Rising","Emerging"].includes(t.status)).sort((a,b)=>b.trendScore-a.trendScore).slice(0,8).map(t=>t.id))
  const [xmin,xmax]=extent(xVals,x=>x),[ymin0,ymax0]=extent(yVals,y=>y),ymin=Math.min(ymin0,-.1),ymax=Math.max(ymax0,.1)
  ;[0,.25,.5,.75,1].forEach(q=>{const x=p.l+q*(W-p.l-p.r),y=p.t+q*(H-p.t-p.b);root.append(svg("line",{x1:x,y1:p.t,x2:x,y2:H-p.b,class:"gridline"}));root.append(svg("line",{x1:p.l,y1:y,x2:W-p.r,y2:y,class:"gridline"}))})
  const zeroY=scale(0,ymin,ymax,H-p.b,p.t);root.append(svg("line",{x1:p.l,y1:zeroY,x2:W-p.r,y2:zeroY,class:"axis"}))
  const median=[...xVals].sort((a,b)=>a-b)[Math.floor(xVals.length/2)]||0,midX=scale(median,xmin,xmax,p.l,W-p.r);root.append(svg("line",{x1:midX,y1:p.t,x2:midX,y2:H-p.b,class:"axis","stroke-dasharray":"5 5"}))
  topics.forEach(t=>{
    const x=scale(Math.log1p(t.recentVolume),xmin,xmax,p.l+12,W-p.r-12),y=scale(t.momentum,ymin,ymax,H-p.b-12,p.t+12),r=7+Math.min(15,Math.sqrt(t.support)*1.4)
    const circle=svg("circle",{cx:x,cy:y,r,fill:COLORS[t.category]||"#6b7b73",opacity:t.confidence==="Early"?.48:.82,class:`bubble ${selected?.id===t.id?"selected":""}`})
    const tooltip=svg("title");tooltip.textContent=`${t.label} · ${t.status} · ${t.recentVolume} recent papers`;circle.append(tooltip)
    circle.addEventListener("click",()=>{selected=t;renderRadar(topics);renderTimeline(t);renderDetail(t)})
    root.append(circle)
    if(scaleLeaders.has(t.id)||trendLeaders.has(t.id)){
      const rightSide=x>W-p.r-150
      const label=svg("text",{x:rightSide?x-r-4:x+r+4,y:y+4,class:"bubble-label","text-anchor":rightSide?"end":"start"})
      label.textContent=t.label;root.append(label)
    }
  })
}
function renderRanks(topics){
  const lists={
    rankEstablished:[...topics].sort((a,b)=>b.recentVolume-a.recentVolume),
    rankRising:[...topics].sort((a,b)=>b.trendScore-a.trendScore),
    rankEmerging:[...topics].filter(t=>t.recentVolume<35).sort((a,b)=>b.trendScore-a.trendScore)
  }
  Object.entries(lists).forEach(([id,items])=>{$("#"+id).innerHTML=items.slice(0,5).map((t,i)=>`<li data-id="${t.id}"><span class="num">${String(i+1).padStart(2,"0")}</span><strong>${esc(t.label)}</strong><small>${id==="rankEstablished"?t.recentVolume:t.trendScore}</small></li>`).join("");$("#"+id).onclick=e=>{const li=e.target.closest("li");if(!li)return;selected=DATA.topics.find(t=>t.id===li.dataset.id);renderTimeline(selected);renderDetail(selected);renderRadar(filtered())}})
}
function renderTimeline(t){
  $("#timelineTitle").textContent=t.label;$("#confidenceBadge").textContent=`${t.confidence} confidence`
  const root=$("#timeline");root.innerHTML="";const W=700,H=250,p={l:48,r:22,t:25,b:38},max=Math.max(...t.shares,1)
  const pts=t.shares.map((v,i)=>[scale(i,0,t.shares.length-1,p.l,W-p.r),scale(v,0,max,H-p.b,p.t)])
  ;[0,.5,1].forEach(q=>{const y=p.t+q*(H-p.t-p.b);root.append(svg("line",{x1:p.l,y1:y,x2:W-p.r,y2:y,class:"gridline"}))})
  const area=svg("path",{d:`M${pts[0][0]},${H-p.b} `+pts.map(x=>`L${x[0]},${x[1]}`).join(" ")+` L${pts.at(-1)[0]},${H-p.b} Z`,class:"area"});root.append(area)
  root.append(svg("path",{d:pts.map((x,i)=>`${i?"L":"M"}${x[0]},${x[1]}`).join(" "),class:"line"}))
  pts.forEach((pt,i)=>{root.append(svg("circle",{cx:pt[0],cy:pt[1],r:5,class:"dot"}));const tx=svg("text",{x:pt[0],y:H-14,"text-anchor":"middle",class:"tick"});tx.textContent=DATA.years[i];root.append(tx);const val=svg("text",{x:pt[0],y:pt[1]-10,"text-anchor":"middle",class:"tick"});val.textContent=t.counts[i];root.append(val)})
}
function renderDetail(t){
  $("#detail").innerHTML=`<p class="kicker">EVIDENCE</p><h2>${esc(t.label)}</h2><span class="status">${esc(t.status)}</span>
  <div class="detail-grid"><div class="detail-stat"><b>${t.recentVolume}</b><span>2024–25 papers</span></div><div class="detail-stat"><b>${t.momentum>0?"+":""}${t.momentum}</b><span>share momentum</span></div><div class="detail-stat"><b>${t.breadth}</b><span>recent venues</span></div><div class="detail-stat"><b>${t.trendScore}</b><span>trend evidence</span></div><div class="detail-stat"><b>${t.support}</b><span>five-year support</span></div><div class="detail-stat"><b>${t.confidence}</b><span>confidence</span></div></div>
  <p class="hint">Matched ontology / aliases: ${(t.aliases||[]).map(x=>esc(x.replaceAll("\\\\b","").replaceAll("\\\\s"," "))).join(" · ")}</p><p><b>Visible in scopes</b><br>${(t.scopes||[]).map(esc).join(" · ")}</p><p><b>Recent venue spread</b><br>${t.venues.length?t.venues.map(esc).join(" · "):"No multi-venue evidence yet"}</p>
  <h3>Representative published papers</h3><ul class="paper-list">${t.papers.length?t.papers.map(p=>`<li><a href="${esc(p.url)}" target="_blank" rel="noreferrer">${esc(p.title)}</a><small>${esc(p.venue)} · ${p.year}${p.authors?.length?" · "+esc(p.authors.slice(0,3).join(", ")):""}</small></li>`).join(""):"<li>No representative paper in the current title-matched sample.</li>"}</ul>`
}
function renderMethod(){
  const missing=DATA.audit.filter(x=>x.status!=="ok"),coverage=DATA.audit.filter(x=>x.status==="ok").length
  $("#methodBody").innerHTML=`<p><b>Included evidence:</b> papers indexed in named peer-reviewed proceedings plus Automation in Construction and Construction Robotics journal metadata. arXiv and workshops are excluded. Current coverage: ${coverage}/${DATA.audit.length} venue-years, ${DATA.paperCount.toLocaleString()} papers.</p><p><b>Topic assignment:</b> a transparent multi-label ontology spans deep learning, computer vision, multimodal learning, generative models, world models, VLM/VLA, robot learning, robotics, and construction Physical AI. Scope buttons are overlapping research lenses, not mutually exclusive folders: one topic may appear in several scopes. This preserves convergences such as generative robot policies.</p><p><b>Construction intersection:</b> a construction task, asset, material, equipment, or field context must intersect with autonomy, robotics, perception, planning, control, inspection, HRI, or safety. This catches papers titled by the task rather than by “construction robotics” while rejecting generic construction-management work.</p><p><b>Trend evidence:</b> counts are normalized per 1,000 papers per year; recent volume, five-year slope, burst, and venue breadth are shrunk toward zero for small samples. Status is a navigation aid, not a prediction of scientific value.</p><p><b>Known limits:</b> title-level classification favors precision over recall; DBLP and Crossref can lag; institutions and abstracts are not yet used; technical debates require human review. Missing venue-years: ${missing.length}. Every result exposes ontology terms, scopes, counts, venues, and representative papers so it can be challenged.</p>`
}
