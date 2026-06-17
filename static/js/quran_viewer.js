(function () {
  const cfg = window.QURAN_VIEWER;
  if (!cfg) return;

  const canvas = document.getElementById('quran-pdf-canvas');
  const wrap = document.getElementById('quran-canvas-wrap');
  const scroll = document.getElementById('quran-canvas-scroll');
  const layer = document.getElementById('quran-highlight-layer');
  const noteEl = document.getElementById('quran-page-note');
  const labelEl = document.getElementById('quran-page-label');
  const zoomLabelEl = document.getElementById('quran-zoom-label');
  const statusEl = document.getElementById('quran-save-status');
  const dragPreview = document.getElementById('quran-drag-preview');

  const ZOOM_MIN = 0.5;
  const ZOOM_MAX = 2.5;
  const ZOOM_STEP = 0.15;

  let paraNumber = cfg.paraNumber;
  let pageNumber = cfg.pageNumber;
  let pageCount = 1;
  let pdfDoc = null;
  let highlights = Array.isArray(cfg.highlights) ? cfg.highlights.slice() : [];
  let activeColor = '#fff59d';
  let dragging = false;
  let dragStart = null;
  let saveTimer = null;
  let loading = false;
  let baseFitScale = 1;
  let zoomFactor = 1;

  if (window.pdfjsLib) {
    pdfjsLib.GlobalWorkerOptions.workerSrc =
      'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';
  }

  function paraPdfUrl(para) {
    const base = cfg.pdfUrl.replace(/para-\d{2}\.pdf/, `para-${String(para).padStart(2, '0')}.pdf`);
    return base;
  }

  function sessionUrl(para, page) {
    const u = new URL(window.location.href);
    u.searchParams.set('para', para);
    u.searchParams.set('page', page);
    return u.toString();
  }

  function setStatus(text) {
    if (statusEl) statusEl.textContent = text || '';
  }

  function containerWidth() {
    return (scroll && scroll.clientWidth) || (wrap && wrap.clientWidth) || 800;
  }

  function updateZoomLabel() {
    if (!zoomLabelEl) return;
    if (Math.abs(zoomFactor - 1) < 0.01) {
      zoomLabelEl.textContent = 'Fit';
    } else {
      zoomLabelEl.textContent = Math.round(zoomFactor * 100) + '%';
    }
  }

  function syncOverlaySize() {
    if (!layer || !canvas) return;
    layer.style.width = canvas.style.width || canvas.width + 'px';
    layer.style.height = canvas.style.height || canvas.height + 'px';
  }

  function renderHighlights() {
    if (!layer) return;
    layer.innerHTML = '';
    syncOverlaySize();
    highlights.forEach((hl) => {
      const div = document.createElement('div');
      div.className = 'quran-highlight';
      div.style.left = (hl.x * 100) + '%';
      div.style.top = (hl.y * 100) + '%';
      div.style.width = (hl.w * 100) + '%';
      div.style.height = (hl.h * 100) + '%';
      div.style.background = hl.color || '#fff59d';
      layer.appendChild(div);
    });
  }

  async function loadPdf(para) {
    if (!window.pdfjsLib) return;
    loading = true;
    setStatus('Loading…');
    const url = paraPdfUrl(para);
    pdfDoc = await pdfjsLib.getDocument(url).promise;
    pageCount = pdfDoc.numPages;
    if (pageNumber > pageCount) pageNumber = pageCount;
    if (pageNumber < 1) pageNumber = 1;
    await renderPage();
    loading = false;
  }

  async function renderPage() {
    if (!pdfDoc) return;
    const page = await pdfDoc.getPage(pageNumber);
    const viewportAtOne = page.getViewport({ scale: 1 });
    baseFitScale = containerWidth() / viewportAtOne.width;
    const scale = baseFitScale * zoomFactor;
    const viewport = page.getViewport({ scale });
    const ctx = canvas.getContext('2d');
    const dpr = window.devicePixelRatio || 1;
    canvas.width = Math.floor(viewport.width * dpr);
    canvas.height = Math.floor(viewport.height * dpr);
    canvas.style.width = Math.floor(viewport.width) + 'px';
    canvas.style.height = Math.floor(viewport.height) + 'px';
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    await page.render({ canvasContext: ctx, viewport }).promise;
    labelEl.textContent = `Juz ${paraNumber} · Page ${pageNumber} of ${pageCount}`;
    canvas.setAttribute(
      'aria-label',
      `Qur'an mushaf juz ${paraNumber}, page ${pageNumber} of ${pageCount}`,
    );
    syncOverlaySize();
    renderHighlights();
    setStatus('');
  }

  function setZoom(factor) {
    zoomFactor = Math.max(ZOOM_MIN, Math.min(ZOOM_MAX, factor));
    updateZoomLabel();
    renderPage();
  }

  async function fetchPageData(para, page) {
    const url = `${cfg.pageDataUrl}?para=${para}&page=${page}`;
    const res = await fetch(url, { headers: { Accept: 'application/json' } });
    if (!res.ok) return;
    const data = await res.json();
    highlights = data.highlights || [];
    if (noteEl) noteEl.value = data.note || '';
    renderHighlights();
  }

  function savePage() {
    if (!cfg.canEdit) return Promise.resolve();
    const payload = {
      para_number: paraNumber,
      page_number: pageNumber,
      note: noteEl ? noteEl.value : '',
      highlights: highlights,
    };
    setStatus('Saving…');
    return fetch(cfg.saveUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': cfg.csrfToken,
      },
      body: JSON.stringify(payload),
    })
      .then((res) => {
        if (res.ok) setStatus('Saved');
        else setStatus('Save failed');
      })
      .catch(() => setStatus('Save failed'));
  }

  async function goToPage(para, page, pushHistory) {
    if (loading) return;
    if (cfg.canEdit) await savePage();
    paraNumber = Math.max(1, Math.min(cfg.paraCount, para));
    pageNumber = Math.max(1, page);
    if (para !== cfg.paraNumber || !pdfDoc) {
      await loadPdf(paraNumber);
    } else {
      if (pageNumber > pageCount) pageNumber = pageCount;
      await renderPage();
    }
    await fetchPageData(paraNumber, pageNumber);
    if (pushHistory) {
      history.replaceState(null, '', sessionUrl(paraNumber, pageNumber));
    }
  }

  function relativePoint(evt) {
    const rect = wrap.getBoundingClientRect();
    const x = (evt.clientX - rect.left) / rect.width;
    const y = (evt.clientY - rect.top) / rect.height;
    return { x: Math.max(0, Math.min(1, x)), y: Math.max(0, Math.min(1, y)) };
  }

  function setupHighlightDrag() {
    if (!cfg.canEdit || !wrap) return;

    wrap.addEventListener('pointerdown', (evt) => {
      if (evt.button !== 0) return;
      dragging = true;
      dragStart = relativePoint(evt);
      if (dragPreview) {
        dragPreview.hidden = false;
        dragPreview.style.background = activeColor;
        dragPreview.style.left = (dragStart.x * 100) + '%';
        dragPreview.style.top = (dragStart.y * 100) + '%';
        dragPreview.style.width = '0';
        dragPreview.style.height = '0';
      }
      wrap.setPointerCapture(evt.pointerId);
    });

    wrap.addEventListener('pointermove', (evt) => {
      if (!dragging || !dragStart || !dragPreview) return;
      const cur = relativePoint(evt);
      const x = Math.min(dragStart.x, cur.x);
      const y = Math.min(dragStart.y, cur.y);
      const w = Math.abs(cur.x - dragStart.x);
      const h = Math.abs(cur.y - dragStart.y);
      dragPreview.style.left = (x * 100) + '%';
      dragPreview.style.top = (y * 100) + '%';
      dragPreview.style.width = (w * 100) + '%';
      dragPreview.style.height = (h * 100) + '%';
    });

    wrap.addEventListener('pointerup', (evt) => {
      if (!dragging || !dragStart) return;
      dragging = false;
      const cur = relativePoint(evt);
      const x = Math.min(dragStart.x, cur.x);
      const y = Math.min(dragStart.y, cur.y);
      const w = Math.abs(cur.x - dragStart.x);
      const h = Math.abs(cur.y - dragStart.y);
      if (dragPreview) dragPreview.hidden = true;
      dragStart = null;
      if (w > 0.01 && h > 0.005) {
        highlights.push({ x, y, w, h, color: activeColor });
        renderHighlights();
        savePage();
      }
    });
  }

  document.getElementById('quran-prev-page')?.addEventListener('click', () => {
    if (pageNumber > 1) goToPage(paraNumber, pageNumber - 1, true);
    else if (paraNumber > 1) goToPage(paraNumber - 1, 999, true);
  });

  document.getElementById('quran-next-page')?.addEventListener('click', () => {
    if (pageNumber < pageCount) goToPage(paraNumber, pageNumber + 1, true);
    else if (paraNumber < cfg.paraCount) goToPage(paraNumber + 1, 1, true);
  });

  document.getElementById('quran-prev-para')?.addEventListener('click', () => {
    if (paraNumber > 1) goToPage(paraNumber - 1, 1, true);
  });

  document.getElementById('quran-next-para')?.addEventListener('click', () => {
    if (paraNumber < cfg.paraCount) goToPage(paraNumber + 1, 1, true);
  });

  document.getElementById('quran-zoom-out')?.addEventListener('click', () => {
    setZoom(zoomFactor - ZOOM_STEP);
  });

  document.getElementById('quran-zoom-in')?.addEventListener('click', () => {
    setZoom(zoomFactor + ZOOM_STEP);
  });

  document.getElementById('quran-zoom-fit')?.addEventListener('click', () => {
    setZoom(1);
  });

  document.getElementById('quran-undo-highlight')?.addEventListener('click', () => {
    highlights.pop();
    renderHighlights();
    savePage();
  });

  document.querySelectorAll('.quran-color-btn').forEach((btn) => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.quran-color-btn').forEach((b) => b.classList.remove('is-active'));
      btn.classList.add('is-active');
      activeColor = btn.dataset.color;
    });
  });

  if (noteEl && cfg.canEdit) {
    noteEl.addEventListener('input', () => {
      clearTimeout(saveTimer);
      saveTimer = setTimeout(() => savePage(), 800);
    });
  }

  let resizeTimer;
  window.addEventListener('resize', () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => renderPage(), 150);
  });

  setupHighlightDrag();
  updateZoomLabel();
  loadPdf(paraNumber);
})();
