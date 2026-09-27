/* ============================================================
   Sentinel Trinity front-end engine
   - counters / gauges
   - responsive sidebar (mobile/tablet hamburger)
   - generic detail-modal system for any clickable element
   - dependency-free inline SVG chart builders (line/bar/donut)
   - button ripple feedback
   ============================================================ */

function animateCounters(){
  document.querySelectorAll('.kpi .val[data-count]').forEach(el=>{
    const target = parseFloat(el.getAttribute('data-count'));
    const suffix = el.getAttribute('data-suffix') || '';
    if(isNaN(target)) return;
    let cur = 0; const steps = 24, inc = target/steps;
    const timer = setInterval(()=>{
      cur += inc;
      if(cur >= target){ el.textContent = (Number.isInteger(target)?target:target.toFixed(1)) + suffix; clearInterval(timer); }
      else el.textContent = Math.floor(cur).toLocaleString() + suffix;
    }, 700/steps);
  });
}

function gaugeFill(){
  document.querySelectorAll('.gauge-ring').forEach(circle=>{
    const pct = parseFloat(circle.getAttribute('data-pct'));
    const r = parseFloat(circle.getAttribute('r'));
    const c = 2*Math.PI*r;
    const off = c - (pct/100)*c;
    circle.style.strokeDasharray = c;
    circle.style.strokeDashoffset = c;
    requestAnimationFrame(()=>{
      circle.style.transition = 'stroke-dashoffset 1.1s cubic-bezier(.2,.8,.2,1)';
      circle.style.strokeDashoffset = off;
    });
  });
}

/* ---------------- Responsive sidebar ---------------- */
function initSidebar(){
  const sidebar = document.getElementById('sidebar');
  const scrim = document.getElementById('sidebarScrim');
  const hamburger = document.getElementById('hamburger');
  const closeBtn = document.getElementById('sidebarClose');
  if(!sidebar) return;
  const open = ()=>{ sidebar.classList.add('open'); scrim.classList.add('show'); };
  const close = ()=>{ sidebar.classList.remove('open'); scrim.classList.remove('show'); };
  hamburger && hamburger.addEventListener('click', open);
  closeBtn && closeBtn.addEventListener('click', close);
  scrim && scrim.addEventListener('click', close);
  sidebar.querySelectorAll('.navitem').forEach(a=>a.addEventListener('click', close));
}

/* ---------------- Button ripple ---------------- */
function initRipples(){
  document.addEventListener('click', (e)=>{
    const btn = e.target.closest('.btn');
    if(!btn) return;
    const rect = btn.getBoundingClientRect();
    const r = document.createElement('span');
    const size = Math.max(rect.width, rect.height);
    r.className = 'ripple';
    r.style.width = r.style.height = size + 'px';
    r.style.left = (e.clientX - rect.left - size/2) + 'px';
    r.style.top = (e.clientY - rect.top - size/2) + 'px';
    btn.appendChild(r);
    setTimeout(()=>r.remove(), 600);
  });
}

/* ---------------- Generic detail modal ---------------- */
const Modal = {
  backdrop:null, panel:null, eyebrow:null, title:null, body:null,
  init(){
    this.backdrop = document.getElementById('modalBackdrop');
    if(!this.backdrop) return;
    this.panel = document.getElementById('modalPanel');
    this.eyebrow = document.getElementById('modalEyebrow');
    this.title = document.getElementById('modalTitle');
    this.body = document.getElementById('modalBody');
    document.getElementById('modalClose').addEventListener('click', ()=>this.close());
    this.backdrop.addEventListener('click', (e)=>{ if(e.target === this.backdrop) this.close(); });
    document.addEventListener('keydown', (e)=>{ if(e.key === 'Escape') this.close(); });
  },
  open(eyebrow, title, bodyHTML){
    if(!this.backdrop) return;
    this.eyebrow.textContent = eyebrow || 'Detail';
    this.title.textContent = title || '';
    this.body.innerHTML = bodyHTML || '';
    this.backdrop.classList.add('show');
  },
  close(){ this.backdrop && this.backdrop.classList.remove('show'); }
};

/* Delegate clicks on any [data-explain] element to open the modal.
   data-explain-title / data-explain-eyebrow / data-explain-body (HTML-escaped-safe text)
   let templates attach rich, per-metric explanations without extra JS. */
