// Simple client-side utils
function qs(sel, el=document){ return el.querySelector(sel); }
function qsa(sel, el=document){ return Array.from(el.querySelectorAll(sel)); }

// Form validation helper
function attachRequired(form){
  form?.addEventListener('submit', (e)=>{
    const required = qsa('input[required], select[required]', form);
    for(const field of required){
      if(!field.value.trim()){
        field.focus();
        field.classList.add('invalid');
        e.preventDefault();
        return false;
      }
    }
  });
}

// Car list filtering
function initListFilter(){
  const input = qs('#carFilter');
  if(!input) return;
  const items = qsa('[data-car-item]');
  input.addEventListener('input', ()=>{
    const v = input.value.toLowerCase();
    for(const li of items){
      const name = li.dataset.name.toLowerCase();
      li.style.display = name.includes(v) ? '' : 'none';
    }
  });
}

// Small interaction: simulate honk on button hover
function initHonk(){
  qsa('button').forEach(btn => {
    btn.addEventListener('mouseenter', () => {
      btn.style.transform = 'translateY(-1px)';
    });
    btn.addEventListener('mouseleave', () => {
      btn.style.transform = '';
    });
  });
}

window.addEventListener('DOMContentLoaded', ()=>{
  attachRequired(qs('form'));
  initListFilter();
  initHonk();
  // Auto-dismiss toasts
  qsa('[data-toast]').forEach((el, i) => {
    setTimeout(() => {
      el.style.transition = 'opacity .3s, transform .3s';
      el.style.opacity = '0';
      el.style.transform = 'translateY(-6px)';
      setTimeout(()=> el.remove(), 350);
    }, 2200 + i*400);
  });

  // Page enter animation
  document.body.classList.add('page-enter');
  requestAnimationFrame(()=>{
    document.body.classList.add('page-enter-active');
    document.body.classList.remove('page-enter');
  });

  // 3D car tilt/parallax
  const scene = qs('#scene3d');
  const car = qs('#car3d');
  if(scene && car){
    let rafId;
    let currentY = 0;
    function onMove(e){
      const rect = scene.getBoundingClientRect();
      const x = (e.clientX - rect.left) / rect.width; // 0..1
      const y = (e.clientY - rect.top) / rect.height; // 0..1
      const rotY = (x - 0.5) * 16; // yaw
      const rotX = (0.5 - y) * 8;  // pitch
      cancelAnimationFrame(rafId);
      rafId = requestAnimationFrame(()=>{
        car.style.transform = `translate3d(-50%, -50%, 0) rotateX(${10 + rotX}deg) rotateY(${rotY}deg)`;
      });
    }
    scene.addEventListener('mousemove', onMove);
    scene.addEventListener('mouseleave', ()=>{
      car.style.transform = 'translate3d(-50%, -50%, 0) rotateX(10deg)';
    });

    // Scroll-based camera pan (translate stage on Z slightly)
    const stage = qs('.stage');
    function onScroll(){
      const max = 200; // px
      const y = Math.min(window.scrollY, max);
      if(y === currentY) return;
      currentY = y;
      const depth = -Math.round((y / max) * 40); // -40px at most
      stage && (stage.style.transform = `translateZ(${depth}px)`);
    }
    window.addEventListener('scroll', ()=>{
      cancelAnimationFrame(rafId);
      rafId = requestAnimationFrame(onScroll);
    }, { passive: true });
    onScroll();

    // Theme switcher
    const buttons = qsa('[data-car-theme]');
    function setTheme(name){
      const classes = ['car-sport','car-red','car-teal','car-gold','car-purple'];
      scene.classList.remove(...classes);
      scene.classList.add(name);
      try { localStorage.setItem('carTheme', name); } catch(_){}
    }
    const saved = (()=>{ try { return localStorage.getItem('carTheme'); } catch(_) { return null } })();
    if(saved){ setTheme(saved); }
    buttons.forEach(btn => {
      btn.addEventListener('click', ()=> setTheme(btn.getAttribute('data-car-theme')));
    });
  }

  // Real car images marquee: prefer local static images, fallback to CDN URLs
  const m1 = qs('[data-marquee="1"]');
  const m2 = qs('[data-marquee="2"]');
  const baseEl = qs('#realCars');
  const carsBase = baseEl?.getAttribute('data-cars-base') || '/static/cars/';
  const localFiles = [
    'mclaren-720s.svg',
    'ferrari-296-gtb.svg',
    'lamborghini-huracan.svg',
    'bugatti-chiron.svg',
    'astonmartin-vantage.svg'
  ];
  const cdnFallback = {
    'mclaren-720s.jpg': 'https://assets.mclaren.com/ii/mclaren/720s/overview/hero-720s-coupe.jpg',
    'ferrari-296-gtb.jpg': 'https://media.ferrari.com/images/auto_immagini/DB/0/762/181/1920-1080/296-gtb.jpg',
    'lamborghini-huracan.jpg': 'https://www-lamborghini-com.azureedge.net/cdn-cgi/image/format=auto/https://www.lamborghini.com/sites/it-en/files/DAM/lamborghini/model/huracan/sterato/overview/huracan_sterato_og.jpg',
    'bugatti-chiron.jpg': 'https://www.bugatti.com/fileadmin/_processed_/sei/p54/se-image-bugatti-chiron-profilee-hero.jpg',
    'astonmartin-vantage.jpg': 'https://www.astonmartin.com/-/media/models/vantage/vantage/og/vantage-og.jpg'
  };
  function buildRow(target){
    if(!target) return;
    const wrap = document.createElement('div');
    wrap.style.display = 'flex';
    wrap.style.gap = '24px';
    const list = [...localFiles, ...localFiles];
    for(const file of list){
      const img = new Image();
      const svgSrc = `${carsBase}${file}`;
      const jpgSrc = svgSrc.replace(/\.svg$/i, '.jpg');
      img.src = svgSrc;
      img.loading = 'lazy';
      img.onerror = () => {
        img.onerror = () => { const fallback = cdnFallback[file.replace('.svg','.jpg')] || cdnFallback[file]; if(fallback) img.src = fallback; };
        img.src = jpgSrc;
      };
      target.appendChild(img);
    }
  }
  buildRow(m1); buildRow(m2);

  // Show spinner on navigation and form submit
  const spinner = qs('#pageSpinner');
  function showSpinner(){ if(spinner){ spinner.classList.remove('hidden'); spinner.classList.add('show'); } }
  function hideSpinner(){ if(spinner){ spinner.classList.remove('show'); spinner.classList.add('hidden'); } }

  qsa('a[href]').forEach(a => {
    const href = a.getAttribute('href');
    if(!href || href.startsWith('#') || href.startsWith('mailto:') || href.startsWith('tel:')) return;
    a.addEventListener('click', (e)=>{
      // Allow ctrl/cmd click to open new tab without spinner
      if(e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.button !== 0) return;
      e.preventDefault();
      document.body.classList.add('page-exit');
      requestAnimationFrame(()=>{
        document.body.classList.add('page-exit-active');
        showSpinner();
        setTimeout(()=>{ window.location.href = href; }, 150);
      });
    });
  });

  qsa('form').forEach(form => {
    form.addEventListener('submit', ()=>{
      showSpinner();
    });
  });

  window.addEventListener('pageshow', ()=>{ hideSpinner(); });
});