function initExplainDelegation(){
  document.addEventListener('click', (e)=>{
    const el = e.target.closest('[data-explain]');
    if(!el) return;
    if(e.target.closest('a,button,form,input,select,textarea')) return; // don't hijack real controls
    const title = el.getAttribute('data-explain-title') || el.getAttribute('data-explain') || 'Details';
    const eyebrow = el.getAttribute('data-explain-eyebrow') || 'Metric detail';
    const body = el.getAttribute('data-explain-body') || '<p>No further detail available.</p>';
    Modal.open(eyebrow, title, body);
  });
}

/* ============================================================
   Chart builders — pure inline SVG, no external dependencies
   (CSP-safe: no remote scripts, works offline / air-gapped labs)
   ============================================================ */
const SVGNS = 'http://www.w3.org/2000/svg';
function svgEl(tag, attrs){
  const el = document.createElementNS(SVGNS, tag);
  for(const k in attrs) el.setAttribute(k, attrs[k]);
  return el;
}

/* Line chart with gradient area fill, grid, and clickable data points. */
function renderLineChart(container){
  const raw = container.getAttribute('data-points');
  const labels = (container.getAttribute('data-labels')||'').split(',');
  const color = container.getAttribute('data-color') || '#ffffff';
  const unit = container.getAttribute('data-unit') || '';
  if(!raw) return;
  const values = raw.split(',').map(Number);
  const W = 640, H = 220, pad = 30;
  const max = Math.max(...values) * 1.15 || 1;
  const min = Math.min(0, Math.min(...values));
  const stepX = (W - pad*2) / (values.length - 1);
  const yFor = v => H - pad - ((v - min) / (max - min || 1)) * (H - pad*2);
  const pts = values.map((v,i)=>[pad + i*stepX, yFor(v)]);

  const svg = svgEl('svg', {viewBox:`0 0 ${W} ${H}`, preserveAspectRatio:'xMidYMid meet'});
  const gid = 'grad-' + Math.random().toString(36).slice(2);
  const defs = svgEl('defs', {});
  const grad = svgEl('linearGradient', {id:gid, x1:'0', y1:'0', x2:'0', y2:'1'});
  grad.appendChild(svgEl('stop', {offset:'0%', 'stop-color':color, 'stop-opacity':'0.35'}));
  grad.appendChild(svgEl('stop', {offset:'100%', 'stop-color':color, 'stop-opacity':'0'}));
  defs.appendChild(grad); svg.appendChild(defs);

  for(let i=0;i<=4;i++){
    const y = pad + i*(H-pad*2)/4;
    svg.appendChild(svgEl('line', {x1:pad, y1:y, x2:W-pad, y2:y, class:'chart-grid-line'}));
  }
  const areaD = `M${pts[0][0]},${H-pad} ` + pts.map(p=>`L${p[0]},${p[1]}`).join(' ') + ` L${pts[pts.length-1][0]},${H-pad} Z`;
  svg.appendChild(svgEl('path', {d:areaD, fill:`url(#${gid})`, class:'chart-area'}));
  const lineD = `M` + pts.map(p=>p.join(',')).join(' L');
  svg.appendChild(svgEl('path', {d:lineD, class:'chart-line-path', stroke:color}));

  pts.forEach((p,i)=>{
    const dot = svgEl('circle', {cx:p[0], cy:p[1], r:3.6, class:'chart-dot'});
    dot.addEventListener('click', ()=>{
      Modal.open('Trend point', labels[i] || `Point ${i+1}`,
        `<div class="mstat"><span>Value</span><b>${values[i]}${unit}</b></div>
         <div class="mstat"><span>Period</span><b>${labels[i]||'—'}</b></div>
         <p style="margin-top:12px">This point is one sample of the metric charted above, drawn from the assessment's tracked history. Click other points along the line to compare how this indicator moved over time.</p>`);
    });
    svg.appendChild(dot);
    if(i % Math.ceil(labels.length/6 || 1) === 0){
      const lbl = svgEl('text', {x:p[0], y:H-8, class:'chart-axis-label', 'text-anchor':'middle'});
      lbl.textContent = labels[i] || '';
      svg.appendChild(lbl);
    }
  });
  container.appendChild(svg);
}

/* Vertical bar chart, each bar clickable. */
function renderBarChart(container){
  const raw = container.getAttribute('data-points');
  const labels = (container.getAttribute('data-labels')||'').split(',');
  const colors = (container.getAttribute('data-colors')||'').split(',');
  if(!raw) return;
  const values = raw.split(',').map(Number);
  const W = 640, H = 220, pad = 30;
  const max = Math.max(...values) * 1.2 || 1;
  const gap = 14;
  const barW = (W - pad*2 - gap*(values.length-1)) / values.length;
  const svg = svgEl('svg', {viewBox:`0 0 ${W} ${H}`, preserveAspectRatio:'xMidYMid meet'});
  for(let i=0;i<=4;i++){
    const y = pad + i*(H-pad*2)/4;
    svg.appendChild(svgEl('line', {x1:pad, y1:y, x2:W-pad, y2:y, class:'chart-grid-line'}));
  }
  values.forEach((v,i)=>{
    const bh = (v/max) * (H - pad*2);
    const x = pad + i*(barW+gap);
    const y = H - pad - bh;
    const color = colors[i] || '#ffffff';
    const bar = svgEl('rect', {x, y, width:barW, height:bh, rx:6, class:'chart-bar', fill:color, style:`animation-delay:${i*0.06}s`});
    bar.addEventListener('click', ()=>{
      Modal.open('Category detail', labels[i] || `Series ${i+1}`,
        `<div class="mstat"><span>Count</span><b>${v}</b></div>
         <p style="margin-top:12px">Shows how many items fall into the <b>${labels[i]||'this'}</b> category out of the current dataset. Use the Findings or Attack Surface pages to drill into the underlying records.</p>`);
    });
    svg.appendChild(bar);
    const lbl = svgEl('text', {x:x+barW/2, y:H-8, class:'chart-axis-label', 'text-anchor':'middle'});
    lbl.textContent = labels[i] || '';
    svg.appendChild(lbl);
    const vlbl = svgEl('text', {x:x+barW/2, y:y-6, class:'chart-axis-label', 'text-anchor':'middle', fill:'#fff'});
    vlbl.textContent = v;
    svg.appendChild(vlbl);
  });
  container.appendChild(svg);
}

/* Donut chart with clickable segments + legend. */
function renderDonutChart(container){
  const raw = container.getAttribute('data-points');
  const labels = (container.getAttribute('data-labels')||'').split(',');
  const colors = (container.getAttribute('data-colors')||'').split(',');
  if(!raw) return;
  const values = raw.split(',').map(Number);
  const total = values.reduce((a,b)=>a+b,0) || 1;
  const size = 200, r = 70, cx = size/2, cy = size/2, circ = 2*Math.PI*r;
  const svg = svgEl('svg', {viewBox:`0 0 ${size} ${size}`});
  svg.appendChild(svgEl('circle', {cx, cy, r, fill:'none', stroke:'rgba(255,255,255,.06)', 'stroke-width':22}));
  let offset = 0;
  values.forEach((v,i)=>{
    const frac = v/total;
    const len = frac * circ;
    const seg = svgEl('circle', {
      cx, cy, r, fill:'none', stroke: colors[i]||'#fff', 'stroke-width':22,
      'stroke-dasharray': `${len} ${circ-len}`, 'stroke-dashoffset': -offset,
      transform:`rotate(-90 ${cx} ${cy})`, class:'chart-donut-seg', 'stroke-linecap':'butt'
    });
    seg.addEventListener('click', ()=>{
      Modal.open('Segment detail', labels[i] || `Segment ${i+1}`,
        `<div class="mstat"><span>Share</span><b>${(frac*100).toFixed(1)}%</b></div>
         <div class="mstat"><span>Count</span><b>${v}</b></div>
         <p style="margin-top:12px">${labels[i]||'This segment'} makes up ${(frac*100).toFixed(1)}% of the total tracked here.</p>`);
    });
    svg.appendChild(seg);
    offset += len;
  });
  const label = svgEl('text', {x:cx, y:cy+5, 'text-anchor':'middle', fill:'#fff', 'font-size':'20', 'font-weight':'700'});
  label.textContent = total;
  svg.appendChild(label);
  container.appendChild(svg);

  const legend = document.createElement('div');
  legend.className = 'chart-legend';
  values.forEach((v,i)=>{
    legend.innerHTML += `<span><i class="dot-sw" style="background:${colors[i]||'#fff'}"></i>${labels[i]||''} (${v})</span>`;
  });
  container.appendChild(legend);
}

function initCharts(){
  document.querySelectorAll('[data-chart="line"]').forEach(renderLineChart);
  document.querySelectorAll('[data-chart="bar"]').forEach(renderBarChart);
  document.querySelectorAll('[data-chart="donut"]').forEach(renderDonutChart);
}

document.addEventListener('DOMContentLoaded', ()=>{
  animateCounters();
  gaugeFill();
  initSidebar();
  initRipples();
  Modal.init();
  initExplainDelegation();
  initCharts();
});
